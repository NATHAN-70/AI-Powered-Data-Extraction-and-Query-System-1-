from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

import os

from src.extractor import Extractor
from src.embedding import get_embedding
from src.vector_db import (
    insert_data,
    search_data
)

from src.rag import generate_answer

app = FastAPI()


def chunk_text(
    text,
    size=500
):

    return [
        text[i:i+size]
        for i in range(
            0,
            len(text),
            size
        )
    ]


@app.post("/load")
async def load_data(

    source_type: str = Form(...),

    url: str = Form(None),

    file: UploadFile = File(None)
):

    try:

        if source_type == "url":

            text = Extractor.extract_url(
                url
            )

        else:

            os.makedirs("uploads", exist_ok=True)

            path = (
                f"uploads/"
                f"{file.filename}"
            )

            with open(
                path,
                "wb"
            ) as f:

                f.write(
                    await file.read()
                )

            if file.filename.endswith(
                ".pdf"
            ):

                text = Extractor.extract_pdf(
                    path
                )

            else:

                text = Extractor.extract_image(
                    path
                )

        chunks = chunk_text(text)

        for chunk in chunks:

            emb = get_embedding(chunk)

            insert_data(
                chunk,
                emb
            )

        return {
            "status": "success",
            "chunks": len(chunks)
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/query")
def query(question: str):

    try:

        query_emb = get_embedding(
            question
        )

        docs = search_data(
            query_emb
        )

        context = "\n".join(docs)

        answer = generate_answer(
            context,
            question
        )

        return {
            "answer": answer
        }

    except Exception as e:

        return {
            "error": str(e)
        }
