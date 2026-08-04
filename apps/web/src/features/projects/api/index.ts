import { fetchApi } from "@/services/http";

export interface Project {
  id: string;
  name: string;
  description: string | null;
  status: "active" | "archived";
  organization_id: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export async function getProjects(): Promise<Project[]> {
  return fetchApi("/projects/");
}

export async function createProject(name: string, description?: string): Promise<Project> {
  return fetchApi("/projects/", {
    method: "POST",
    body: JSON.stringify({ name, description }),
  });
}

export async function getProject(id: string): Promise<Project> {
  return fetchApi(`/projects/${id}`);
}

export async function archiveProject(id: string): Promise<Project> {
  return fetchApi(`/projects/${id}/archive`, {
    method: "DELETE",
  });
}
