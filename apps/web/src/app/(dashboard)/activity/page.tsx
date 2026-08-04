"use client";

import { Activity } from "lucide-react";

export default function ActivityPage() {
  return (
    <div className="p-8 max-w-4xl mx-auto w-full">
      <header className="mb-8 border-b border-neutral-800 pb-4">
        <h1 className="text-3xl font-bold text-white">Activity Logs</h1>
        <p className="text-neutral-400 mt-2">Track recent changes across all your projects.</p>
      </header>

      <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-12 flex flex-col items-center text-center">
        <div className="w-12 h-12 bg-neutral-800 rounded-full flex items-center justify-center mb-4">
          <Activity className="w-6 h-6 text-neutral-500" />
        </div>
        <h2 className="text-lg font-semibold text-white mb-2">No recent activity</h2>
        <p className="text-neutral-400 max-w-sm">
          Once you and your team start making edits and updates to scripts, the history log will appear here.
        </p>
      </div>
    </div>
  );
}
