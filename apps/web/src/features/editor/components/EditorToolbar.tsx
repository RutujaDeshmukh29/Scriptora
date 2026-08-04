import { Editor } from "@tiptap/react";
import { 
  Bold, 
  Italic, 
  Strikethrough, 
  Code, 
  List, 
  ListOrdered,
  Heading1,
  Heading2,
  Quote,
  Undo,
  Redo
} from "lucide-react";

interface EditorToolbarProps {
  editor: Editor | null;
}

export function EditorToolbar({ editor }: EditorToolbarProps) {
  if (!editor) {
    return null;
  }

  const buttons = [
    {
      icon: <Bold className="w-4 h-4" />,
      onClick: () => editor.chain().focus().toggleBold().run(),
      isActive: editor.isActive('bold'),
      title: "Bold"
    },
    {
      icon: <Italic className="w-4 h-4" />,
      onClick: () => editor.chain().focus().toggleItalic().run(),
      isActive: editor.isActive('italic'),
      title: "Italic"
    },
    {
      icon: <Strikethrough className="w-4 h-4" />,
      onClick: () => editor.chain().focus().toggleStrike().run(),
      isActive: editor.isActive('strike'),
      title: "Strikethrough"
    },
    {
      icon: <Code className="w-4 h-4" />,
      onClick: () => editor.chain().focus().toggleCode().run(),
      isActive: editor.isActive('code'),
      title: "Code"
    },
    { divider: true },
    {
      icon: <Heading1 className="w-4 h-4" />,
      onClick: () => editor.chain().focus().toggleHeading({ level: 1 }).run(),
      isActive: editor.isActive('heading', { level: 1 }),
      title: "Heading 1"
    },
    {
      icon: <Heading2 className="w-4 h-4" />,
      onClick: () => editor.chain().focus().toggleHeading({ level: 2 }).run(),
      isActive: editor.isActive('heading', { level: 2 }),
      title: "Heading 2"
    },
    { divider: true },
    {
      icon: <List className="w-4 h-4" />,
      onClick: () => editor.chain().focus().toggleBulletList().run(),
      isActive: editor.isActive('bulletList'),
      title: "Bullet List"
    },
    {
      icon: <ListOrdered className="w-4 h-4" />,
      onClick: () => editor.chain().focus().toggleOrderedList().run(),
      isActive: editor.isActive('orderedList'),
      title: "Ordered List"
    },
    {
      icon: <Quote className="w-4 h-4" />,
      onClick: () => editor.chain().focus().toggleBlockquote().run(),
      isActive: editor.isActive('blockquote'),
      title: "Blockquote"
    },
    { divider: true },
    {
      icon: <Undo className="w-4 h-4" />,
      onClick: () => editor.chain().focus().undo().run(),
      disabled: !editor.can().undo(),
      title: "Undo"
    },
    {
      icon: <Redo className="w-4 h-4" />,
      onClick: () => editor.chain().focus().redo().run(),
      disabled: !editor.can().redo(),
      title: "Redo"
    },
  ];

  return (
    <div className="flex flex-wrap items-center gap-1 p-2 bg-neutral-900 border-b border-neutral-800 rounded-t-xl">
      {buttons.map((btn, i) => {
        if (btn.divider) {
          return <div key={`divider-${i}`} className="w-px h-6 bg-neutral-800 mx-1" />;
        }
        return (
          <button
            key={btn.title}
            onClick={btn.onClick}
            disabled={btn.disabled}
            title={btn.title}
            className={`p-2 rounded-lg transition-colors ${
              btn.isActive
                ? "bg-indigo-500/20 text-indigo-400"
                : "text-neutral-400 hover:bg-neutral-800 hover:text-white"
            } ${btn.disabled ? "opacity-50 cursor-not-allowed" : ""}`}
          >
            {btn.icon}
          </button>
        );
      })}
    </div>
  );
}
