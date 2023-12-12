def generate_key():
    return Fernet.generate_key()

def encrypt_message(key, message):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(key, encrypted_message):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()