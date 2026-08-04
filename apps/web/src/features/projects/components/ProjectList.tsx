"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getProjects, createProject, Project } from "../api";

export function ProjectList() {
  const router = useRouter();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  // New Project Form State
  const [isCreating, setIsCreating] = useState(false);
  const [newProjectName, setNewProjectName] = useState("");
  const [newProjectDesc, setNewProjectDesc] = useState("");
  const [createLoading, setCreateLoading] = useState(false);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (err: any) {
      if (err.message === "Could not validate credentials") {
        router.push("/login");
      } else {
        setError(err.message || "Failed to load projects");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProjectName.trim()) return;

    setCreateLoading(true);
    try {
      const project = await createProject(newProjectName, newProjectDesc);
      setProjects([...projects, project]);
      setIsCreating(false);
      setNewProjectName("");
      setNewProjectDesc("");
    } catch (err: any) {
      alert(err.message || "Failed to create project");
    } finally {
      setCreateLoading(false);
    }
  };

  return (
    <>
      <header className="flex justify-between items-center mb-12 border-b border-neutral-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Dashboard</h1>
          <p className="text-neutral-400 mt-1">Manage your Scriptora projects and workspaces.</p>
        </div>
        <button
          onClick={() => setIsCreating(true)}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2.5 rounded-lg font-semibold text-sm transition-all shadow-lg shadow-indigo-500/20"
        >
          + New Project
        </button>
      </header>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl mb-8">
          {error}
        </div>
      )}

      {isCreating && (
        <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 mb-8 shadow-xl">
          <h2 className="text-xl font-bold text-white mb-4">Create New Project</h2>
          <form onSubmit={handleCreateProject} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-neutral-400 mb-1">Project Name</label>
              <input
                type="text"
                required
                value={newProjectName}
                onChange={(e) => setNewProjectName(e.target.value)}
                className="w-full px-4 py-2 bg-neutral-950 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-white placeholder-neutral-600"
                placeholder="e.g. Q3 Marketing Campaign"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-neutral-400 mb-1">Description (Optional)</label>
              <textarea
                value={newProjectDesc}
                onChange={(e) => setNewProjectDesc(e.target.value)}
                className="w-full px-4 py-2 bg-neutral-950 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-white placeholder-neutral-600 resize-none h-24"
                placeholder="A brief description of what this project is about..."
              />
            </div>
            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={() => setIsCreating(false)}
                className="px-4 py-2 rounded-lg font-medium text-neutral-300 hover:text-white hover:bg-neutral-800 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={createLoading}
                className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2 rounded-lg font-semibold transition-colors disabled:opacity-50"
              >
                {createLoading ? "Creating..." : "Create Project"}
              </button>
            </div>
          </form>
        </div>
      )}

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 bg-neutral-900 rounded-2xl border border-neutral-800 animate-pulse"></div>
          ))}
        </div>
      ) : projects.length === 0 ? (
        <div className="text-center py-20 bg-neutral-900/50 rounded-2xl border border-neutral-800 border-dashed">
          <h3 className="text-xl font-semibold text-neutral-300 mb-2">No projects found</h3>
          <p className="text-neutral-500 max-w-sm mx-auto mb-6">
            You haven't created any projects yet. Start by creating a new project workspace.
          </p>
          <button
            onClick={() => setIsCreating(true)}
            className="bg-neutral-800 hover:bg-neutral-700 text-white px-5 py-2.5 rounded-lg font-medium text-sm transition-all"
          >
            Create your first project
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div
              key={project.id}
              className="group bg-neutral-900 border border-neutral-800 hover:border-indigo-500/50 rounded-2xl p-6 transition-all hover:shadow-xl hover:shadow-indigo-500/5 cursor-pointer flex flex-col"
              onClick={() => router.push(`/projects/${project.id}`)}
            >
              <div className="flex justify-between items-start mb-4">
                <div className="w-10 h-10 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center font-bold text-lg">
                  {project.name.charAt(0).toUpperCase()}
                </div>
                <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${project.status === 'active' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-neutral-800 text-neutral-400'}`}>
                  {project.status.toUpperCase()}
                </span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-indigo-400 transition-colors line-clamp-1">{project.name}</h3>
              <p className="text-neutral-400 text-sm line-clamp-2 mb-6 flex-grow">
                {project.description || "No description provided."}
              </p>
              <div className="text-xs text-neutral-500 pt-4 border-t border-neutral-800 mt-auto">
                Updated {new Date(project.updated_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
