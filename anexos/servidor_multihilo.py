import socket
import threading

HOST = '0.0.0.0'
PORT = 12345


def manejar_cliente(conn, addr):
    print(f"[NUEVA CONEXION] {addr} conectado.")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[{addr}] Mensaje recibido: {data.decode()}")
            conn.sendall(data)  # eco
    print(f"[DESCONEXION] {addr} se ha desconectado.")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor multihilo escuchando en {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo.start()
            print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
