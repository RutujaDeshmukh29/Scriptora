import { RegisterForm } from "@/features/auth/components/RegisterForm";
import Link from "next/link";

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
            Scriptora
          </h2>
          <p className="mt-2 text-center text-sm text-neutral-400">
            Create a new workspace account
          </p>
        </div>
        
        <div className="bg-neutral-900 border border-neutral-800 p-8 rounded-2xl shadow-xl">
          <RegisterForm />
          
          <div className="mt-6 text-center text-sm text-neutral-400">
            Already have an account?{" "}
            <Link href="/login" className="text-indigo-400 hover:text-indigo-300 transition-colors font-medium">
              Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
