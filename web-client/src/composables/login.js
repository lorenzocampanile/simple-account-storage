import router from "@/router";
import { STATUS_CODES, sendHttpReq } from "./httpreq";

export async function login(username, password) {
  let response = await sendHttpReq('POST', '/api/v1/auth/login/', {
    'login': username,
    'password': password,
  });

  // Set the password as the encryption key to use
  sessionStorage.removeItem('encryptionKey');
  if (response.status === STATUS_CODES.OK) {
    sessionStorage.setItem('encryptionKey', password);
  }

  return response;
}

export async function logout() {
  let response = await sendHttpReq('POST', '/api/v1/auth/logout/', {});
  if (response.status === STATUS_CODES.OK) {
    router.push('/login');
  }

  sessionStorage.removeItem('encryptionKey');
}

export function isUserAuthenticated() {
  let key = sessionStorage.getItem('encryptionKey');
  if (key) {
    return true;
  }

  return false;
}
