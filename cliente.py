import socket, threading, os, tkinter as tk
from tkinter import scrolledtext
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from criptografia import cifrar_mensagem, decifrar_mensagem

class ClienteGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cliente - Chat Seguro Atitus")
        self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled', height=20, width=50)
        self.chat_area.pack(padx=10, pady=10)
        
        self.msg_entry = tk.Entry(self.root, width=40)
        self.msg_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.msg_entry.bind("<Return>", lambda e: self.enviar())
        
        self.send_btn = tk.Button(self.root, text="Enviar", command=self.enviar)
        self.send_btn.pack(side=tk.RIGHT, padx=10)

        self.session_key = os.urandom(16) # AES-128 bits [cite: 26]
        self.client = None

        threading.Thread(target=self.conectar, daemon=True).start()
        self.root.mainloop()

    def log(self, texto, cor="black"):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, texto + "\n", cor)
        self.chat_area.tag_config("verde", foreground="green")
        self.chat_area.tag_config("laranja", foreground="orange")
        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')

    def conectar(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('localhost', 5000))
            pub_data = self.client.recv(1024)
            public_key = serialization.load_pem_public_key(pub_data)
            
            pacote_chave = public_key.encrypt(
                self.session_key, 
                padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            self.client.send(pacote_chave)
            self.log("[SUCESSO] Conectado e Seguro.", "verde")
            
            while True:
                data = self.client.recv(1024)
                if not data: break
                msg = decifrar_mensagem(data, self.session_key)
                self.log(f"Server: {msg}")
        except:
            self.log("[ERRO] Falha na conexão.", "verde")

    def enviar(self):
        txt = self.msg_entry.get()
        if txt and self.client:
            self.log(f"Você: {txt}", "laranja")
            self.client.send(cifrar_mensagem(txt, self.session_key))
            self.msg_entry.delete(0, tk.END)

if __name__ == "__main__":
    ClienteGUI()