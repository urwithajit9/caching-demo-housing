/**
 * lib/api.ts
 *
 * Updated to use environment variables for production.
 */

const getBaseURL = () => {
  // In production, use the environment variable
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }

  // Development: differentiate server vs client
  if (typeof window === "undefined") {
    return "http://backend:8000";
  }
  return "http://localhost:8000";
};

export const API_BASE_URL = getBaseURL();

/**
 * Centralized fetch wrapper.
 * All API calls go through this function.
 */
export async function fetchAPI(endpoint: string, options?: RequestInit) {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(
      `API call failed: ${response.status} ${response.statusText}`,
    );
  }

  return response.json();
}
