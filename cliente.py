import socket
import os
import threading
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from criptografia import cifrar_mensagem, decifrar_mensagem

def receber_mensagens(client, session_key):
    while True:
        try:
            data = client.recv(1024)
            if not data: break
            msg = decifrar_mensagem(data, session_key)
            print(f"\n[Servidor]: {msg}\n> ", end="")
        except Exception:
            print("\n[Erro] Conexão encerrada pelo servidor.")
            break

def rodar_cliente():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))

    try:
        pub_data = client.recv(1024)
        public_key = serialization.load_pem_public_key(pub_data)
        
        session_key = os.urandom(16)
        enc_key = public_key.encrypt(
            session_key,
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        client.send(enc_key)
        print("[!] Handshake concluído. Pode digitar.")

        # Inicia thread para escutar o servidor
        threading.Thread(target=receber_mensagens, args=(client, session_key), daemon=True).start()

        while True:
            texto = input("> ")
            if texto.lower() == 'sair': break
            client.send(cifrar_mensagem(texto, session_key))
    finally:
        client.close()

if __name__ == "__main__":
    rodar_cliente()