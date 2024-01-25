from langchain.agents import tool
import os

@tool
def getDocumentCharged(prompt, carpeta="./md_folder/"): 
    """Devuelve el numero de archivos cargados."""
    listFiles = os.listdir(carpeta)
    numFiles = len(listFiles) 
    return f"Hay cargados {numFiles} archivos"
