/**
 * app/page.tsx
 *
 * Updated to support filtering via URL query parameters.
 */

import { fetchAPI } from "@/lib/api";
import { PaginatedResponse, Property } from "@/types/property";
import { PropertyCard } from "@/components/PropertyCard";
import { FilterBar } from "@/components/FilterBar";

interface HomePageProps {
  searchParams:Promise< {
    type?: string;
    city?: string;
    min_price?: string;
    max_price?: string;
    page?: string;
  }>;
}

export default async function HomePage({ searchParams }: HomePageProps) {
  // Build the API URL with query parameters
  const filters = await searchParams;
  const params = new URLSearchParams();

  // if (searchParams.type) params.set("property_type", searchParams.type);
  // if (searchParams.city) params.set("location__city", searchParams.city);
  // if (searchParams.min_price) params.set("price__gte", searchParams.min_price);
  // if (searchParams.max_price) params.set("price__lte", searchParams.max_price);
  // if (searchParams.page) params.set("page", searchParams.page);

  // 3. Use the unwrapped 'filters' object
  if (filters.type) params.set("property_type", filters.type);
  if (filters.city) params.set("location__city", filters.city);
  if (filters.min_price) params.set("price__gte", filters.min_price);
  if (filters.max_price) params.set("price__lte", filters.max_price);
  if (filters.page) params.set("page", filters.page);

  const queryString = params.toString();
  const endpoint = `/api/properties/cached/${queryString ? `?${queryString}` : ""}`;

  const data: PaginatedResponse<Property> = await fetchAPI(endpoint);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Housing Portal</h1>
          <p className="text-gray-600 mt-1">
            {data.count.toLocaleString()} properties available
          </p>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Filter bar */}
        <FilterBar />

        {/* Results count */}
        {data.count === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">
              No properties match your filters.
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Try adjusting your search criteria.
            </p>
          </div>
        ) : (
          <>
            {/* Grid of property cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data.results.map((property) => (
                <PropertyCard key={property.id} property={property} />
              ))}
            </div>

            {/* Pagination info */}
            <div className="mt-8 text-center text-gray-600">
              Showing {data.results.length} of {data.count} properties
            </div>
          </>
        )}
      </main>
    </div>
  );
}
