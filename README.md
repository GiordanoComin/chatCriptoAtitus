# chatCriptoAtitus
Giordano Paulo Comin - 1131168

Ambos os codigos devem ser executados em computadores via terminal
Requisitos:
Python
Bibliteca: cryptography

Em caso de uso em mais de um computador: Atualizar o endereço o ip do server no codigo cliente.
-----------------------------------------------------------------------------------------
Descrição dos Algoritmos Utilizados:
- RSA (Criptografia Assimétrica):
    Utilizado para o handshake seguro e a troca de chaves de sessão. 
    Por que utilizado: O RSA permite que o servidor envie uma chave pública para que o cliente cifre a "chave de sessão". Isso garante que a chave simétrica nunca        viaje em texto claro pela rede

- AES-128 (Criptografia Simétrica):
    Utilizado para cifrar o conteúdo de todas as mensagens trocadas no chat.
    Por que utilizado: O AES com chave de 128 bits é o padrão exigido para garantir que terceiros não autorizados leiam as conversas. Ele é altamente eficiente        para comunicação em tempo real.

- HMAC-SHA256 (Autenticação de Mensagem):
    Utilizado para garantir a integridade de cada pacote enviado.
    Por que utilizamos: O HMAC gera um código de autenticação baseado na mensagem e na chave secreta. Caso qualquer bit da mensagem seja alterado durante a            transmissão, o sistema detecta a falha e exibe um alerta de mensagem adulterada.  


