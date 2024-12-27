const BASE_URL = import.meta.env.VITE_BASE_BACKEND_URL;

/**
 * apiFetch is a wrapper around fetch to get data from te backend.
 * It handles authentication by using the user token stored in local
 * storage during the login process. If the token expired, it is refreshed
 * and the query is retried.
 * @param path URL path
 * @param withAuth if true add the user authentication header
 */
export default async function apiFetch(
  path: string,
  init?: RequestInit,
  withAuth: boolean = false
): Promise<Response> {
  const fullUrl = `${BASE_URL}${path}`;

  if (!withAuth) return await fetch(fullUrl, init);

  let response = await fetchWithAuth(fullUrl, init);

  // If the token has expired, we need to use our refresh token
  // to obtain a new token
  if (response.status === 401) {
    const refresh = getRefreshTokenFromStorage();
    if (refresh === null) {
      // redirect to login page if we have no token
      return Promise.reject("Not authenticated");
    }
    await refreshToken();
    // We replay the request
    response = await fetchWithAuth(fullUrl, init);
  }

  return response;
}

async function fetchWithAuth(
  input: RequestInfo | URL,
  init?: RequestInit
): Promise<Response> {
  // Add auth header to the request
  const token = getTokenFromStorage();
  if (token === null) {
    // redirect to login page if we have no token
    return Promise.reject("Not authenticated");
  }
  return fetch(input, addAuth(token, init));
}

function addAuth(token: string, init?: RequestInit): RequestInit {
  const headersWithAuth = new Headers(init?.headers);
  headersWithAuth.set("Authorization", `Bearer ${token}`);
  return {
    ...init,
    headers: headersWithAuth,
  };
}

function getRefreshTokenFromStorage() {
  return localStorage.getItem("refreshToken");
}

type refreshTokenResponse = {
  data: { access: string };
  errors?: Array<{ message: string }>;
};

async function refreshToken() {
  const refresh = localStorage.getItem("refreshToken");
  const response = await fetch(`${BASE_URL}api/token/refresh/`, {
    method: "POST",
    body: JSON.stringify({ refresh }),
  });
  if (!response.ok) {
    throw new Error(`Cannot refresh token: ${response.body}`);
  }
  const { data, errors }: refreshTokenResponse = await response.json();
  if (errors) throw errors;

  // Save JWT token in session storage
  localStorage.setItem("jwtToken", data.access);
}

function getTokenFromStorage() {
  return localStorage.getItem("jwtToken");
}
