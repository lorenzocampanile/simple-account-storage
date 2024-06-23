let arrayBufferToBase64 = function (buffer) {
  let binary = '';

  let bytes = new Uint8Array(buffer);
  let len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
      binary += String.fromCharCode( bytes[ i ] );
  }
  return window.btoa(binary);
}

let base64ToArrayBuffer = function(base64text) {
  let bytesArray = [];

  let binary = window.atob(base64text);
  let len = binary.length;
  for (let i = 0; i < len; i++) {
    bytesArray.push(binary[i].charCodeAt(0));
  }

  return Uint8Array.from(bytesArray).buffer;
}

export const encryptPassword = async function(plainTextPassword) {
  // Import the public key
  let publicKey = await window.crypto.subtle.importKey(
    "jwk",
    JSON.parse(sessionStorage.getItem('publicKey')),
    {
      name: "RSA-OAEP",
      hash: {name: "SHA-256"}
    },
    true,
    ['encrypt']
  );

  // Encrypt the password
  let textEncoder = new TextEncoder();
  let encryptedPassword = await window.crypto.subtle.encrypt(
    {
      name: "RSA-OAEP",
    },
    publicKey,
    textEncoder.encode(plainTextPassword),
  );


  // Return the encrypted password, encoded in base64
  return arrayBufferToBase64(encryptedPassword);
}

export const decryptPassword = async function(encryptedPassword) {
  // Import the private key
  let privateKey = await window.crypto.subtle.importKey(
    "jwk",
    JSON.parse(sessionStorage.getItem('privateKey')),
    {
      name: "RSA-OAEP",
      hash: {name: "SHA-256"}
    },
    true,
    ['decrypt']
  );

  // Decode the base64
  let encryptedDecodedPassword = base64ToArrayBuffer(encryptedPassword);

  // Decrypt the password
  let decryptedPassword = await window.crypto.subtle.decrypt(
    {
      name: "RSA-OAEP",
    },
    privateKey,
    encryptedDecodedPassword,
  );

  // Return the plain text decrypted password
  let textDecoder = new TextDecoder();
  return textDecoder.decode(decryptedPassword);
}