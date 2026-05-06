import socket
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def iniciar_cliente():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))

    try:
        public_key_data = client.recv(1024)
        public_key = serialization.load_pem_public_key(public_key_data)
        print("Chave pública do servidor recebida.")

        session_key = os.urandom(16) 
        print(f"Chave de sessão gerada: {session_key.hex()}")

        encrypted_session_key = public_key.encrypt(
            session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        client.send(encrypted_session_key)
        print("Chave de sessão cifrada enviada ao servidor.")

    finally:
        client.close()

if __name__ == "__main__":
    iniciar_cliente()