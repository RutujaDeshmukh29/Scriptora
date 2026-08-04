"use client";

import { SettingsForm } from "@/features/auth/components/SettingsForm";

export default function SettingsPage() {
  return (
    <div className="p-8 max-w-4xl mx-auto w-full">
      <header className="mb-8 border-b border-neutral-800 pb-4">
        <h1 className="text-3xl font-bold text-white">Settings</h1>
        <p className="text-neutral-400 mt-2">Manage your account preferences and profile photo.</p>
      </header>

      <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-8">
        <SettingsForm />
      </div>
    </div>
  );
}
