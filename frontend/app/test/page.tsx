/**
 * app/test/page.tsx
 *
 * A simple test page to verify the API connection works.
 * This is a Server Component — it fetches on the server before rendering.
 */

import { fetchAPI } from "@/lib/api"; // @/lib/api means frontend/lib/api.ts
import { PaginatedResponse, Property } from "@/types/property";

export default async function TestPage() {
  try {
    const data: PaginatedResponse<Property> = await fetchAPI(
      "/api/properties/cached/",
    );

    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">API Connection Test</h1>
        <p className="mb-4">
          Successfully fetched {data.results.length} properties out of{" "}
          {data.count} total.
        </p>
        <div className="space-y-2">
          {data.results.slice(0, 3).map((property) => (
            <div key={property.id} className="border p-4 rounded">
              <h2 className="font-bold">{property.title}</h2>
              <p>Price: ${property.price}</p>
              <p>
                Location: {property.location.city}, {property.location.state}
              </p>
            </div>
          ))}
        </div>
      </div>
    );
  } catch (error) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold text-red-600">Error</h1>
        <p>Failed to fetch data from API.</p>
        <pre className="mt-4 p-4 bg-gray-100 rounded">
          {error instanceof Error ? error.message : "Unknown error"}
        </pre>
      </div>
    );
  }
}
