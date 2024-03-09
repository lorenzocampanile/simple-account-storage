import { STATUS_CODES, sendHttpReq } from "./httpreq";

export async function login(username, password) {
  let response = await sendHttpReq('POST', '/auth/v2/login/', {
    'username': username,
    'password': password,
  }, 'application/x-www-form-urlencoded');

  // Set the password as the encryption key to use
  sessionStorage.removeItem('encryptionKey');
  if (response.status === STATUS_CODES.OK) {
    sessionStorage.setItem('encryptionKey', password);
  }

  return response;
}
