"use client";

import { Users, Shield, UserPlus } from "lucide-react";

export function ProjectMembers({ projectId }: { projectId: string }) {
  // Mock members for now since we haven't implemented the API route for listing members
  const members = [
    { id: "1", name: "Current User", email: "you@example.com", role: "owner" }
  ];

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-white">Project Members</h3>
        <button
          className="flex items-center gap-2 bg-neutral-800 hover:bg-neutral-700 text-white px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
        >
          <UserPlus className="w-4 h-4" />
          Invite
        </button>
      </div>

      <div className="space-y-3">
        {members.map(member => (
          <div key={member.id} className="flex items-center justify-between p-3 border border-neutral-800 bg-neutral-900 rounded-lg">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-sm">
                {member.name.charAt(0)}
              </div>
              <div>
                <p className="text-sm font-medium text-white">{member.name}</p>
                <p className="text-xs text-neutral-500">{member.email}</p>
              </div>
            </div>
            
            <div className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-neutral-800 text-neutral-400 text-xs font-medium">
              <Shield className="w-3 h-3" />
              {member.role.charAt(0).toUpperCase() + member.role.slice(1)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
