/**
 * lib/api.ts
 *
 * Centralized API configuration.
 * Handles the URL difference between server-side (Docker) and client-side (browser).
 */

// Determine the base URL based on where the code is running
const getBaseURL = () => {
  // Check if we're running on the server (Node.js) or in the browser
  if (typeof window === "undefined") {
    // Server-side: use the Docker service name
    return "http://backend:8000";
  }
  // Client-side: use localhost
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
