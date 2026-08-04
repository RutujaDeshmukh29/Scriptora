"use client";

import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";
import { EditorToolbar } from "./EditorToolbar";
import { useEffect, useState } from "react";

interface ScriptEditorProps {
  initialContent: string;
  onUpdate: (html: string) => void;
  readOnly?: boolean;
}

export function ScriptEditor({ initialContent, onUpdate, readOnly = false }: ScriptEditorProps) {
  const [mounted, setMounted] = useState(false);

  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({
        placeholder: "Start writing your script here...",
      }),
    ],
    content: initialContent,
    editable: !readOnly,
    onUpdate: ({ editor }) => {
      onUpdate(editor.getHTML());
    },
    editorProps: {
      attributes: {
        class: "prose prose-invert prose-indigo max-w-none focus:outline-none min-h-[500px] p-6",
      },
    },
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div className="h-[500px] bg-neutral-900 animate-pulse rounded-xl" />;
  }

  return (
    <div className="border border-neutral-800 rounded-xl bg-neutral-950 shadow-sm overflow-hidden flex flex-col">
      {!readOnly && <EditorToolbar editor={editor} />}
      <div className="flex-1 bg-neutral-950 overflow-y-auto">
        <EditorContent editor={editor} />
      </div>
    </div>
  );
}
