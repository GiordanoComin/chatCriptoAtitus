import socket, threading, os, tkinter as tk
from tkinter import scrolledtext
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from criptografia import decifrar_mensagem, cifrar_mensagem

class ServidorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Servidor - Chat Seguro Atitus")
        self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled', height=20, width=50)
        self.chat_area.pack(padx=10, pady=10)
        
        self.msg_entry = tk.Entry(self.root, width=40)
        self.msg_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.msg_entry.bind("<Return>", lambda e: self.enviar())
        
        self.send_btn = tk.Button(self.root, text="Enviar", command=self.enviar)
        self.send_btn.pack(side=tk.RIGHT, padx=10)

        # Configuração de Criptografia [cite: 17, 26]
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.pem_public = self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.session_key = None
        self.conn = None

        threading.Thread(target=self.configurar_rede, daemon=True).start()
        self.root.mainloop()

    def log(self, texto, cor="black"):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, texto + "\n", cor)
        self.chat_area.tag_config("verde", foreground="green")
        self.chat_area.tag_config("azul", foreground="blue")
        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')

    def configurar_rede(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 5000))
        server.listen(1)
        self.log("Aguardando conexão do cliente...", "verde")
        
        self.conn, addr = server.accept()
        self.conn.send(self.pem_public) # Envia chave pública [cite: 25]
        
        pacote_chave = self.conn.recv(256)
        self.log(f"[CHAVE RECEBIDA]: {pacote_chave.hex()[:32]}...", "verde")
        
        self.session_key = self.private_key.decrypt(
            pacote_chave, 
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        self.log("[SUCESSO] Handshake concluído.", "verde")
        
        while True:
            try:
                data = self.conn.recv(1024)
                if not data: break
                msg = decifrar_mensagem(data, self.session_key) # [cite: 27]
                self.log(f"Cliente: {msg}")
            except:
                self.log("[ALERTA] Erro de integridade!", "verde") # [cite: 28]
                break

    def enviar(self):
        txt = self.msg_entry.get()
        if txt and self.conn:
            self.log(f"Você: {txt}", "azul")
            self.conn.send(cifrar_mensagem(txt, self.session_key))
            self.msg_entry.delete(0, tk.END)

if __name__ == "__main__":
    ServidorGUI()