import router from "@/router";
import { STATUS_CODES, sendHttpReq } from "./httpreq";
import CryptoJS from 'crypto-js';

export async function login(username, password) {
  let loginResponse = await sendHttpReq('POST', '/api/v1/auth/login/', {
    'login': username,
    'password': password,
  });
  if (loginResponse.status === STATUS_CODES.OK) {
    // Fetch the account keys
    let keyResponse = await sendHttpReq('GET', '/api/v1/auth/encryption-keys/');
    let keyResponseData = await keyResponse.json();

    // Decrypt and store the private key
    let privateKey = CryptoJS.AES.decrypt(keyResponseData['encrypted_private_key'], password).toString(CryptoJS.enc.Utf8);
    sessionStorage.setItem('privateKey', privateKey);

    // Store the public key
    let publicKey = keyResponseData['public_key']
    sessionStorage.setItem('publicKey', publicKey);
  }

  return loginResponse;
}

export async function logout() {
  let response = await sendHttpReq('POST', '/api/v1/auth/logout/', {});
  if (response.status === STATUS_CODES.OK) {
    sessionStorage.removeItem('privateKey');
    sessionStorage.removeItem('publicKey');
    router.push('/login');
  }
}

export function isUserAuthenticated() {
  let key = sessionStorage.getItem('privateKey');
  if (key) {
    return true;
  }

  return false;
}
