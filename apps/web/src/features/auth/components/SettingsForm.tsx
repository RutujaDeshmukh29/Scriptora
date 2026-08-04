"use client";

import { useState, useEffect } from "react";
import { useAuthStore } from "@/store/authStore";
import { updateProfile } from "../api";
import { UserCircle, Camera, CheckCircle2 } from "lucide-react";

export function SettingsForm() {
  const user = useAuthStore(state => state.user);
  const updateUser = useAuthStore(state => state.updateUser);
  
  const [name, setName] = useState("");
  const [avatarUrl, setAvatarUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (user) {
      setName(user.name || "");
      setAvatarUrl(user.avatar_url || "");
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setStatus("idle");
    setErrorMessage("");

    try {
      const data = await updateProfile({ name, avatar_url: avatarUrl });
      updateUser({ name: data.name, avatar_url: data.avatar_url });
      setStatus("success");
      setTimeout(() => setStatus("idle"), 3000);
    } catch (err: any) {
      setStatus("error");
      setErrorMessage(err.message || "Failed to update profile");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* Profile Photo Section */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-4">Profile Photo</h3>
        <div className="flex items-center gap-6">
          <div className="relative group">
            <div className="w-24 h-24 bg-indigo-500/20 rounded-full flex items-center justify-center border-4 border-neutral-900 overflow-hidden">
              {avatarUrl || user?.avatar_url ? (
                <img src={avatarUrl || user?.avatar_url || ""} alt="Avatar" className="w-full h-full object-cover" />
              ) : (
                <UserCircle className="w-12 h-12 text-indigo-400" />
              )}
              <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity rounded-full">
                <Camera className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
          <div className="flex-1 max-w-md">
            <label htmlFor="avatarUrl" className="block text-sm font-medium text-neutral-400 mb-2">
              Avatar Image URL
            </label>
            <input
              type="url"
              id="avatarUrl"
              value={avatarUrl}
              onChange={(e) => setAvatarUrl(e.target.value)}
              placeholder="https://example.com/photo.jpg"
              className="w-full px-3 py-2 bg-neutral-950 border border-neutral-800 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-neutral-600 transition-colors"
            />
            <p className="text-xs text-neutral-500 mt-2">
              Provide a direct link to an image (JPEG, PNG, or GIF). We recommend a square image at least 256x256px.
            </p>
          </div>
        </div>
      </div>

      <div className="border-t border-neutral-800 my-8" />

      {/* Account Info Section */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-4">Personal Information</h3>
        <div className="space-y-4 max-w-md">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-neutral-400 mb-2">
              Full Name
            </label>
            <input
              type="text"
              id="name"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 bg-neutral-950 border border-neutral-800 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-400 mb-2">
              Email Address
            </label>
            <input
              type="email"
              disabled
              value={user?.email || ""}
              className="w-full px-3 py-2 bg-neutral-900 border border-neutral-800 rounded-lg text-neutral-500 cursor-not-allowed"
            />
            <p className="text-xs text-neutral-500 mt-2">
              Email address cannot be changed at this time.
            </p>
          </div>
        </div>
      </div>

      {status === "error" && (
        <div className="text-red-400 text-sm bg-red-400/10 border border-red-400/20 p-3 rounded-lg max-w-md">
          {errorMessage}
        </div>
      )}

      {status === "success" && (
        <div className="text-emerald-400 text-sm bg-emerald-400/10 border border-emerald-400/20 p-3 rounded-lg max-w-md flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          Settings saved successfully.
        </div>
      )}

      <div>
        <button
          type="submit"
          disabled={loading}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2 rounded-lg font-medium text-sm transition-colors disabled:opacity-50"
        >
          {loading ? "Saving changes..." : "Save changes"}
        </button>
      </div>
    </form>
  );
}
