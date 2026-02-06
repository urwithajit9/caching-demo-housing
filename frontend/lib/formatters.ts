/**
 * lib/formatters.ts
 *
 * Utility functions for formatting data for display.
 */

/**
 * Format a price string from the API into a readable currency format.
 * Input: "450000.00"
 * Output: "$450,000"
 */
export function formatPrice(price: string): string {
  const numericPrice = parseFloat(price);
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0, // No cents
    maximumFractionDigits: 0,
  }).format(numericPrice);
}

/**
 * Format a date string into a readable format.
 * Input: "2024-01-15T10:30:00Z"
 * Output: "Jan 15, 2024"
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(date);
}

/**
 * Capitalize the first letter of each word.
 * Input: "apartment"
 * Output: "Apartment"
 */
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
