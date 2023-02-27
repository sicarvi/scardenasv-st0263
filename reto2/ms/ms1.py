from os import listdir, getcwd, walk
from os.path import isfile, join
import pika
import pickle

DIR_NAME = "example_files"

def list_files():
    p = join(getcwd(),DIR_NAME)
    files_found = [f for f in listdir(p) if isfile(join(p, f))]
    return files_found

def get_file(name:str):
    isFound = 'File not found.'
    p = join(getcwd(),DIR_NAME)
    for root, dirs, files in walk(p):
        if name in files:
            isFound = 'Exists!'
    return isFound

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("user", "password")))
channel = connection.channel()

def callback(ch, method, props, body):
    body = pickle.loads(body)
    print(f"LLEGO ESTO: {body}")
    if body.get('method') == 'list_files':
        response = pickle.dumps(list_files())
    elif body.get('method') == 'get_file':
        name = body.get('name')
        response = pickle.dumps(get_file(name))


    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
channel.basic_consume(queue="requests", on_message_callback=callback)
print('Initalized and listening')
channel.start_consuming()

