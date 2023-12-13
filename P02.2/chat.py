import socket
import threading
import json
import pickle

numIp = 12345  # Porta padrão usada para a comunicação UDP.

class LamportClock:
    """ Classe para implementar um relógio de Lamport.
    O relógio de Lamport é uma maneira simples de ordenar eventos em um sistema distribuído. """
    def __init__(self):
        self.value = 0  # Valor inicial do relógio.
        self.lock = threading.Lock()  # Lock para sincronização em ambientes multithread.

    def increment(self):
        """ Incrementa o valor do relógio e retorna o novo valor. """
        with self.lock:
            self.value += 1
            return self.value

    def update(self, received_time):
        """ Atualiza o relógio com base no tempo recebido de outra mensagem. """
        with self.lock:
            self.value = max(self.value, received_time) + 1
            return self.value

def listen_for_messages(sock, clock, alias):
    """ Função para ouvir mensagens de outros usuários do chat. """
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # Recebe dados de outros usuários.
            message, received_time = pickle.loads(data)  # Desempacota a mensagem e o tempo recebido.
            clock.update(received_time)  # Atualiza o relógio com base no tempo recebido.
            # Exibe a mensagem recebida.
            print(f"{message['alias']} disse: {message['text']} at Lamport time {clock.value}")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

def send_message(sock, clock, alias, peers):
    """ Função para enviar mensagens para outros usuários. """
    while True:
        message_text = input("Digite sua mensagem: ")  # Solicita ao usuário uma mensagem para enviar.
        lamport_time = clock.increment()  # Incrementa o relógio antes de enviar a mensagem.
        # Prepara os dados da mensagem para envio.
        message_data = json.dumps({"alias": alias, "text": message_text})
        data = pickle.dumps((message_data, lamport_time))
        # Envia a mensagem para todos os peers (outros usuários) do chat.
        for peer in peers:
            sock.sendto(data, peer)

def main():
    """ Função principal para executar o chat. """
    
    alias = input("Digite seu apelido no chat: ")  # Solicita ao usuário um apelido para o chat.

    # Lista para armazenar os endereços IP dos outros membros do chat.
    peers = []
    num = int(input("Digite o número de membros que terá seu chat em grupo (sem incluir você): "))
    for _ in range(num):
        ip = input("Digite o IP do membro: ")  # Pede o IP de cada membro do chat.
        peers.append((ip, numIp))  # Adiciona o IP e a porta à lista de peers.

    # Configura o socket para comunicação UDP.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', numIp))  # Associa o socket à porta definida.

    clock = LamportClock()  # Cria uma instância do relógio de Lamport.

    # Cria e inicia uma thread para ouvir mensagens.
    listener_thread = threading.Thread(target=listen_for_messages, args=(sock, clock, alias), daemon=True)
    listener_thread.start()

    send_message(sock, clock, alias, peers)  # Chama a função para enviar mensagens.

if __name__ == "__main__":
    main()  # Executa a função principal se o script for o módulo principal.
