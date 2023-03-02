from fastapi import FastAPI
from response_handler import RabbitResponse
import pika
import pickle
import grpc
import ms2_pb2_grpc
import ms2_pb2

GRPC_PORT = 50054

app = FastAPI()
robin = 0

def runGRPC(operation,name=''):
    # operation = 0 --> call to list_files()
    # operaiton = 1 --> call to get_file()
    response = ''
    with grpc.insecure_channel(f'0.0.0.0:9010') as channel:
        stub = ms2_pb2_grpc.FileFindServiceStub(channel)
        if operation == 0:
            response = stub.list_files(ms2_pb2.Empty())
        else:
            response = stub.get_file(ms2_pb2.Name(name=name))

    return response

        

@app.get('/list_files')
def list_files():
    files_found = ''

    if robin == 0:
        files_found = runGRPC(0)
    else:
        body = pickle.dumps({'method':'list_files'})
        com = RabbitResponse()
        files_found = pickle.loads(com.call(body))

    return {"response":files_found}

@app.get('/get_file')
def get_file(name: str):
    is_found = ''
    
    if robin == 0:
        is_found = runGRPC(1)
    else:
        body = pickle.dumps({'method':'get_file', 'name':name})
        com = RabbitResponse()
        is_found = pickle.loads(com.call(body))

    return {"response":is_found}