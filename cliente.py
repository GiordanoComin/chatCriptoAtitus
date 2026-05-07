import socket, threading, os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from criptografia import cifrar_mensagem, decifrar_mensagem

VERDE, AMARELO, CIANO, RESET = "\033[92m", "\033[93m", "\033[96m", "\033[0m"
os.system('cls' if os.name == 'nt' else 'clear')

def receber(client, key):
    while True:
        try:
            data = client.recv(1024)
            if not data: break
            
            print(f"\r\033[K{VERDE}[DADOS CRIPTOGRAFADOS]: {data.hex()[:32]}...{RESET}")
            print("descriptografando.....")
            
            msg = decifrar_mensagem(data, key)
            print(f"\033[K{AMARELO}Server:{RESET} {msg}")
            print(f"Digite sua mensagem: ", end="", flush=True)
        except:
            print(f"\n{VERDE}[SISTEMA]{RESET} Conexão encerrada.")
            break

def iniciar():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))

    pub_data = client.recv(1024)
    public_key = serialization.load_pem_public_key(pub_data)
    print(f"{CIANO}[INFO]{RESET} Chave Pública do servidor recebida.")
    
    session_key = os.urandom(16)
    pacote_chave = public_key.encrypt(
        session_key, 
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    
    print(f"{VERDE}[CHAVE CRIPTOGRAFADA ENVIADA]:{RESET} {pacote_chave.hex()[:64]}...")
    client.send(pacote_chave)

    print(f"{CIANO}[SUCESSO]{RESET} Handshake concluído.")
    threading.Thread(target=receber, args=(client, session_key), daemon=True).start()
    
    while True:
        txt = input("Digite sua mensagem: ") 
        if txt.lower() == 'sair': break
        if txt.strip():
            print(f"\033[A\033[KVocê: {txt}")
            client.send(cifrar_mensagem(txt, session_key))

if __name__ == "__main__":
    iniciar()