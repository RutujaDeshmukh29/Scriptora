import { fetchApi } from "./api-client";

export async function login(email: string, password: string) {
  return fetchApi("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function register(email: string, full_name: string, password: string) {
  return fetchApi("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, full_name, password }),
  });
}
