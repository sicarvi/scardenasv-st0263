from fastapi import FastAPI
from response_handler import RabbitResponse
import pika
import pickle
import grpc
import ms2_pb2_grpc
import ms2_pb2
from google.protobuf.json_format import MessageToDict
import json

f = open('config.json')
settings = json.load(f)
GRPC_PORT = settings['GRPC_PORT']
f.close()

app = FastAPI()
robin = 0

def runGRPC(operation,name=''):
    # operation = 0 --> call to list_files()
    # operaiton = 1 --> call to get_file()
    response = ''
    with grpc.insecure_channel(f'127.0.0.1:{GRPC_PORT}') as channel:
        stub = ms2_pb2_grpc.FileFindServiceStub(channel)
        if operation == 0:
            response = stub.list_files(ms2_pb2.Empty())
        else:
            response = stub.get_file(ms2_pb2.Name(name=name))

    return MessageToDict(response)

@app.get('/list_files')
def list_files():
    files_found = ''
    global robin

    if robin == 0:
        robin+=1
        files_found = runGRPC(0)
        return files_found
    else:
        robin-=1
        body = pickle.dumps({'method':'list_files'})
        com = RabbitResponse()
        files_found = pickle.loads(com.call(body))

    return {"response":files_found}

@app.get('/get_file')
def get_file(name: str):
    is_found = ''
    global robin
    
    if robin == 0:
        robin+=1
        is_found = runGRPC(1, name)
    else:
        robin-=1
        body = pickle.dumps({'method':'get_file', 'name':name})
        com = RabbitResponse()
        is_found = pickle.loads(com.call(body))

    return {"response":is_found}