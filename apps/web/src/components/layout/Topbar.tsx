"use client";

import { useAuthStore } from "@/store/authStore";
import { useRouter } from "next/navigation";
import Link from "next/link";

export function Topbar() {
  const logout = useAuthStore((state) => state.logout);
  const user = useAuthStore((state) => state.user);
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
        <Link href="/notifications" className="text-neutral-400 hover:text-white transition-colors relative">
          <span className="w-5 h-5 block border-2 border-current rounded-full" />
          <span className="absolute top-0 right-0 w-2 h-2 bg-indigo-500 rounded-full" />
        </Link>
        <Link href="/settings" className="flex items-center gap-2 ml-4 group">
          <div className="w-8 h-8 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-sm overflow-hidden border border-neutral-800 group-hover:border-indigo-500/50 transition-colors">
            {user?.avatar_url ? (
              <img src={user.avatar_url} alt="Profile" className="w-full h-full object-cover" />
            ) : (
              user?.name?.charAt(0) || "U"
            )}
          </div>
          <span className="text-sm font-medium text-neutral-300 group-hover:text-white transition-colors hidden sm:block">
            {user?.name || "User"}
          </span>
        </Link>
        <div className="w-px h-6 bg-neutral-800 mx-2" />
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
