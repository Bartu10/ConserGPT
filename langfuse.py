import os
from langfuse import Langfuse

 
# Get keys for your project from the project settings page
# https://cloud.langfuse.com
os.environ["LANGFUSE_PUBLIC_KEY"] = "sk-lf-bc068304-7e5d-4eab-a5d2-67080f948d0a"
os.environ["LANGFUSE_SECRET_KEY"] = "pk-lf-91342c92-5649-4d6e-9417-73aa75e93edd"
 
# Your host, defaults to https://cloud.langfuse.com
# For US data region, set to "https://us.cloud.langfuse.com"
# os.environ["LANGFUSE_HOST"] = "http://localhost:3000"

 
langfuse = Langfuse()