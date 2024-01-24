from langchain.agents import tool
import os

@tool
def getDocumentCharged(carpeta:str)->int:
    """Devuelve el numero de archivos cargados."""
    listFiles = os.listdir(carpeta)
    print(listFiles)
    return len(listFiles)


print(getDocumentCharged("./md"))
