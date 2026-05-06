import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from criptografia import decifrar_mensagem

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pem_public = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

def rodar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(1)
    print("--- Servidor Aguardando Conexão ---")

    conn, addr = server.accept()
    try:
        conn.send(pem_public) 
        enc_key = conn.recv(256)
        
        session_key = private_key.decrypt(
            enc_key,
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        print("[!] Conexão segura estabelecida.")

        while True:
            data = conn.recv(1024)
            if not data: break
            try:
                msg = decifrar_mensagem(data, session_key)
                print(f"Mensagem: {msg}")
            except Exception:
                print("[ALERTA] Mensagem adulterada detectada!")
    finally:
        conn.close()

if __name__ == "__main__":
    rodar_servidor()