import os
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader
from agents.tool import getDocumentCharged


model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

nombre_archivo = "./md/acuerdos_acuerdo202-10-200720deporte20escuela.md"

try:
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    print(f"El archivo '{nombre_archivo}' no se encontró.")
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")


headersToSplitOn = [("#", "Header"), ("##", "Title")]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on = headersToSplitOn)
md_header_splits = markdown_splitter.split_text(contenido)


for document in md_header_splits:    
    # Extraer y mostrar los metadatos
    metadata = document.metadata
    page_content = document.page_content
    for key, value in metadata.items():
        print("##########################################################################")
        print(f"{value}{page_content}")

vector_store = Chroma.from_documents(md_header_splits, embeddings, collection_metadata={"hnsw:space": "cosine"}, persist_directory="stores/ConserGPT")





