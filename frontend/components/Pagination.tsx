/**
 * components/Pagination.tsx
 *
 * Pagination controls for browsing through paginated results.
 */

"use client";

import { useRouter, useSearchParams } from "next/navigation";

interface PaginationProps {
  count: number;
  next: string | null;
  previous: string | null;
}

export function Pagination({ count, next, previous }: PaginationProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const currentPage = parseInt(searchParams.get("page") || "1");
  const pageSize = 20; // DRF default
  const totalPages = Math.ceil(count / pageSize);

  const goToPage = (page: number) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set("page", page.toString());
    router.push(`/?${params.toString()}`);
  };

  if (totalPages <= 1) {
    // Don't show pagination if there's only one page
    return null;
  }

  return (
    <div className="mt-8 flex items-center justify-center gap-2">
      {/* Previous button */}
      <button
        onClick={() => goToPage(currentPage - 1)}
        disabled={!previous}
        className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Previous
      </button>

      {/* Page numbers */}
      <div className="flex items-center gap-2">
        {/* First page */}
        {currentPage > 2 && (
          <>
            <button
              onClick={() => goToPage(1)}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              1
            </button>
            {currentPage > 3 && <span className="text-gray-500">...</span>}
          </>
        )}

        {/* Previous page number */}
        {currentPage > 1 && (
          <button
            onClick={() => goToPage(currentPage - 1)}
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            {currentPage - 1}
          </button>
        )}

        {/* Current page (highlighted) */}
        <button
          disabled
          className="px-4 py-2 border-2 border-blue-600 rounded-md text-blue-600 bg-blue-50 font-semibold"
        >
          {currentPage}
        </button>

        {/* Next page number */}
        {currentPage < totalPages && (
          <button
            onClick={() => goToPage(currentPage + 1)}
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            {currentPage + 1}
          </button>
        )}

        {/* Last page */}
        {currentPage < totalPages - 1 && (
          <>
            {currentPage < totalPages - 2 && (
              <span className="text-gray-500">...</span>
            )}
            <button
              onClick={() => goToPage(totalPages)}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              {totalPages}
            </button>
          </>
        )}
      </div>

      {/* Next button */}
      <button
        onClick={() => goToPage(currentPage + 1)}
        disabled={!next}
        className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Next
      </button>
    </div>
  );
}
