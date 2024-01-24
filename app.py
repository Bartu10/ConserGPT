import os
import gradio as gr

from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate

from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceBgeEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader


local_llm = "zephyr-7b-alpha.Q5_K_S.gguf"

config = {
    'max_new_tokens': 1024,
    'repetition_penalty': 1.1,
    'temperature': 0,
    'top_k': 20,
    'top_p': 0.9,
    'stream': True,
    'threads': int(os.cpu_count() / 2)
}

llm = CTransformers(
    model=local_llm,
    model_type="zephyr",
    lib="avx2",  # for CPU use
    **config
)

print("LLM Initialized...")

def format_prompt(context: str, question: str) -> str:
    if "getDocumentCharged" in question:
        num_files = getDocumentCharged("./md")
        return f"Contexto: {context}\nPregunta: {question}\n\nNúmero de archivos cargados: {num_files}"
    else:
        return f"Contexto: {context}\nPregunta: {question}\n\nRespuesta útil:"

prompt_template = """Utiliza la siguiente información para responder a la pregunta del usuario.
Si no sabes la respuesta, di simplemente que no la sabes, no intentes inventarte una respuesta.

{formatted_prompt}
"""

prompt = PromptTemplate(template=prompt_template,
                        input_variables=['context', 'question'])

# Format the prompt based on the keyword
formatted_prompt = format_prompt("Contexto de ejemplo", "¿Cuántos archivos hay en la carpeta?")
prompt_output = prompt.format(context="Contexto de ejemplo", question="¿Cuántos archivos hay en la carpeta?", formatted_prompt=formatted_prompt)


model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)


load_vector_store = Chroma(
    persist_directory="stores/ConserGPT/", embedding_function=embeddings)
retriever = load_vector_store.as_retriever(search_kwargs={"k": 1})

chain_type_kwargs = {"prompt": prompt}


def get_response(input):
    query = input
    chain_type_kwargs = {"prompt": prompt}
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                     return_source_documents=True, chain_type_kwargs=chain_type_kwargs, verbose=True)
    response = qa(query)
    return response["result"]


input = gr.Text(
    label="Prompt",
    show_label=False,
    max_lines=1,
    placeholder="Enter your prompt",
    container=False,
)

iface = gr.Interface(fn=get_response,
                     inputs=input,
                     outputs="text",
                     title="ConserGPT",
                     description="This is a RAG implementation based on Zephyr 7B Alpha LLM.",
                     allow_flagging='never'
                     )

iface.launch(share=True)
