/**
 * components/FilterBar.tsx
 *
 * A client component that renders filter inputs.
 * Updates URL query parameters when filters change.
 */

"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState, useEffect } from "react";

export function FilterBar() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // Initialize state from URL parameters
  const [propertyType, setPropertyType] = useState(
    searchParams.get("type") || "",
  );
  const [city, setCity] = useState(searchParams.get("city") || "");
  const [minPrice, setMinPrice] = useState(searchParams.get("min_price") || "");
  const [maxPrice, setMaxPrice] = useState(searchParams.get("max_price") || "");

  // Update URL when filters change
  useEffect(() => {
    const params = new URLSearchParams();

    if (propertyType) params.set("type", propertyType);
    if (city) params.set("city", city);
    if (minPrice) params.set("min_price", minPrice);
    if (maxPrice) params.set("max_price", maxPrice);

    // Push to URL without reloading the page
    const queryString = params.toString();
    router.push(queryString ? `/?${queryString}` : "/");
  }, [propertyType, city, minPrice, maxPrice, router]);

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Property Type Filter */}
        <div>
          <label
            htmlFor="type"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Property Type
          </label>
          <select
            id="type"
            value={propertyType}
            onChange={(e) => setPropertyType(e.target.value)}
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Types</option>
            <option value="apartment">Apartment</option>
            <option value="house">House</option>
            <option value="villa">Villa</option>
            <option value="studio">Studio</option>
            <option value="condo">Condo</option>
          </select>
        </div>

        {/* City Filter */}
        <div>
          <label
            htmlFor="city"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            City
          </label>
          <select
            id="city"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Cities</option>
            <option value="Seattle">Seattle</option>
            <option value="Portland">Portland</option>
            <option value="San Francisco">San Francisco</option>
            <option value="Los Angeles">Los Angeles</option>
            <option value="Austin">Austin</option>
            <option value="Denver">Denver</option>
            <option value="Chicago">Chicago</option>
            <option value="Miami">Miami</option>
            <option value="New York">New York</option>
            <option value="Boston">Boston</option>
          </select>
        </div>

        {/* Min Price Filter */}
        <div>
          <label
            htmlFor="min-price"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Min Price
          </label>
          <input
            id="min-price"
            type="number"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            placeholder="No minimum"
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Max Price Filter */}
        <div>
          <label
            htmlFor="max-price"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Max Price
          </label>
          <input
            id="max-price"
            type="number"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            placeholder="No maximum"
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Clear filters button */}
      {(propertyType || city || minPrice || maxPrice) && (
        <button
          onClick={() => {
            setPropertyType("");
            setCity("");
            setMinPrice("");
            setMaxPrice("");
          }}
          className="mt-4 text-sm text-blue-600 hover:text-blue-800 font-medium"
        >
          Clear all filters
        </button>
      )}
    </div>
  );
}
