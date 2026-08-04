import { create } from "zustand";
import Cookies from "js-cookie";

interface User {
  id: string;
  name: string;
  email: string;
  avatar_url?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: typeof window !== "undefined" ? localStorage.getItem("token") : null,
  setAuth: (user, token) => {
    localStorage.setItem("token", token);
    Cookies.set("token", token, { expires: 7 }); // 7 days
    set({ user, token });
  },
  logout: () => {
    localStorage.removeItem("token");
    Cookies.remove("token");
    set({ user: null, token: null });
  },
}));
