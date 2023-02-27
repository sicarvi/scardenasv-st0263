from fastapi import FastAPI
from response_handler import RabbitResponse
import pika
import pickle

app = FastAPI()


@app.get('/list_files')
def list_files():
    files_found = ''
    body = pickle.dumps({'method':'list_files'})
    com = RabbitResponse()
    files_found = pickle.loads(com.call(body))

    return {"response":files_found}

@app.get('/get_file')
def list_files(name: str):
    is_found = ''
    body = pickle.dumps({'method':'get_file', 'name':name})
    com = RabbitResponse()
    is_found = pickle.loads(com.call(body))

    return {"response":is_found}