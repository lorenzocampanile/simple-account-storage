import { STATUS_CODES, sendHttpReq } from "./httpreq";

export async function login(username, password) {
  let response = await sendHttpReq('POST', '/api/v1/accounts/login/', {
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
