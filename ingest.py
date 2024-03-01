from langchain_community.document_loaders import DirectoryLoader,UnstructuredFileLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveJsonSplitter
from langchain_community.vectorstores import Qdrant
import os



loader = DirectoryLoader('./JSON/', glob="**/*.json", show_progress=True,loader_cls=UnstructuredFileLoader)
docs = loader.load()
splitter = RecursiveJsonSplitter(max_chunk_size=300)
json_chunks = splitter.split_json(json_data=docs)
print(json_chunks)


model_kwargs={'device' :'cpu'}
encode_kwargs={'normalize_embeddings' :  False}
embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-large-en", model_kwargs=model_kwargs,encode_kwargs=encode_kwargs)
print(embeddings)

url = "http://localhost:6333"


try:
    qdrant = Qdrant.from_documents(
        json_chunks,
        embeddings,
        url=url,
        prefer_grpc=False,
        collection_name="hack_db"
    )
    print("Vector DB Successfully Created!")
except Exception as e:
    print("Error:", e)
