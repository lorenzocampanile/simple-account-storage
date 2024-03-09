export const STATUS_CODES = {
  OK: 200,
  OK_CREATED: 201,
  UNAUTHENTICATED: 401,
  PAYLOAD_ERROR: 400,
}

export async function getCsrfToken() {
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
          } else {
            // In order to have the CSRF token cookie available, I need to call a GET API
            // TODO: Use another endpoint
            await fetch(`${import.meta.env.VITE_BASE_API_URL}/auth/login/`);
            cookieValue = getCsrfToken();
          }
      }
  }
  return cookieValue;
}

export async function sendHttpReq(method, url, params, contentType = 'application/json') {
  let headers = {
    'Content-Type': contentType,
    'X-CSRFToken': await getCsrfToken(),
  }

  let reqBody = '';
  if (method.toUpperCase() === 'GET') {
    let encodedParams = new URLSearchParams(params).toString();
    url = `${url}/?${encodedParams}`;
  } else {
    if (contentType == 'application/json') {
      reqBody = JSON.stringify(params);
    }
    if (contentType == 'application/x-www-form-urlencoded') {
      reqBody = new URLSearchParams(params).toString();
    }
  }

  return await fetch(`${import.meta.env.VITE_BASE_API_URL}${url}`, {
    method: method,
    headers: headers,
    body: reqBody,
    credentials: "include"
  });
}