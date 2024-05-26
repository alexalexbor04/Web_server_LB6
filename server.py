import socket
import threading

def handle_client(client_socket):
    with client_socket:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"\nReceived request:\n{request}")

        http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
        client_socket.sendall(http_response.encode('utf-8'))


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Разрешено подключение от {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    IP = input("Введите IP-адрес сервера (по умолчанию 127.0.0.1): ")
    if IP == '':
        IP = "127.0.0.1"

    PORT = input('Введите порт для внешнего подключения (по умолчанию 80): ')
    if PORT == '':
        PORT = 80
    else:
        PORT = int(PORT)

    start_server(IP, PORT)
