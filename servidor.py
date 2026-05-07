import socket, threading, os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from criptografia import decifrar_mensagem, cifrar_mensagem

# Cores para o terminal
VERDE, AZUL, RESET = "\033[92m", "\033[94m", "\033[0m"

os.system('cls' if os.name == 'nt' else 'clear') # Limpa o terminal antes de iniciar

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048) # [cite: 17]
pem_public = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
)

def receber(conn, key):
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            print(f"\n{VERDE}[CRIPTOGRAFADO]: {data.hex()[:32]}...{RESET}")
            print(f"Descriptografando...")
            msg = decifrar_mensagem(data, key)
            print(f"{AZUL}CLIENTE:{RESET} {msg}\n> ", end="")
        except: break

def iniciar():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000)) # [cite: 19]
    server.listen(1)
    print(f"{VERDE}=== SERVIDOR DE CHAT SEGURO ATITUS ==={RESET}")
    print("Aguardando conexão do cliente...")

    conn, addr = server.accept()
    conn.send(pem_public) # Troca de chaves [cite: 25, 29]
    session_key = private_key.decrypt(
        conn.recv(256), padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    
    print(f"{VERDE}[!] Conexão estabelecida com {addr}{RESET}")
    threading.Thread(target=receber, args=(conn, session_key), daemon=True).start()

    while True:
        txt = input("> ")
        if txt.lower() == 'sair': break
        conn.send(cifrar_mensagem(txt, session_key)) # [cite: 26]

if __name__ == "__main__":
    iniciar()