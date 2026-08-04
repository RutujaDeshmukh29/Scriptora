"use client";

import { Bell } from "lucide-react";

export default function NotificationsPage() {
  return (
    <div className="p-8 max-w-4xl mx-auto w-full">
      <header className="mb-8 border-b border-neutral-800 pb-4">
        <h1 className="text-3xl font-bold text-white">Notifications</h1>
        <p className="text-neutral-400 mt-2">Stay updated on your projects and mentions.</p>
      </header>

      <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-12 flex flex-col items-center text-center">
        <div className="w-12 h-12 bg-neutral-800 rounded-full flex items-center justify-center mb-4">
          <Bell className="w-6 h-6 text-neutral-500" />
        </div>
        <h2 className="text-lg font-semibold text-white mb-2">You're all caught up!</h2>
        <p className="text-neutral-400 max-w-sm">
          When team members mention you or leave comments on your scripts, they'll appear here.
        </p>
      </div>
    </div>
  );
}
