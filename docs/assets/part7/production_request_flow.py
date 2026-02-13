"""
diagrams/production_request_flow.py

Generates detailed request flow diagram showing all caching layers.

Install dependencies:
    pip install diagrams

Run:
    python production_request_flow.py

Output: production_request_flow.png
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import React, Django
from diagrams.saas.cdn import Cloudflare

with Diagram(
    "Complete Production Request Flow (Vercel + Railway)",
    filename="production_request_flow",
    show=False,
    direction="LR",
):

    user = User("User Browser")

    with Cluster("Layer 1: Browser Cache (SWR)"):
        swr_cache = React("SWR Cache\n0ms (instant)")

    with Cluster("Layer 2: Vercel Edge (Nearest CDN)"):
        vercel_edge = React("Next.js SSR\n~20ms")

    with Cluster("Layer 3: Railway Backend"):
        django_app = Django("Django API\n~10ms")

        with Cluster("Layer 4: Redis Cache"):
            redis_cache = Redis("Redis\n~4ms")

        with Cluster("Layer 5: Database"):
            postgres = PostgreSQL("PostgreSQL\n~15ms (optimized)")

    with Cluster("Layer 6: Image CDN"):
        cloudinary = Cloudflare("Cloudinary\n~10ms (edge)")

    # First request (cache miss everywhere)
    user >> Edge(label="1. First request", color="red") >> swr_cache
    swr_cache >> Edge(label="2. Cache miss", color="red") >> vercel_edge
    vercel_edge >> Edge(label="3. SSR", color="red") >> django_app
    django_app >> Edge(label="4. Cache miss", color="red") >> redis_cache
    redis_cache >> Edge(label="5. Query DB", color="red") >> postgres
    postgres >> Edge(label="6. Return data", color="green") >> redis_cache
    redis_cache >> Edge(label="7. Cache", color="green") >> django_app
    django_app >> Edge(label="8. Return JSON", color="green") >> vercel_edge
    vercel_edge >> Edge(label="9. Render", color="green") >> swr_cache
    swr_cache >> Edge(label="10. Display", color="green") >> user

    # Image requests
    user >> Edge(label="11. Image request", color="blue", style="dashed") >> cloudinary
    (
        cloudinary
        >> Edge(label="12. Optimized image", color="blue", style="dashed")
        >> user
    )

    # Second request (all caches warm)
    (
        user
        >> Edge(label="13. Second request", color="purple", style="dotted")
        >> swr_cache
    )
    swr_cache >> Edge(label="14. Instant (0ms)", color="purple", style="dotted") >> user

print("✅ Diagram generated: production_request_flow.png")
print("This shows the complete request lifecycle through all caching layers")
