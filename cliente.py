import socket, threading, os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from criptografia import cifrar_mensagem, decifrar_mensagem

VERDE, AMARELO, RESET = "\033[92m", "\033[93m", "\033[0m"

os.system('cls' if os.name == 'nt' else 'clear')

def receber(client, key):
    while True:
        try:
            data = client.recv(1024)
            if not data: break
            print(f"\n{VERDE}[CRIPTOGRAFADO]: {data.hex()[:32]}...{RESET}")
            print(f"Descriptografando...")
            msg = decifrar_mensagem(data, key)
            print(f"{AMARELO}SERVIDOR:{RESET} {msg}\n> ", end="")
        except: break

def iniciar():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))

    # Handshake RSA [cite: 17, 25]
    pub_key = serialization.load_pem_public_key(client.recv(1024))
    session_key = os.urandom(16) # Chave 128 bits [cite: 26]
    client.send(pub_key.encrypt(
        session_key, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    ))

    print(f"{VERDE}=== CLIENTE DE CHAT CONECTADO ==={RESET}")
    threading.Thread(target=receber, args=(client, session_key), daemon=True).start()

    while True:
        txt = input("> ")
        if txt.lower() == 'sair': break
        client.send(cifrar_mensagem(txt, session_key))

if __name__ == "__main__":
    iniciar()