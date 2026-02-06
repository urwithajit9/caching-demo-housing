/**
 * lib/fetcher.ts
 *
 * Fetcher function for SWR.
 * SWR calls this function with a URL and expects a promise that resolves to data.
 */

import { API_BASE_URL } from "./api";

export async function fetcher(endpoint: string) {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url);

  if (!response.ok) {
    const error = new Error("An error occurred while fetching the data.");
    // Attach extra info to the error object
    throw error;
  }

  return response.json();
}
