/**
 * components/PropertyCard.tsx
 *
 * A card component that displays a single property listing.
 * Used in the grid on the listing page.
 */

import { Property } from "@/types/property";
import { formatPrice, capitalize } from "@/lib/formatters";
import Image from "next/image";
import { LazyImage } from "./LazyImage";
import { getCloudinaryBlurURL } from "@/lib/cloudinary";
import Link from "next/link";
interface PropertyCardProps {
  property: Property;
}

export function PropertyCard({ property }: PropertyCardProps) {
  const statusColors = {
    available: "bg-green-100 text-green-800",
    pending: "bg-yellow-100 text-yellow-800",
    sold: "bg-red-100 text-red-800",
  };

  // Get the first image (display_order = 0) or fallback to placeholder
  const mainImage =
    property.images && property.images.length > 0
      ? property.images.find((img) => img.display_order === 0) ||
        property.images[0]
      : null;

  return (
    <Link href={`/properties/${property.id}`} className="block">
    <div className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-200">
      {/* Image section - UPDATED */}
      <div className="relative h-48 w-full bg-gray-100">
        {mainImage ? (
          // <Image
          //   src={mainImage.thumbnail_url}
          //   alt={mainImage.alt_text || property.title}
          //   fill
          //   className="object-cover"
          //   sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          //   loading="lazy"
              //  placeholder="blur"
              //  blurDataURL={getCloudinaryBlurURL(mainImage.thumbnail_url)}
          // />
          <LazyImage
            src={mainImage.thumbnail_url}
            alt={mainImage.alt_text || property.title}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            // placeholder="blur"
            // blurDataURL={getCloudinaryBlurURL(mainImage.thumbnail_url)}
          />
        ) : (
          // Fallback gradient if no image uploaded
          <div className="h-full w-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-6xl font-bold">
            {property.bedrooms}BR
          </div>
        )}
      </div>

      {/* Content - keep unchanged */}
      <div className="p-4">
        <div className="mb-2">
          <span
            className={`inline-block px-2 py-1 text-xs font-semibold rounded ${statusColors[property.status]}`}
          >
            {capitalize(property.status)}
          </span>
        </div>

        <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2">
          {property.title}
        </h3>

        <p className="text-2xl font-bold text-blue-600 mb-3">
          {formatPrice(property.price)}
        </p>

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

        <div className="border-t pt-3">
          <p className="text-sm text-gray-600">
            📍 {property.location.city}, {property.location.state}
          </p>
        </div>

        {property.agent && (
          <div className="mt-2 text-xs text-gray-500">
            Listed by {property.agent.name}
          </div>
        )}
      </div>
    </div>
    </Link>
  );
}
