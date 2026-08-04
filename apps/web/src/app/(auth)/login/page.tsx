import { LoginForm } from "@/features/auth/components/LoginForm";
import Link from "next/link";

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-neutral-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 text-neutral-100 selection:bg-indigo-500/30">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-4xl font-extrabold tracking-tight text-white">
          Scriptora
        </h2>
        <p className="mt-2 text-center text-sm text-neutral-400">
          Sign in to your workspace
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-neutral-900 border border-neutral-800 p-8 rounded-2xl shadow-xl">
          <LoginForm />
          
          <div className="mt-6 text-center text-sm text-neutral-400">
            Don't have an account?{" "}
            <Link href="/register" className="text-indigo-400 hover:text-indigo-300 transition-colors font-medium">
              Create one
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
