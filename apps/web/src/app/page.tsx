import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-neutral-950 flex flex-col items-center justify-center text-neutral-100 selection:bg-indigo-500/30 overflow-hidden relative">
      {/* Background glow effects */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-[128px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[128px] pointer-events-none"></div>

      <div className="z-10 text-center max-w-3xl px-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-sm font-medium mb-8 border border-indigo-500/20">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
          </span>
          Scriptora v0.1.0 is Live
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-white mb-6">
          The future of <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">Collaborative</span> Writing.
        </h1>
        
        <p className="text-lg md:text-xl text-neutral-400 mb-10 max-w-2xl mx-auto leading-relaxed">
          Scriptora is an open-source, real-time collaborative scriptwriting platform built for creative teams, studios, and agencies.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/login"
            className="w-full sm:w-auto px-8 py-3.5 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold shadow-lg shadow-indigo-600/25 transition-all hover:scale-105"
          >
            Go to Dashboard
          </Link>
          <a
            href="https://github.com/RutujaDeshmukh29/Scriptora"
            target="_blank"
            rel="noopener noreferrer"
            className="w-full sm:w-auto px-8 py-3.5 rounded-full bg-neutral-900 hover:bg-neutral-800 text-white font-semibold border border-neutral-800 hover:border-neutral-700 transition-all"
          >
            View on GitHub
          </a>
        </div>
      </div>
    </div>
  );
}
