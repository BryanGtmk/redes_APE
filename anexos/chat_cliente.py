import socket
import threading

HOST = '127.0.0.1'
PORT = 11000


def recibir(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[INFO] El servidor cerro la conexion.")
                break
            print(f"\nServidor dice: {data.decode('utf-8')}")
            print("Tu mensaje (Cliente): ", end="", flush=True)
        except (ConnectionResetError, ConnectionAbortedError):
            print("\n[ERROR] La conexion se perdio inesperadamente.")
            break


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print("[ERROR] No se pudo conectar. ¿El servidor esta encendido?")
            return

        print(f"Conectado al chat del servidor.")
        print("Escribe 'salir' para terminar la conversacion de forma segura.\n")

        hilo_recepcion = threading.Thread(target=recibir, args=(s,), daemon=True)
        hilo_recepcion.start()

        try:
            while True:
                msg = input("Tu mensaje (Cliente): ")
                s.sendall(msg.encode('utf-8'))
                if msg.lower() == 'salir':
                    break
        except (BrokenPipeError, ConnectionResetError):
            print("[ERROR] El servidor finalizo la conexion.")


if __name__ == "__main__":
    main()
