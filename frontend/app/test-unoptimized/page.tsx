/**
 * app/test-unoptimized/page.tsx
 *
 * Test page WITHOUT Next.js Image optimization.
 * Uses regular <img> tags to show the performance difference.
 */

import { fetchAPI } from "@/lib/api";
import { PaginatedResponse, Property } from "@/types/property";

export default async function UnoptimizedTestPage() {
  const data: PaginatedResponse<Property> = await fetchAPI(
    "/api/properties/cached/",
  );

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Unoptimized Images Test</h1>
        <p className="text-red-600 mb-8">
          ⚠️ This page uses regular &lt;img&gt; tags without optimization. Do
          NOT use this in production.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.results.map((property) => {
            const mainImage = property.images?.[0];

            return (
              <div
                key={property.id}
                className="border rounded-lg overflow-hidden"
              >
                <div className="h-48 bg-gray-200">
                  {mainImage && (
                    /* Regular img tag - NO optimization */
                    <img
                      src={mainImage.original_url} // Full-size original (5MB+)
                      alt={property.title}
                      className="w-full h-full object-cover"
                    />
                  )}
                </div>
                <div className="p-4">
                  <h3 className="font-bold">{property.title}</h3>
                  <p className="text-xl font-bold text-blue-600">
                    ${property.price}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
