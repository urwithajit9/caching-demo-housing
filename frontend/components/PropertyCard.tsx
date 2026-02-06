/**
 * components/PropertyCard.tsx
 *
 * A card component that displays a single property listing.
 * Used in the grid on the listing page.
 */

import { Property } from "@/types/property";
import { formatPrice, capitalize } from "@/lib/formatters";

interface PropertyCardProps {
  property: Property;
}

export function PropertyCard({ property }: PropertyCardProps) {
  // Determine badge color based on status
  const statusColors = {
    available: "bg-green-100 text-green-800",
    pending: "bg-yellow-100 text-yellow-800",
    sold: "bg-red-100 text-red-800",
  };

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-200">
      {/* Image placeholder - we'll add real images in Part 6 */}
      <div className="h-48 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-6xl font-bold">
        {property.bedrooms}BR
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Status badge */}
        <div className="mb-2">
          <span
            className={`inline-block px-2 py-1 text-xs font-semibold rounded ${statusColors[property.status]}`}
          >
            {capitalize(property.status)}
          </span>
        </div>

        {/* Title */}
        <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2">
          {property.title}
        </h3>

        {/* Price */}
        <p className="text-2xl font-bold text-blue-600 mb-3">
          {formatPrice(property.price)}
        </p>

        {/* Details grid */}
        <div className="grid grid-cols-2 gap-2 text-sm text-gray-600 mb-3">
          <div>
            <span className="font-semibold">{property.bedrooms}</span> Beds
          </div>
          <div>
            <span className="font-semibold">{property.bathrooms}</span> Baths
          </div>
          <div className="col-span-2">
            <span className="font-semibold">
              {capitalize(property.property_type)}
            </span>
          </div>
        </div>

        {/* Location */}
        <div className="border-t pt-3">
          <p className="text-sm text-gray-600">
            📍 {property.location.city}, {property.location.state}
          </p>
        </div>

        {/* Agent info */}
        {property.agent && (
          <div className="mt-2 text-xs text-gray-500">
            Listed by {property.agent.name}
          </div>
        )}
      </div>
    </div>
  );
}
