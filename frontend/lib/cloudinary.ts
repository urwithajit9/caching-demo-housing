/**
 * lib/cloudinary.ts
 *
 * Helper functions for Cloudinary URL transformations.
 */

/**
 * Generate a tiny blurred version of a Cloudinary image for use as a placeholder.
 * Returns a 20px-wide, heavily blurred version.
 */
export function getCloudinaryBlurURL(url: string): string {
  if (!url || !url.includes("res.cloudinary.com")) {
    // Not a Cloudinary URL, return a solid color data URL
    return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2UwZTBlMCIvPjwvc3ZnPg==";
  }

  // Parse the URL and inject blur transformation
  // Cloudinary URL format: https://res.cloudinary.com/{cloud_name}/image/upload/{transformations}/{path}
  const parts = url.split("/upload/");
  if (parts.length !== 2) return url; // Invalid format, return as-is

  const [base, path] = parts;

  // Build blur transformation: width=20, quality=1, blur=1000
  const blurTransformation = "w_20,q_1,e_blur:1000";

  return `${base}/upload/${blurTransformation}/${path}`;
}
