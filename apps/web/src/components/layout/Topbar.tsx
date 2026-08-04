"use client";

import { useAuthStore } from "@/store/authStore";
import { useRouter } from "next/navigation";

export function Topbar() {
  const logout = useAuthStore((state) => state.logout);
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <header className="h-16 bg-neutral-900 border-b border-neutral-800 flex items-center justify-between px-6 sticky top-0 z-10 md:ml-64">
      <div className="flex items-center md:hidden">
        <span className="text-xl font-bold text-white tracking-tight">Scriptora</span>
      </div>
      
      <div className="flex-1 md:hidden"></div>

      <div className="flex items-center gap-4 ml-auto">
        <button className="text-neutral-400 hover:text-white transition-colors relative">
          {/* Notification bell icon placeholder */}
          <span className="w-5 h-5 block border-2 border-current rounded-full" />
          <span className="absolute top-0 right-0 w-2 h-2 bg-indigo-500 rounded-full" />
        </button>
        <button
          onClick={handleLogout}
          className="text-sm font-medium text-neutral-400 hover:text-white transition-colors"
        >
          Logout
        </button>
      </div>
    </header>
  );
}
