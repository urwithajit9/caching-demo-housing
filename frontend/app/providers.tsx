/**
 * app/providers.tsx
 *
 * Client component that wraps the app with SWR configuration.
 */

"use client";

import { SWRConfig } from "swr";
import { fetcher } from "@/lib/fetcher";
import { ReactNode } from "react";

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <SWRConfig
      value={{
        fetcher, // Default fetcher for all useSWR calls
        revalidateOnFocus: false, // Don't refetch when user focuses the tab
        revalidateOnReconnect: true, // Refetch when internet reconnects
        dedupingInterval: 2000, // Don't refetch same endpoint within 2 seconds
      }}
    >
      {children}
    </SWRConfig>
  );
}
