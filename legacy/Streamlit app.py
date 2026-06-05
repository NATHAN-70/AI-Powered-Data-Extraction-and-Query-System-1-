import os
import streamlit as st
import requests
from requests.exceptions import RequestException

# Allow overriding API URL via environment variable for flexibility in dev
API = os.getenv("API_URL", "http://localhost:8000")

st.title(
    "Multi Source RAG Assistant"
)

option = st.selectbox(
    "Choose Source",
    [
        "URL",
        "PDF",
        "IMAGE"
    ]
)

if option == "URL":

    url = st.text_input(
        "Enter URL"
    )

    if st.button(
        "Load URL"
    ):

        try:
            response = requests.post(
                f"{API}/load",
                data={
                    "source_type": "url",
                    "url": url
                },
                timeout=60
            )
            res_data = response.json()
            if "error" in res_data:
                st.error(res_data["error"])
            else:
                st.success(f"Loaded URL successfully! Chunks created: {res_data.get('chunks', 0)}")
                st.json(res_data)
        except RequestException as e:
            st.error(f"Failed to reach API at {API}. Is the backend running? Error: {e}")
        except Exception as e:
            st.error(f"Error parsing response: {e}. Raw response: {getattr(response, 'text', '')}")

else:

    uploaded_file = st.file_uploader(
        "Upload File"
    )

    if st.button(
        "Upload"
    ):

        if uploaded_file is None:
            st.error("Please choose a file to upload first.")
        else:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

            try:
                response = requests.post(
                    f"{API}/load",
                    files=files,
                    data={"source_type": "file"},
                    timeout=60,
                )
                res_data = response.json()
                if "error" in res_data:
                    st.error(res_data["error"])
                else:
                    st.success(f"Uploaded and processed file successfully! Chunks created: {res_data.get('chunks', 0)}")
                    st.json(res_data)
            except RequestException as e:
                st.error(f"Failed to reach API at {API}. Is the backend running? Error: {e}")
            except Exception as e:
                st.error(f"Error parsing response: {e}. Raw response: {getattr(response, 'text', '')}")

st.divider()

query = st.text_area(
    "Ask Question"
)

if st.button(
    "Generate Answer"
):

    try:
        response = requests.post(
            f"{API}/query",
            params={
                "question": query
            },
            timeout=60
        )
        res_data = response.json()
        if "error" in res_data:
            st.error(res_data["error"])
        elif "answer" in res_data:
            st.write(res_data["answer"])
        else:
            st.error(f"Unexpected response from API: {res_data}")
    except RequestException as e:
        st.error(f"Failed to reach API at {API}. Is the backend running? Error: {e}")
    except Exception as e:
        st.error(f"Error parsing response: {e}. Raw response: {getattr(response, 'text', '')}")
