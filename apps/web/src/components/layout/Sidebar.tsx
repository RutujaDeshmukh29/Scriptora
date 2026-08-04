"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Projects", href: "/dashboard" },
    { name: "Activity Logs", href: "/activity" },
    { name: "Profile", href: "/profile" },
    { name: "Settings", href: "/settings" },
  ];

  return (
    <aside className="w-64 bg-neutral-900 border-r border-neutral-800 hidden md:flex flex-col h-screen fixed left-0 top-0">
      <div className="h-16 flex items-center px-6 border-b border-neutral-800">
        <span className="text-xl font-bold text-white tracking-tight">Scriptora</span>
      </div>
      
      <nav className="flex-1 px-4 py-6 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                isActive
                  ? "bg-indigo-500/10 text-indigo-400"
                  : "text-neutral-400 hover:bg-neutral-800 hover:text-white"
              }`}
            >
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-neutral-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold">
            U
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-medium text-white">My Account</span>
            <span className="text-xs text-neutral-500">Free Tier</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
