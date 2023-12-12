import socket
import threading
import json
import pickle
from cryptography.fernet import Fernet

numIp = 12345
class LamportClock:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

    def update(self, received_time):
        with self.lock:
            self.value = max(self.value, received_time) + 1
            return self.value
    
def generate_key():
    return Fernet.generate_key()

def encrypt_message(key, message):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(key, encrypted_message):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def listen_for_messages(sock, clock, alias, key):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print("oiiiii")
            encrypted_message, received_time = pickle.loads(data)
            print("oi", encrypt_message)
            decrypted_message = decrypt_message(key, encrypted_message)
            print("oi", decrypted_message)
            message = json.loads(decrypted_message)
            print("oi2")
            clock.update(received_time)
            print("oi")
            print(f"{message['alias']} disse: {message['text']} at Lamport time {clock.value}")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

def send_message(sock, clock, alias, peers, key):
    while True:
        message_text = input("Digite sua mensagem: ")
        lamport_time = clock.increment()
        message_data = json.dumps({"alias": alias, "text": message_text})
        encrypted_data = encrypt_message(key, message_data)
        data = pickle.dumps((encrypted_data, lamport_time))
        for peer in peers:
            sock.sendto(data, peer)

def main():

    alias = input("Digite seu apelido no chat: ")

    peers = []
    num = int(input("Digite o número de membros que terá seu chat em grupo (sem incluir você): "))
    for _ in range(num):
        ip = input("Digite o IP do membro: ")
        peers.append((ip, numIp))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', numIp))

    clock = LamportClock()

    key = generate_key()
    print("Key ", key)

    listener_thread = threading.Thread(target=listen_for_messages, args=(sock, clock, alias, key), daemon=True)
    listener_thread.start()

    send_message(sock, clock, alias, peers, key)

if __name__ == "__main__":
    main()