import { fetchApi } from "@/services/http";

export async function login(email: string, password: string) {
  return fetchApi("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function register(email: string, name: string, password: string) {
  return fetchApi("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, name, password }),
  });
}

export async function updateProfile(data: { name?: string; avatar_url?: string }) {
  return fetchApi("/auth/me", {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}
