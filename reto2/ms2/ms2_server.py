from os import listdir, getcwd, walk
from os.path import isfile, join
import grpc
import ms2_pb2_grpc
import ms2_pb2
from concurrent import futures
import json

DIR_NAME = ""
PORT = 0

class MS2Servicer(ms2_pb2_grpc.FileFindServiceServicer):

    def list_files(self, request, context):
        p = join(getcwd(),DIR_NAME)
        files_found = [f for f in listdir(p) if isfile(join(p, f))]
        return ms2_pb2.Response1(files=files_found)
    
    def get_file(self, request, context):
        isFound = 'File not found.'
        name = request.name
        p = join(getcwd(),DIR_NAME)
        for root, dirs, files in walk(p):
            if name in files:
                isFound = 'Exists!'

        return ms2_pb2.Response2(is_found=isFound)
    
def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    ms2_pb2_grpc.add_FileFindServiceServicer_to_server(MS2Servicer(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    print('gRPC server is up and running')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    f = open('config.json')
    settings = json.load(f)
    DIR_NAME = settings['DIR_NAME']
    PORT = settings['PORT']
    f.close()
    main()