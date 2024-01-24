from langchain.agents import tool
import os

@tool
def getDocumentCharged(carpeta):
    """Devuelve el numero de archivos cargados."""
    listFiles = os.listdir(carpeta)
    numFiles = len(listFiles) 
    return f"Hay cargados {numFiles} archivos"

