import socket
import threading
import json
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

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

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def encrypt_message(message, public_key):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_message(encrypted_message, private_key):
    original_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message.decode()

def listen_for_messages(sock, clock, alias, my_private_key):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            encrypted_message, received_time = pickle.loads(data)
            message_data = decrypt_message(encrypted_message, my_private_key)
            message = json.loads(message_data)
            clock.update(received_time)
            print(f"{message['alias']} disse: {message['text']} at Lamport time {clock.value}")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

def send_message(sock, clock, alias, peers, my_private_key, public_keys):
    while True:
        message_text = input("Digite sua mensagem: ")
        lamport_time = clock.increment()
        message_data = json.dumps({"alias": alias, "text": message_text})

        for peer_alias in peers:
            public_key = public_keys[peer_alias]
            encrypted_data = encrypt_message(message_data, public_key)
            data = pickle.dumps((encrypted_data, lamport_time))
            peer_ip, peer_port = peers[peer_alias]
            sock.sendto(data, (peer_ip, peer_port))

def main():
    my_port = int(input("Digite sua porta: "))
    alias = input("Digite seu apelido no chat: ")

    my_private_key, my_public_key = generate_keys()
    print("Sua chave pública:")
    print(serialize_public_key(my_public_key).decode())

    peers = {}
    public_keys = {}
    num = int(input("Digite o número de membros que terá seu chat em grupo (sem incluir você): "))
    for _ in range(num):
        member_alias = input("Digite o apelido do membro: ")
        ip = input("Digite o IP do membro: ")
        port = int(input("Digite a porta do membro: "))
        peers[member_alias] = (ip, port)

        public_key_pem = input(f"Digite a chave pública do membro {member_alias}: ")
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        public_keys[member_alias] = public_key

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', my_port))

    clock = LamportClock()

    listener_thread = threading.Thread(target=listen_for_messages, args=(sock, clock, alias, my_private_key), daemon=True)
    listener_thread.start()

    send_message(sock, clock, alias, peers, my_private_key, public_keys)

if __name__ == "__main__":
    main()
