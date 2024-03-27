export const STATUS_CODES = {
  OK: 200,
  OK_CREATED: 201,
  UNAUTHENTICATED: 401,
  PAYLOAD_ERROR: 400,
  NO_CONTENT: 204,
}


export async function readCsrfToken() {
  let name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }

  return cookieValue;
}


export async function getCsrfToken() {
  let cookieValue = readCsrfToken();

  if (cookieValue === null) {
    await fetch(`${import.meta.env.VITE_BASE_API_URL}/api/csrf/`, {credentials: "include"});
    cookieValue = readCsrfToken();
  }

  return cookieValue;
}


export async function sendHttpReq(method, url, params, contentType = 'application/json') {
  let headers = {
    'Content-Type': contentType,
    'X-CSRFToken': await getCsrfToken(),
    'X-Encryption-Key': sessionStorage.getItem('encryptionKey'),
  }

  let reqBody = '';
  if (method.toUpperCase() === 'GET') {
    let encodedParams = new URLSearchParams(params).toString();
    url = `${url}?${encodedParams}`;
  } else {
    if (contentType == 'application/json') {
      reqBody = JSON.stringify(params);
    }
    if (contentType == 'application/x-www-form-urlencoded') {
      reqBody = new URLSearchParams(params).toString();
    }
  }

  let reqParams = {
    method: method,
    headers: headers,
    credentials: "include"
  };
  if (method.toUpperCase() !== 'GET')
    reqParams['body'] = reqBody;
  return await fetch(`${import.meta.env.VITE_BASE_API_URL}${url}`, reqParams);
}