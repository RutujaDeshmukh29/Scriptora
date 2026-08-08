"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { getScript, updateScript, Script } from "@/features/scripts/api";
import { ScriptEditor } from "@/features/editor/components/Editor";
import { exportToPdf } from "@/features/editor/utils/exportToPdf";
import Link from "next/link";
import { ArrowLeft, Save, CheckCircle2, Download } from "lucide-react";

export default function ScriptEditorPage() {
  const { projectId, scriptId } = useParams();
  const [script, setScript] = useState<Script | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "saved">("idle");
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");

  useEffect(() => {
    async function loadScript() {
      try {
        const data = await getScript(projectId as string, scriptId as string);
        setScript(data);
        setContent(data.content || "");
        setTitle(data.title || "");
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadScript();
  }, [projectId, scriptId]);

  const handleSave = async (htmlToSave?: string) => {
    if (!script) return;
    setSaving(true);
    setSaveStatus("saving");
    try {
      await updateScript(projectId as string, scriptId as string, {
        title: title,
        content: htmlToSave || content
      });
      setSaveStatus("saved");
      setTimeout(() => setSaveStatus("idle"), 2000);
    } catch (err) {
      console.error("Failed to save", err);
      setSaveStatus("idle");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-neutral-400">Loading editor...</div>;
  }

  if (!script) {
    return <div className="p-8 text-red-400">Script not found.</div>;
  }

  return (
    <div className="min-h-screen bg-neutral-950 flex flex-col">
      <header className="h-16 bg-neutral-900 border-b border-neutral-800 flex items-center justify-between px-6">
        <div className="flex items-center gap-4 flex-1">
          <Link 
            href={`/projects/${projectId}`}
            className="p-2 rounded-lg text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <input 
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onBlur={() => handleSave()}
            className="text-lg font-semibold text-white bg-transparent border-none focus:outline-none focus:ring-1 focus:ring-indigo-500 rounded px-2 py-1 w-full max-w-md transition-all hover:bg-neutral-800/50"
            placeholder="Untitled Script"
          />
        </div>

        <div className="flex items-center gap-4">
          {saveStatus === "saving" && (
            <span className="text-sm text-neutral-400 flex items-center gap-2">
              <span className="w-4 h-4 border-2 border-neutral-400 border-t-transparent rounded-full animate-spin" />
              Saving...
            </span>
          )}
          {saveStatus === "saved" && (
            <span className="text-sm text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-4 h-4" />
              Saved
            </span>
          )}
          <button
            onClick={() => exportToPdf(content, `${script.title}.pdf`)}
            className="flex items-center gap-2 bg-neutral-800 hover:bg-neutral-700 text-white px-4 py-2 rounded-lg font-medium text-sm transition-colors"
          >
            <Download className="w-4 h-4" />
            Export PDF
          </button>
          <button
            onClick={() => handleSave()}
            disabled={saving}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg font-medium text-sm transition-colors disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            Save
          </button>
        </div>
      </header>

      <main className="flex-1 overflow-hidden p-6">
        <div className="max-w-4xl mx-auto h-full flex flex-col">
          <ScriptEditor 
            initialContent={script.content}
            onUpdate={(html) => setContent(html)}
          />
        </div>
      </main>
    </div>
  );
}
