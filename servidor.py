import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

public_key = private_key.public_key()

pem_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(1)
    print("Servidor aguardando conexão...")

    conn, addr = server.accept()
    try:
        conn.send(pem_public_key)
        print("Chave pública enviada.")

        encrypted_session_key = conn.recv(256)
        
        session_key = private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"Chave de sessão (AES) recebida e decifrada: {session_key.hex()}")
        
    finally:
        conn.close()
        server.close()

if __name__ == "__main__":
    iniciar_servidor()