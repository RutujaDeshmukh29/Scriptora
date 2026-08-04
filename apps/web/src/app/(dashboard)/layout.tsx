import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-neutral-950 font-sans">
      <Sidebar />
      <Topbar />
      <main className="md:ml-64 flex-1">
        {children}
      </main>
    </div>
  );
}
