"use client";

import { useAuthStore } from "@/store/authStore";
import { UserCircle } from "lucide-react";

export default function ProfilePage() {
  const user = useAuthStore(state => state.user);

  return (
    <div className="p-8 max-w-4xl mx-auto w-full">
      <header className="mb-8 border-b border-neutral-800 pb-4">
        <h1 className="text-3xl font-bold text-white">Profile Settings</h1>
        <p className="text-neutral-400 mt-2">Manage your account and preferences.</p>
      </header>

      <div className="bg-neutral-900 border border-neutral-800 rounded-xl overflow-hidden">
        <div className="p-8 border-b border-neutral-800">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 bg-indigo-500/20 rounded-full flex items-center justify-center border-4 border-neutral-950">
              {user?.avatar_url ? (
                <img src={user.avatar_url} alt={user.name} className="w-full h-full rounded-full object-cover" />
              ) : (
                <UserCircle className="w-12 h-12 text-indigo-400" />
              )}
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">{user?.name || "User"}</h2>
              <p className="text-neutral-400">{user?.email}</p>
            </div>
          </div>
        </div>
        
        <div className="p-8">
          <h3 className="text-lg font-semibold text-white mb-4">Account Information</h3>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-b border-neutral-800 pb-4">
              <div className="text-sm font-medium text-neutral-400">Full Name</div>
              <div className="md:col-span-2 text-sm text-white">{user?.name}</div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-b border-neutral-800 pb-4">
              <div className="text-sm font-medium text-neutral-400">Email Address</div>
              <div className="md:col-span-2 text-sm text-white">{user?.email}</div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pb-2">
              <div className="text-sm font-medium text-neutral-400">Password</div>
              <div className="md:col-span-2 text-sm text-white">
                <button className="text-indigo-400 hover:text-indigo-300 transition-colors">Change password</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
