/**
 * app/properties/[id]/page.tsx
 *
 * Property detail page showing full information and all images.
 */

import { fetchAPI } from "@/lib/api";
import { Property } from "@/types/property";
import { ImageGallery } from "@/components/ImageGallery";
import { formatPrice, capitalize, formatDate } from "@/lib/formatters";
import Link from "next/link";

interface PropertyDetailPageProps {
  params: {
    id: string;
  };
}

export default async function PropertyDetailPage({
  params,
}: PropertyDetailPageProps) {
    const { id } = await params;
  const property: Property = await fetchAPI(`/api/properties/${id}/`);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <Link
            href="/"
            className="text-blue-600 hover:text-blue-800 mb-4 inline-block"
          >
            ← Back to listings
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">{property.title}</h1>
          <p className="text-gray-600 mt-1">
            📍 {property.location.city}, {property.location.state}{" "}
            {property.location.zip_code}
          </p>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left column - Images and details */}
          <div className="lg:col-span-2 space-y-6">
            {/* Image gallery */}
            <ImageGallery images={property.images} />

            {/* Description */}
            <div className="bg-white rounded-lg p-6 shadow">
              <h2 className="text-xl font-bold mb-4">About this property</h2>
              <p className="text-gray-700 whitespace-pre-line">
                {property.description}
              </p>
            </div>

            {/* Details */}
            <div className="bg-white rounded-lg p-6 shadow">
              <h2 className="text-xl font-bold mb-4">Property Details</h2>
              <dl className="grid grid-cols-2 gap-4">
                <div>
                  <dt className="text-sm text-gray-600">Type</dt>
                  <dd className="text-lg font-semibold">
                    {capitalize(property.property_type)}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-gray-600">Status</dt>
                  <dd className="text-lg font-semibold">
                    {capitalize(property.status)}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-gray-600">Bedrooms</dt>
                  <dd className="text-lg font-semibold">{property.bedrooms}</dd>
                </div>
                <div>
                  <dt className="text-sm text-gray-600">Bathrooms</dt>
                  <dd className="text-lg font-semibold">
                    {property.bathrooms}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-gray-600">Listed</dt>
                  <dd className="text-lg font-semibold">
                    {formatDate(property.created_at)}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-gray-600">Views</dt>
                  <dd className="text-lg font-semibold">
                    {property.view_count.toLocaleString()}
                  </dd>
                </div>
              </dl>
            </div>
          </div>

          {/* Right column - Price and agent */}
          <div className="space-y-6">
            {/* Price card */}
            <div className="bg-white rounded-lg p-6 shadow sticky top-4">
              <div className="text-4xl font-bold text-blue-600 mb-6">
                {formatPrice(property.price)}
              </div>

              {/* Agent info */}
              {property.agent && (
                <div className="border-t pt-6">
                  <h3 className="text-sm font-semibold text-gray-600 mb-2">
                    LISTED BY
                  </h3>
                  <p className="text-lg font-semibold">{property.agent.name}</p>
                  {property.agent.email && (
                    <p className="text-sm text-gray-600 mt-1">
                      {property.agent.email}
                    </p>
                  )}
                  {property.agent.phone && (
                    <p className="text-sm text-gray-600">
                      {property.agent.phone}
                    </p>
                  )}
                  {property.agent.office && (
                    <p className="text-sm text-gray-500 mt-2">
                      {property.agent.office.name}
                    </p>
                  )}
                </div>
              )}

              {/* Contact button */}
              <button className="w-full mt-6 bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition">
                Contact Agent
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
