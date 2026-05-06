import os
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def cifrar_mensagem(mensagem, chave_sessao):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(chave_sessao), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    pad_len = 16 - (len(mensagem) % 16)
    padded_msg = mensagem.encode() + bytes([pad_len] * pad_len)
    ciphertext = encryptor.update(padded_msg) + encryptor.finalize()

    h = hmac.HMAC(chave_sessao, hashes.SHA256())
    h.update(iv + ciphertext)
    tag = h.finalize()
    
    return iv + tag + ciphertext

def decifrar_mensagem(dados, chave_sessao):
    iv = dados[:16]
    received_hmac = dados[16:48]
    ciphertext = dados[48:]

    h = hmac.HMAC(chave_sessao, hashes.SHA256())
    h.update(iv + ciphertext)
    h.verify(received_hmac) # Levanta exceção se adulterado

    cipher = Cipher(algorithms.AES(chave_sessao), modes.CBC(iv))
    decryptor = cipher.decryptor()
    msg_padded = decryptor.update(ciphertext) + decryptor.finalize()
    
    padding_len = msg_padded[-1]
    return msg_padded[:-padding_len].decode()