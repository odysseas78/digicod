import sodium from "libsodium-wrappers";

function toBase64(bytes) {
  return sodium.to_base64(bytes, sodium.base64_variants.ORIGINAL);
}

function fromBase64(text) {
  return sodium.from_base64(text, sodium.base64_variants.ORIGINAL);
}

async function generateKeypair() {
  await sodium.ready;

  const keypair = sodium.crypto_box_keypair();

  return {
    privateKey: toBase64(keypair.privateKey),
    publicKey: toBase64(keypair.publicKey),
  };
}

export async function encryptWithPublicKey(message, publicKeyBase64) {
  await sodium.ready;

  const publicKey = fromBase64(publicKeyBase64);

  const encrypted = sodium.crypto_box_seal(
    sodium.from_string(message),
    publicKey
  );

  return toBase64(encrypted);
}

async function decryptWithPrivateKey(encryptedBase64, publicKeyBase64, privateKeyBase64) {
  await sodium.ready;

  const encrypted = fromBase64(encryptedBase64);
  const publicKey = fromBase64(publicKeyBase64);
  const privateKey = fromBase64(privateKeyBase64);

  const decrypted = sodium.crypto_box_seal_open(
    encrypted,
    publicKey,
    privateKey
  );

  return sodium.to_string(decrypted);
}

// Test
const keys = await generateKeypair();

const message = "Hallo geheime Nachricht";

const encrypted = await encryptWithPublicKey(message, keys.publicKey);

const decrypted = await decryptWithPrivateKey(
  encrypted,
  keys.publicKey,
  keys.privateKey
);

