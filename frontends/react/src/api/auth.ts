import apiFetch from "./apiFetch";

type loginResponse = {
  data: {
    access: string;
    refresh: string;
  };
  errors?: Array<{ message: string }>;
};

export async function login(username: string, password: string) {
  const response = await apiFetch("login/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  if (!response.ok) {
    throw new Error(`Cannot login: ${response.body}`);
  }
  const { data, errors }: loginResponse = await response.json();
  if (errors) throw errors;

  // Save JWT token in session storage
  localStorage.setItem("jwtToken", data.access);
}
