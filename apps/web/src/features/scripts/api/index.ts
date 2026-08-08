import { fetchApi } from "@/services/http";

export interface Script {
  id: string;
  project_id: string;
  title: string;
  content: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export async function getScripts(projectId: string): Promise<Script[]> {
  return fetchApi(`/projects/${projectId}/scripts/`);
}

export async function createScript(projectId: string, title?: string): Promise<Script> {
  return fetchApi(`/projects/${projectId}/scripts/`, {
    method: "POST",
    body: JSON.stringify({ title }),
  });
}

export async function getScript(projectId: string, scriptId: string): Promise<Script> {
  return fetchApi(`/scripts/${scriptId}`);
}

export async function updateScript(projectId: string, scriptId: string, data: { title?: string; content?: string }): Promise<Script> {
  return fetchApi(`/scripts/${scriptId}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}
