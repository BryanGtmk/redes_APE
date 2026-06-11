import socket
import threading

HOST = '0.0.0.0'
PORT = 11000


def recibir(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[INFO] El cliente cerro la conexion.")
                break
            print(f"\nCliente dice: {data.decode('utf-8')}")
            print("Tu respuesta (Servidor): ", end="", flush=True)
        except (ConnectionResetError, ConnectionAbortedError):
            print("\n[ERROR] La conexion se perdio inesperadamente.")
            break


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor de chat escuchando en {HOST}:{PORT} ...")
        conn, addr = s.accept()
        print(f"Cliente conectado desde {addr}")

        hilo_recepcion = threading.Thread(target=recibir, args=(conn,), daemon=True)
        hilo_recepcion.start()

        try:
            while True:
                msg = input("Tu respuesta (Servidor): ")
                conn.sendall(msg.encode('utf-8'))
                if msg.lower() == 'salir':
                    break
        except (BrokenPipeError, ConnectionResetError):
            print("[ERROR] No se pudo enviar el mensaje al cliente.")
        finally:
            conn.close()
            print("Conexion finalizada.")


if __name__ == "__main__":
    main()
