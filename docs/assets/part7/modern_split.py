"""
diagrams/vercel_railway_architecture.py

Generates architecture diagram for Path 2 (Vercel + Railway - Optimal).

Install dependencies:
    pip install diagrams

Run:
    python vercel_railway_architecture.py

Output: vercel_railway_architecture.png
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.saas.cdn import Cloudflare
from diagrams.programming.framework import React, Django
from diagrams.onprem.network import Internet

with Diagram(
    "Path 2: Vercel + Railway (Recommended)",
    filename="vercel_railway_architecture",
    show=False,
    direction="TB",
):

    users = Users("Global Users")
    internet = Internet("Internet")

    with Cluster("Vercel Edge Network (100+ Locations)"):
        edge_us = React("Edge\nUS East")
        edge_eu = React("Edge\nEU West")
        edge_asia = React("Edge\nAsia Pacific")
        edge_nodes = [edge_us, edge_eu, edge_asia]

    with Cluster("Railway (US-East)"):
        with Cluster("Backend Service"):
            django_app = Django("Django API\n+ Gunicorn")

        with Cluster("Database"):
            postgres = PostgreSQL("PostgreSQL")

        with Cluster("Cache"):
            redis_cache = Redis("Redis")

    cloudinary = Cloudflare("Cloudinary CDN\n(Global)")

    # Request flow
    users >> internet
    internet >> Edge(label="Nearest edge") >> edge_nodes

    for edge in edge_nodes:
        edge >> Edge(label="API calls", style="dashed") >> django_app

    django_app >> postgres
    django_app >> redis_cache
    django_app >> Edge(label="Images") >> cloudinary

    # Return path
    cloudinary >> Edge(label="Images", style="dotted") >> edge_nodes

print("✅ Diagram generated: vercel_railway_architecture.png")
print("This shows the optimal split: frontend on edge, backend centralized")
