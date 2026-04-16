import requests

url = "http://localhost:8000/ingest"

files = {
    "file": open("/home/robertopsf/rag-system/client/teste.txt", "rb")
}

response = requests.post(url, files=files)

print(response.json())