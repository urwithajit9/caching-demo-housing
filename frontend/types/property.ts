/**
 * types/property.ts
 *
 * TypeScript interfaces that mirror the Django serializers.
 * These define the shape of the data we get from the API.
 */

export interface Location {
  id: number;
  city: string;
  state: string;
  zip_code: string;
}

export interface Office {
  id: number;
  name: string;
  city: string;
  phone: string;
}

export interface Agent {
  id: number;
  name: string;
  email: string;
  phone: string;
  office: Office;
}

export interface Property {
  id: number;
  title: string;
  description: string;
  property_type: "apartment" | "house" | "villa" | "studio" | "condo";
  price: string; // Django returns this as a string: "450000.00"
  bedrooms: number;
  bathrooms: number;
  location: Location;
  agent: Agent;
  status: "available" | "pending" | "sold";
  view_count: number;
  created_at: string; // ISO 8601 date string
}

// PaginatedResponse<T> is a generic interface. It works with any type.
// PaginatedResponse<Property> means a paginated response where results is an array of Property objects.

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
