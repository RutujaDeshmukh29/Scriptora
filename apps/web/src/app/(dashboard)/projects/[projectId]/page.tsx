"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getProject, Project } from "@/features/projects/api";
import { ScriptList } from "@/features/scripts/components/ScriptList";
import { ProjectMembers } from "@/features/projects/components/ProjectMembers";

export default function ProjectDetailsPage() {
  const { projectId } = useParams();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProject() {
      try {
        const data = await getProject(projectId as string);
        setProject(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchProject();
  }, [projectId]);

  if (loading) {
    return <div className="p-8 text-neutral-400">Loading project...</div>;
  }

  if (!project) {
    return <div className="p-8 text-red-400">Project not found.</div>;
  }

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <header className="mb-8 border-b border-neutral-800 pb-4">
        <h1 className="text-3xl font-bold text-white">{project.name}</h1>
        {project.description && (
          <p className="text-neutral-400 mt-2">{project.description}</p>
        )}
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-neutral-950 border border-neutral-800 rounded-xl p-6">
            <ScriptList projectId={projectId as string} />
          </div>
        </div>

        <div>
          <div className="bg-neutral-950 border border-neutral-800 rounded-xl p-6">
            <ProjectMembers projectId={projectId as string} />
          </div>
        </div>
      </div>
    </div>
  );
}
