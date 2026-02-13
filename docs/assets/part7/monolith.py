"""
diagrams/monolith_architecture.py

Generates architecture diagram for Path 1 (Railway Only - Monolith).

Install dependencies:
    pip install diagrams

Run:
    python monolith_architecture.py

Output: monolith_architecture.png
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.saas.cdn import Cloudflare
from diagrams.programming.framework import React, Django

with Diagram(
    "Path 1: Railway Only (Monolith)",
    filename="monolith_architecture",
    show=False,
    direction="LR",
):

    users = Users("Users")

    with Cluster("Railway Platform"):
        with Cluster("Frontend Service"):
            nextjs = React("Next.js\n(SSR)")

        with Cluster("Backend Service"):
            django_app = Django("Django\n+ Gunicorn")

        with Cluster("Database Service"):
            postgres = PostgreSQL("PostgreSQL\n(Managed)")

        with Cluster("Cache Service"):
            redis_cache = Redis("Redis\n(Managed)")

    cloudinary = Cloudflare("Cloudinary\nCDN")

    # Request flow
    users >> Edge(label="HTTPS") >> nextjs
    nextjs >> Edge(label="API calls") >> django_app
    django_app >> Edge(label="Queries") >> postgres
    django_app >> Edge(label="Cache") >> redis_cache
    django_app >> Edge(label="Images") >> cloudinary

    # Notes
    # All services on one platform
    # Simple management, single dashboard
    # Automatic SSL and deployments

print("✅ Diagram generated: monolith_architecture.png")
