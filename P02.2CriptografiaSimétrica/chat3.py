import socket
import threading
import json
import pickle
import re
import hashlib
import base64
from cryptography.fernet import Fernet

# Define a porta padrão para a comunicação UDP.
numIp = 12345

class LamportClock:
    """
    Classe que implementa um relógio de Lamport, usado para estabelecer uma ordem de eventos
    em um sistema distribuído, crucial para a consistência de estado entre diferentes nós.
    """
    def __init__(self):
        # Valor inicial do relógio.
        self.value = 0
        # Lock para sincronização em ambientes multithread.
        self.lock = threading.Lock()

    def increment(self):
        """
        Incrementa o valor do relógio. Isso é feito antes de um nó enviar uma mensagem,
        para assegurar a ordem das mensagens.
        """
        with self.lock:
            self.value += 1
            return self.value

    def update(self, received_time):
        """
        Atualiza o relógio com o maior valor entre o atual e o recebido, e incrementa em 1.
        Isso ajuda a manter a consistência da ordem dos eventos entre diferentes nós.
        """
        with self.lock:
            self.value = max(self.value, received_time) + 1
            return self.value

def validate_key(key):
    """
    Valida se a chave de criptografia fornecida pelo usuário atende aos requisitos mínimos.
    Isso inclui ter pelo menos 8 caracteres, com letras maiúsculas e minúsculas, números e
    caracteres especiais.
    """
    if (len(key) >= 8 and
        re.search("[a-z]", key) and
        re.search("[A-Z]", key) and
        re.search("[0-9]", key) and
        re.search("[!@#$%^&*(),.<>/?]", key)):
        return True
    return False

def generate_fernet_key_from_input(input_key):
    """
    Gera uma chave Fernet válida a partir da entrada do usuário. Isso é feito usando
    um hash SHA-256 da entrada, que é então codificado em base64.
    """
    hash_key = hashlib.sha256(input_key.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(hash_key)
    return fernet_key

def encrypt_message(key, message):
    """
    Criptografa uma mensagem usando a chave Fernet.
    Isso garante que apenas pessoas com a chave correta possam ler a mensagem.
    """
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(key, encrypted_message):
    """
    Descriptografa uma mensagem usando a chave Fernet.
    Isso é usado para ler mensagens que foram criptografadas com a mesma chave.
    """
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def listen_for_messages(sock, clock, alias, key):
    """
    Thread que fica ouvindo por mensagens de outros usuários.
    Quando uma mensagem é recebida, ela é descriptografada e exibida para o usuário.
    """
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # Recebe dados de outros usuários.
            encrypted_message, received_time = pickle.loads(data)  # Desempacota e descriptografa a mensagem.
            decrypted_message = decrypt_message(key, encrypted_message)
            message = json.loads(decrypted_message)  # Converte a mensagem de JSON para um dicionário Python.
            clock.update(received_time)  # Atualiza o relógio de Lamport com o tempo recebido.
            print(f"{message['alias']} disse: {message['text']}")  # Exibe a mensagem.
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

def send_message(sock, clock, alias, peers, key):
    """
    Função para enviar mensagens para outros usuários. As mensagens são criptografadas antes do envio.
    """
    while True:
        message_text = input("Digite sua mensagem: ")  # Solicita uma mensagem do usuário.
        lamport_time = clock.increment()  # Incrementa o relógio de Lamport.
        message_data = json.dumps({"alias": alias, "text": message_text})  # Prepara a mensagem.
        encrypted_data = encrypt_message(key, message_data)  # Criptografa a mensagem.
        data = pickle.dumps((encrypted_data, lamport_time))  # Empacota a mensagem para envio

        for peer in peers:
            # Envia a mensagem criptografada para cada peer na lista.
            sock.sendto(data, peer)

def main():
    """
    Função principal para executar o chat.
    Configura o chat, incluindo validação de chave, criação de socket e início das threads de escuta e envio.
    """
    # Solicita ao usuário um apelido para o chat.
    alias = input("Digite seu apelido no chat: ")

    # Loop para obter uma chave de criptografia válida do usuário.
    while True:
        key_input = input("Digite uma chave de segurança (mínimo de 8 caracteres, incluindo letras, números e símbolos): ")
        if validate_key(key_input):
            break
        else:
            print("Chave inválida. Por favor, siga o formato solicitado.")

    # Gera uma chave Fernet válida a partir da entrada do usuário.
    key = generate_fernet_key_from_input(key_input)

    # Lista para armazenar os endereços IP dos outros membros do chat.
    peers = []
    # Pede ao usuário o número de membros no chat.
    num = int(input("Digite o número de membros que terá seu chat em grupo (sem incluir você): "))
    for _ in range(num):
        # Pede o IP de cada membro do chat.
        ip = input("Digite o IP do membro: ")
        # Adiciona o IP e a porta à lista de peers.
        peers.append((ip, numIp))

    # Imprime uma linha em branco para separar a configuração da interação do chat.
    print("\n")
    # Configura um socket UDP para comunicação.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Associa o socket à porta especificada.
    sock.bind(('', numIp))

    # Cria uma instância do relógio de Lamport.
    clock = LamportClock()
    
    # Inicia uma thread para ouvir mensagens de entrada.
    listener_thread = threading.Thread(target=listen_for_messages, args=(sock, clock, alias, key), daemon=True)
    listener_thread.start()

    # Chama a função para enviar mensagens. Esta função continuará em execução e permitirá que o usuário
    # digite e envie mensagens.
    send_message(sock, clock, alias, peers, key)

if __name__ == "__main__":
    main()  # Executa a função principal se o script for o módulo principal.