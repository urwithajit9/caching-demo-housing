/**
 * components/ImageGallery.tsx
 *
 * Image gallery with main image and thumbnail strip.
 * Click thumbnails to change the main image.
 */

"use client";

import { useState } from "react";
import Image from "next/image";
import type { PropertyImage } from "@/types/property";

interface ImageGalleryProps {
  images: PropertyImage[];
}

export function ImageGallery({ images }: ImageGalleryProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  if (!images || images.length === 0) {
    return (
      <div className="w-full h-96 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-4xl font-bold">
        No Images
      </div>
    );
  }

  const currentImage = images[currentIndex];

  return (
    <div className="space-y-4">
      {/* Main image */}
      <div className="relative w-full h-96 bg-gray-100 rounded-lg overflow-hidden">
        <Image
          src={currentImage.webp_url || currentImage.original_url}
          alt={currentImage.alt_text || "Property image"}
          fill
          className="object-contain"
          priority // Load first image immediately
          sizes="100vw"
        />

        {/* Navigation arrows (if more than 1 image) */}
        {images.length > 1 && (
          <>
            <button
              onClick={() =>
                setCurrentIndex(
                  (currentIndex - 1 + images.length) % images.length,
                )
              }
              className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white p-2 rounded-full shadow-lg"
              aria-label="Previous image"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </button>
            <button
              onClick={() =>
                setCurrentIndex((currentIndex + 1) % images.length)
              }
              className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white p-2 rounded-full shadow-lg"
              aria-label="Next image"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          </>
        )}

        {/* Image counter */}
        <div className="absolute bottom-4 right-4 bg-black/70 text-white px-3 py-1 rounded-full text-sm">
          {currentIndex + 1} / {images.length}
        </div>
      </div>

      {/* Thumbnail strip */}
      {images.length > 1 && (
        <div className="flex gap-2 overflow-x-auto pb-2">
          {images.map((image, index) => (
            <button
              key={image.id}
              onClick={() => setCurrentIndex(index)}
              className={`relative flex-shrink-0 w-24 h-18 rounded overflow-hidden ${
                index === currentIndex
                  ? "ring-2 ring-blue-600"
                  : "opacity-60 hover:opacity-100"
              }`}
            >
              <Image
                src={
                  image.thumbnail_url || image.webp_url || image.original_url
                }
                alt={image.alt_text || `Thumbnail ${index + 1}`}
                fill
                className="object-cover"
                sizes="96px"
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
