import socket, threading, os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from criptografia import decifrar_mensagem, cifrar_mensagem

VERDE, AZUL, CIANO, RESET = "\033[92m", "\033[94m", "\033[96m", "\033[0m"
os.system('cls' if os.name == 'nt' else 'clear')

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pem_public = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
)

def receber(conn, key):
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            
            print(f"\r\033[K{VERDE}[DADOS CRIPTOGRAFADOS]: {data.hex()[:32]}...{RESET}")
            print("descriptografando.....")
            
            msg = decifrar_mensagem(data, key)
            print(f"\033[K{AZUL}Cliente:{RESET} {msg}")
            print(f"Digite sua mensagem: ", end="", flush=True)
        except:
            print(f"\n{VERDE}[SISTEMA]{RESET} Conexão encerrada.")
            break

def iniciar():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(1)
    print(f"{VERDE}=== SERVIDOR INICIADO ==={RESET}")

    conn, addr = server.accept()
    conn.send(pem_public)
    print(f"{CIANO}[INFO]{RESET} Chave Pública enviada.")

    pacote_chave = conn.recv(256)
    print(f"{VERDE}[CHAVE CRIPTOGRAFADA RECEBIDA]:{RESET} {pacote_chave.hex()[:64]}...")
    
    session_key = private_key.decrypt(
        pacote_chave, 
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    print(f"{CIANO}[SUCESSO]{RESET} Chave de sessão AES estabelecida.")
    threading.Thread(target=receber, args=(conn, session_key), daemon=True).start()
    
    while True:
        txt = input("Digite sua mensagem: ") 
        if txt.lower() == 'sair': break
        if txt.strip():
            print(f"\033[A\033[KVocê: {txt}")
            conn.send(cifrar_mensagem(txt, session_key))

if __name__ == "__main__":
    iniciar()