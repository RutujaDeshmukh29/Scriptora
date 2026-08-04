import { ProjectList } from "@/features/projects/components/ProjectList";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        <ProjectList />
      </div>
    </div>
  );
}
