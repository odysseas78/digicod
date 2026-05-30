from nacl.public import PrivateKey, PublicKey, SealedBox
import base64


def generate_keypair():
    private_key = PrivateKey.generate()
    public_key = private_key.public_key

    return {
        "private_key": base64.b64encode(bytes(private_key)).decode(),
        "public_key": base64.b64encode(bytes(public_key)).decode(),
    }


def encrypt_with_public_key(message: str, public_key_b64: str) -> str:
    public_key = PublicKey(base64.b64decode(public_key_b64))
    box = SealedBox(public_key)

    encrypted = box.encrypt(message.encode("utf-8"))

    return base64.b64encode(encrypted).decode()


def decrypt_with_private_key(encrypted_b64: str, private_key_b64: str) -> str:
    private_key = PrivateKey(base64.b64decode(private_key_b64))
    box = SealedBox(private_key)

    decrypted = box.decrypt(base64.b64decode(encrypted_b64))

    return decrypted.decode("utf-8")


# keys = generate_keypair()

# message = "Hallo geheime Nachricht"

# encrypted = encrypt_with_public_key(message, keys["public_key"])
# decrypted = decrypt_with_private_key(encrypted, keys["private_key"])

# print("Private:", keys["private_key"])
# print("Public:", keys["public_key"])
# print("Encrypted:", encrypted)
# print("Decrypted:", decrypted)