/**
 * components/LazyImage.tsx
 *
 * Custom lazy loading component with Intersection Observer.
 * Shows a skeleton loader until the image enters the viewport.
 */

"use client";

import { useInView } from "react-intersection-observer";
import Image from "next/image";
import { useState } from "react";

interface LazyImageProps {
  src: string;
  alt: string;
  fill?: boolean;
  width?: number;
  height?: number;
  className?: string;
  sizes?: string;
}

export function LazyImage({
  src,
  alt,
  fill,
  width,
  height,
  className,
  sizes,
}: LazyImageProps) {
  const { ref, inView } = useInView({
    triggerOnce: true, // Load once, don't unload when scrolling back up
    rootMargin: "200px", // Start loading 200px before entering viewport
  });

  const [isLoading, setIsLoading] = useState(true);

  return (
    <div ref={ref} className="relative w-full h-full">
      {inView ? (
        <>
          {/* Skeleton loader - shows while image is loading */}
          {isLoading && (
            <div className="absolute inset-0 bg-gray-200 animate-pulse" />
          )}

          {/* Actual image */}
          <Image
            src={src}
            alt={alt}
            fill={fill}
            width={width}
            height={height}
            className={className}
            sizes={sizes}
            onLoadingComplete={() => setIsLoading(false)}
          />
        </>
      ) : (
        /* Placeholder before image enters viewport */
        <div className="w-full h-full bg-gray-200" />
      )}
    </div>
  );
}
