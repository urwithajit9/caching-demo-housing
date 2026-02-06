/**
 * app/page.tsx
 *
 * Client Component using SWR for data fetching and caching.
 */

"use client";

import useSWR from "swr";
import { useSearchParams } from "next/navigation";
import { PaginatedResponse, Property } from "@/types/property";
import { PropertyCard } from "@/components/PropertyCard";
import { FilterBar } from "@/components/FilterBar";
import { Pagination } from "@/components/Pagination";

export default function HomePage() {
  const searchParams = useSearchParams();

  // Build the endpoint URL with current filters
  const params = new URLSearchParams();
  const type = searchParams.get("type");
  const city = searchParams.get("city");
  const minPrice = searchParams.get("min_price");
  const maxPrice = searchParams.get("max_price");
  const page = searchParams.get("page");

  if (type) params.set("property_type", type);
  if (city) params.set("location__city", city);
  if (minPrice) params.set("price__gte", minPrice);
  if (maxPrice) params.set("price__lte", maxPrice);
  if (page) params.set("page", page);

  const queryString = params.toString();
  const endpoint = `/api/properties/cached/${queryString ? `?${queryString}` : ""}`;

  // SWR hook - fetches data and handles caching
  const { data, error, isLoading, isValidating } =
    useSWR<PaginatedResponse<Property>>(endpoint);



  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading properties...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-lg font-semibold">
            Failed to load properties
          </p>
          <p className="text-gray-600 mt-2">Please try again later.</p>
        </div>
      </div>
    );
  }

  // Data loaded successfully
  if (!data) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Housing Portal
              </h1>
              <p className="text-gray-600 mt-1">
                {data.count.toLocaleString()} properties available
              </p>
            </div>

            {/* Cache status indicator - ADD THIS */}
            {isValidating && (
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                <span>Refreshing...</span>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Filter bar */}
        <FilterBar />

        {/* Results */}
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
            <Pagination
              count={data.count}
              next={data.next}
              previous={data.previous}
            />
            <div className="mt-8 text-center text-gray-600">
              Showing {data.results.length} of {data.count} properties
            </div>
          </>
        )}
      </main>
    </div>
  );
}
