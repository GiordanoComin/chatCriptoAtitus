import socket
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from criptografia import cifrar_mensagem

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

        print("Chat iniciado. Digite 'sair' para encerrar.")
        while True:
            texto = input("> ")
            if texto.lower() == 'sair': break
            
            pacote = cifrar_mensagem(texto, session_key)
            client.send(pacote)
    finally:
        client.close()

if __name__ == "__main__":
    rodar_cliente()