"use client";

import { useEffect, useState } from "react";
import { getScripts, createScript, Script } from "../api";
import { useRouter } from "next/navigation";
import { FileText, Plus } from "lucide-react";

export function ScriptList({ projectId }: { projectId: string }) {
  const router = useRouter();
  const [scripts, setScripts] = useState<Script[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    async function loadScripts() {
      try {
        const data = await getScripts(projectId);
        setScripts(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadScripts();
  }, [projectId]);

  const handleCreate = async () => {
    setCreating(true);
    try {
      const script = await createScript(projectId, "Untitled Script");
      router.push(`/projects/${projectId}/scripts/${script.id}`);
    } catch (err) {
      console.error(err);
      setCreating(false);
    }
  };

  if (loading) {
    return <div className="text-neutral-500 animate-pulse">Loading scripts...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-white">Project Scripts</h3>
        <button
          onClick={handleCreate}
          disabled={creating}
          className="flex items-center gap-2 bg-neutral-800 hover:bg-neutral-700 text-white px-3 py-1.5 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
        >
          <Plus className="w-4 h-4" />
          {creating ? "Creating..." : "New Script"}
        </button>
      </div>

      {scripts.length === 0 ? (
        <div className="text-center py-12 border border-neutral-800 border-dashed rounded-xl bg-neutral-900/50">
          <FileText className="w-8 h-8 text-neutral-600 mx-auto mb-3" />
          <p className="text-neutral-400 text-sm mb-4">No scripts have been created yet.</p>
          <button
            onClick={handleCreate}
            disabled={creating}
            className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            Create your first script
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {scripts.map(script => (
            <div 
              key={script.id}
              onClick={() => router.push(`/projects/${projectId}/scripts/${script.id}`)}
              className="p-4 border border-neutral-800 bg-neutral-900 rounded-xl hover:border-indigo-500/50 hover:bg-neutral-800/50 cursor-pointer transition-all group"
            >
              <div className="flex items-start gap-3">
                <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-400">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-white font-medium group-hover:text-indigo-400 transition-colors">{script.title}</h4>
                  <p className="text-neutral-500 text-xs mt-1">
                    Updated {new Date(script.updated_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
