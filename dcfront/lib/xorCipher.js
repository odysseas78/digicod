function xorBytes(dataBytes, keyBytes) {
  const result = new Uint8Array(dataBytes.length);

  for (let i = 0; i < dataBytes.length; i++) {
    result[i] = dataBytes[i] ^ keyBytes[i % keyBytes.length];
  }

  return result;
}

function bytesToBase64(bytes) {
  if (typeof Buffer !== "undefined") {
    return Buffer.from(bytes).toString("base64");
  }

  let binary = "";
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary);
}

function base64ToBytes(base64) {
  if (typeof Buffer !== "undefined") {
    return new Uint8Array(Buffer.from(base64, "base64"));
  }

  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);

  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }

  return bytes;
}

export function encrypt(inputString, key) {
  const encoder = new TextEncoder();

  const inputBytes = encoder.encode(inputString);
  const keyBytes = encoder.encode(key);

  if (keyBytes.length === 0) {
    throw new Error("Key must not be empty");
  }

  const encryptedBytes = xorBytes(inputBytes, keyBytes);
  return bytesToBase64(encryptedBytes);
}

export function decrypt(encryptedString, key) {
  const encoder = new TextEncoder();
  const decoder = new TextDecoder();

  const encryptedBytes = base64ToBytes(encryptedString);
  const keyBytes = encoder.encode(key);

  if (keyBytes.length === 0) {
    throw new Error("Key must not be empty");
  }

  const decryptedBytes = xorBytes(encryptedBytes, keyBytes);
  return decoder.decode(decryptedBytes);
}



// #####################################################
function xorCipher(inputString, key) {
  let encrypted = "";

  for (let i = 0; i < inputString.length; i++) {
    const charCode = inputString.charCodeAt(i);
    const keyCode = key.charCodeAt(i % key.length);
    encrypted += String.fromCharCode(charCode ^ keyCode);
  }

  return encrypted;
}

function encrypt2(inputString, key) {
  const encrypted = xorCipher(inputString, key);
  return Buffer.from(encrypted, "utf-8").toString("base64");
}

function decrypt2(encryptedString, key) {
  const encrypted = Buffer.from(encryptedString, "base64").toString("utf-8");
  return xorCipher(encrypted, key);
}
// #############################################################
function xorCipher3(inputString, key) {
  let encrypted = "";

  for (let i = 0; i < inputString.length; i++) {
    const charCode = inputString.charCodeAt(i);
    const keyCode = key.charCodeAt(i % key.length);
    encrypted += String.fromCharCode(charCode ^ keyCode);
  }

  return encrypted;
}

function encrypt3(inputString, key) {
  const encrypted = xorCipher3(inputString, key);
  return btoa(encrypted);
}

function decrypt3(encryptedString, key) {
  const encrypted = atob(encryptedString);
  return xorCipher3(encrypted, key);
}
