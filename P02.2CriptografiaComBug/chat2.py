import socket
import threading
import json
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Porta padrão para a comunicação UDP. Todos os peers devem ouvir nesta porta.
numIp = 12345

class LamportClock:
    """
    Classe para implementar um relógio de Lamport.
    O relógio de Lamport é um mecanismo para determinar a ordem dos eventos em um sistema distribuído,
    essencial para manter a consistência do estado entre diferentes partes do sistema.
    """
    def __init__(self):
        # Inicializa o valor do relógio para 0.
        self.value = 0
        # Lock para garantir que as operações com o relógio sejam thread-safe.
        self.lock = threading.Lock()

    def increment(self):
        """
        Incrementa o valor do relógio.
        Isso é feito antes de um peer enviar uma mensagem, para garantir a ordem das mensagens.
        """
        with self.lock:
            self.value += 1
            return self.value

    def update(self, received_time):
        """
        Atualiza o valor do relógio com base no tempo recebido de outra mensagem.
        Isso ajuda a manter a consistência da ordem dos eventos entre diferentes peers.
        """
        with self.lock:
            self.value = max(self.value, received_time) + 1
            return self.value

# Gerador de chaves RSA para criptografia assimétrica.
def generate_keys():
    """
    Gera um par de chaves RSA - uma chave privada e uma chave pública.
    A chave pública pode ser compartilhada com outros peers para permitir que eles criptografem mensagens.
    A chave privada é mantida em segredo e usada para descriptografar mensagens recebidas.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Exponente público comum para chaves RSA.
        key_size=2048,  # Tamanho da chave. Quanto maior, mais segura, mas também mais lenta.
        backend=default_backend()  # Backend criptográfico para a geração da chave.
    )
    public_key = private_key.public_key()  # Deriva a chave pública a partir da chave privada.
    return private_key, public_key

# Serializador de chave pública.
def serialize_public_key(public_key):
    """
    Serializa a chave pública para um formato que pode ser facilmente compartilhado (PEM).
    Isso é útil para enviar a chave pública para outros peers.
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

# Funções de criptografia e descriptografia.
def encrypt_message(message, public_key):
    """
    Criptografa uma mensagem usando a chave pública de um receptor.
    Isso garante que apenas o receptor (que possui a chave privada correspondente) possa ler a mensagem.
    """
    encrypted = public_key.encrypt(
        message.encode(),  # Codifica a mensagem em bytes.
        padding.OAEP(  # Padding OAEP para a criptografia RSA.
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_message(encrypted_message, private_key):
    """
    Descriptografa uma mensagem recebida usando a chave privada do receptor.
    Isso é usado para ler mensagens que foram criptografadas com a chave pública do receptor.
    """
    original_message = private_key.decrypt(
        encrypted_message,  # Mensagem criptografada.
        padding.OAEP(  # Padding OAEP para a descriptografia RSA.
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message.decode()  # Converte a mensagem de volta para string.

# Thread para escutar mensagens.
def listen_for_messages(sock, clock, alias, my_private_key):
    """
    Thread que fica ouvindo por mensagens de outros peers.
    Quando uma mensagem é recebida, ela é descriptografada e exibida para o usuário.
    """
    while True:
        try:
                       # Recebe dados de outros usuários. 'addr' contém o endereço do remetente.
            data, addr = sock.recvfrom(1024)  
            # Desempacota a mensagem criptografada e o tempo do relógio de Lamport.
            encrypted_message, received_time = pickle.loads(data)  
            # Descriptografa a mensagem usando a chave privada.
            message_data = decrypt_message(encrypted_message, my_private_key)  
            # Converte a mensagem de JSON para um dicionário Python.
            message = json.loads(message_data)  
            # Atualiza o relógio de Lamport com base no tempo recebido.
            clock.update(received_time)  
            # Exibe a mensagem descriptografada e o tempo do relógio de Lamport.
            print(f"{message['alias']} disse: {message['text']} at Lamport time {clock.value}")
        except Exception as e:
            # Imprime qualquer erro que ocorrer durante a recepção e processamento da mensagem.
            print(f"Erro ao receber mensagem: {e}")

def send_message(sock, clock, alias, peers, my_private_key, public_keys):
    """
    Função para enviar mensagens para outros peers. A mensagem é criptografada com a chave pública do destinatário.
    """
    while True:
        # Solicita ao usuário uma mensagem para enviar.
        message_text = input("Digite sua mensagem: ")  
        # Incrementa o relógio de Lamport antes de enviar a mensagem.
        lamport_time = clock.increment()  
        # Prepara os dados da mensagem para envio, convertendo para formato JSON.
        message_data = json.dumps({"alias": alias, "text": message_text})

        # Envia a mensagem para cada um dos peers.
        for peer_alias in peers:
            # Pega a chave pública do peer destinatário.
            public_key = public_keys[peer_alias]
            # Criptografa a mensagem com a chave pública do destinatário.
            encrypted_data = encrypt_message(message_data, public_key)
            # Empacota a mensagem criptografada e o tempo do relógio para envio.
            data = pickle.dumps((encrypted_data, lamport_time))
            # Pega o endereço IP e porta do peer destinatário.
            peer_ip, peer_port = peers[peer_alias]
            # Envia a mensagem criptografada para o peer.
            sock.sendto(data, (peer_ip, peer_port))

def main():
    """
    Função principal para executar o chat.
    Configura o chat, incluindo geração de chaves, criação de socket e início das threads de escuta e envio.
    """
    # Solicita ao usuário um apelido para o chat.
    alias = input("Digite seu apelido no chat: ")

    # Gera um par de chaves RSA para o usuário (chave privada e pública).
    my_private_key, my_public_key = generate_keys()
    # Exibe a chave pública do usuário para compartilhamento com outros peers.
    print("Sua chave pública:")
    print(serialize_public_key(my_public_key).decode())

    # Dicionário para armazenar os endereços dos peers e suas chaves públicas.
    peers = {}
    public_keys = {}
    # Pede ao usuário o número de membros no chat.
    num = int(input("Digite o número de membros que terá seu chat em grupo (sem incluir você): "))
    for _ in range(num):
        # Pede informações de cada membro (apelido, IP e chave pública).
        member_alias = input("Digite o apelido do membro: ")
        ip = input("Digite o IP do membro: ")
        # Armazena o endereço IP e porta do membro no dicionário de peers.
        peers[member_alias] = (ip, numIp)

        # Pede e armazena a chave pública de cada membro.
        public_key_pem = input(f"Digite a chave pública do membro {member_alias}: ")
        # Converte a chave pública de formato PEM para um objeto de chave pública.
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        # Armazena a chave pública no dicionário de chaves públicas.
        public_keys[member_alias] = public_key

    # Configura um socket UDP para comunicação.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Associa o socket à porta especificada.
    sock.bind(('', numIp))

    # Cria uma instância do relógio de Lamport.
    clock = LamportClock()
        # Inicia uma thread para ouvir mensagens de entrada.
    listener_thread = threading.Thread(target=listen_for_messages, args=(sock, clock, alias, my_private_key), daemon=True)
    listener_thread.start()

    # Chama a função para enviar mensagens. Esta função continuará em execução e permitirá que o usuário
    # digite e envie mensagens.
    send_message(sock, clock, alias, peers, my_private_key, public_keys)

if __name__ == "__main__":
    main()  # Executa a função principal se o script for o módulo principal.
