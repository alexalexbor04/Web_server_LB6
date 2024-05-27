import socket
import threading
from os.path import join, isfile
from datetime import datetime
from server_config import *


def logging(date, addr, path):
    with open('log.txt', 'a') as logs:
        logs.write(f'<{date}> {addr}: {path}\n')

def add_date():
    return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GTM')

def add_code(path, extension):
    if not isfile(path):
        return 404
    elif extension not in ALLOWED_TYPES:
        return 403
    else:
        return 200

def generate_path(request):
    path = request.split('\n')[0].split(' ')[1][1:]
    if not path:
        path = DEF
    return join(DIR, path)

def get_extension(path):
    return path.split('.')[-1]

def http_processing(request, addr):
    path = generate_path(request)
    extension = get_extension(path)
    code = add_code(path, extension)
    date = add_date()
    body = b''
    if code == 200:
        body = file_reader(path)  
    else:
        extension = 'html'
    response = PAT.format(code, CODES[code], date, TYPES[extension], len(body)).encode() + body
    logging(date, addr, path)
    return response

def file_reader(path):
    try:
        if isfile(path):
            with open(path, 'rb') as f:
                return f.read()
        else:
            print(f"Нет такого файла: {path}")
            return None
    except Exception as e:
        print(f"Ошибка чтения файла {path}: {e}")
        return None

def handle_client(client_socket, addr):
    with client_socket:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"\nПолученный запрос:\n{request}")
        if request:
            http_response = http_processing(request, addr)
            client_socket.sendall(http_response)

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Разрешено подключение от {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


if __name__ == "__main__":
    IP = input("Введите IP-адрес сервера (по умолчанию 127.0.0.1): ")
    if IP == '':
        IP = "127.0.0.1"

    PORT = input('Введите порт (по умолчанию 80): ')
    if PORT == '':
        PORT = 80
    else:
        PORT = int(PORT)

    start_server(IP, PORT)