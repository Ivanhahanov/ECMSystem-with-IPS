from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import AsyncElasticsearch
from .indexing_files import add_files_to_elasticsearch
app = FastAPI()
es = AsyncElasticsearch()
origins = [
    "http://localhost",
    "http://192.168.0.218:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"data": "hello"}


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    print(file.file)
    contents = await file.read()
    with open(f"/app/files/{file.filename}", 'w') as f:
        f.write(contents.decode())
    add_files_to_elasticsearch()
    return {"filename": file.filename}
