import os
import logging
from typing import List, Optional

from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

collection: Optional[Collection] = None
_initialized = False

# Local fallback storage (used if Milvus can't be reached)
_local_store = {
    "texts": [],
    "embeddings": None  # numpy array of shape (n, dim)
}
_local_store_path = os.path.join(os.path.dirname(__file__), "local_vectors.npz")

try:
    import numpy as _np
except Exception:
    _np = None

# Configurable via environment variables. Defaults target a local Milvus server.
MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
COLLECTION_NAME = os.getenv("MILVUS_COLLECTION", "rag_collection")
EMBED_DIM = int(os.getenv("EMBED_DIM", "384"))

def init_db():
    global collection, _initialized
    if _initialized:
        return

    # Connect to Milvus. Use host/port (pymilvus >=2.x) by default. If you were using
    # local persistent uri or a different configuration, set MILVUS_HOST/MILVUS_PORT.
    try:
        logger.info("Connecting to Milvus at %s:%s", MILVUS_HOST, MILVUS_PORT)
        connections.connect(alias="default", host=MILVUS_HOST, port=MILVUS_PORT)
    except Exception as exc:
        # If Milvus isn't available, fall back to a local numpy store for development
        logger.warning("Failed to connect to Milvus, falling back to local numpy store: %s", exc)
        if _np is None:
            raise RuntimeError(
                "Milvus not available and numpy is not installed. Install numpy or start Milvus. "
                "Original error: %s" % exc
            ) from exc
        # try loading existing local store from disk
        if os.path.exists(_local_store_path):
            try:
                data = _np.load(_local_store_path, allow_pickle=True)
                _local_store["texts"] = data["texts"].tolist()
                _local_store["embeddings"] = data["embeddings"]
            except Exception:
                logger.exception("Failed to load existing local vector store, starting fresh")
                _local_store["texts"] = []
                _local_store["embeddings"] = None
        else:
            _local_store["texts"] = []
            _local_store["embeddings"] = None
        _initialized = True
        return

    fields = [
        FieldSchema(
            name="id",
            dtype=DataType.INT64,
            is_primary=True,
            auto_id=True
        ),
        FieldSchema(
            name="text",
            dtype=DataType.VARCHAR,
            max_length=5000
        ),
        FieldSchema(
            name="embedding",
            dtype=DataType.FLOAT_VECTOR,
            dim=384
        )
    ]

    schema = CollectionSchema(fields)

    try:
        collection = Collection(COLLECTION_NAME)
        logger.info("Opened existing collection '%s'", COLLECTION_NAME)
    except Exception:
        logger.info("Creating collection '%s'", COLLECTION_NAME)
        collection = Collection(COLLECTION_NAME, schema)
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128},
        }
        collection.create_index(field_name="embedding", index_params=index_params)

    _initialized = True


def insert_data(text: str, embedding: List[float]):
    """Insert a single text + embedding into the collection.

    Raises RuntimeError if Milvus is not available.
    """
    init_db()
    if collection is None and _np is None:
        raise RuntimeError("Milvus collection is not initialized and numpy is not available for fallback")

    # pymilvus expects a column-wise list of lists matching schema fields.
    try:
        if collection is not None:
            collection.insert([[text], [embedding]])
            collection.flush()
            return

        # Local fallback
        _local_store["texts"].append(text)
        emb = _np.array(embedding, dtype=_np.float32)
        if _local_store["embeddings"] is None:
            _local_store["embeddings"] = emb.reshape(1, -1)
        else:
            _local_store["embeddings"] = _np.vstack([_local_store["embeddings"], emb.reshape(1, -1)])

        # persist to disk
        try:
            _np.savez_compressed(_local_store_path, texts=_local_store["texts"], embeddings=_local_store["embeddings"])
        except Exception:
            logger.exception("Failed to persist local vector store to disk")

    except Exception as exc:
        logger.exception("Failed to insert data into collection or local store")
        raise


def search_data(query_embedding: List[float], limit: int = 3) -> List[str]:
    """Search for nearest neighbors and return texts.

    Returns a list of texts (may be shorter than `limit` if collection is empty).
    """
    init_db()
    if collection is None and _np is None:
        raise RuntimeError("Milvus collection is not initialized and numpy is not available for fallback")

    try:
        if collection is not None:
            collection.load()
            result = collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param={"metric_type": "L2"},
                limit=limit,
                output_fields=["text"],
            )

            # result is a list per query; we only queried with 1 vector so take result[0]
            hits = result[0] if len(result) > 0 else []
            texts: List[str] = []
            for hit in hits:
                entity = getattr(hit, "entity", None)
                if entity:
                    text = entity.get("text")
                    texts.append(text)
            return texts

        # Local fallback search using numpy (brute-force L2)
        if _local_store["embeddings"] is None or len(_local_store["texts"]) == 0:
            return []

        q = _np.array(query_embedding, dtype=_np.float32)
        vecs = _local_store["embeddings"]
        # compute L2 distances
        dists = _np.linalg.norm(vecs - q.reshape(1, -1), axis=1)
        idx = _np.argsort(dists)[:limit]
        return [ _local_store["texts"][i] for i in idx.tolist() ]

    except Exception as exc:
        logger.exception("Failed during search")
        raise
