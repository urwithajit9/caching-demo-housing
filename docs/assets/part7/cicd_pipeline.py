"""
diagrams/cicd_pipeline.py

Generates CI/CD pipeline diagram showing automated deployment flow.

Install dependencies:
    pip install diagrams

Run:
    python cicd_pipeline.py

Output: cicd_pipeline.png
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions
from diagrams.programming.framework import React, Django
from diagrams.saas.chat import Slack
from diagrams.generic.device import Mobile

with Diagram(
    "CI/CD Pipeline Flow", filename="cicd_pipeline", show=False, direction="LR"
):

    developer = Mobile("Developer")
    github = Github("GitHub\nRepository")

    with Cluster("GitHub Actions"):
        trigger = GithubActions("Trigger\non Push")

        with Cluster("Backend Pipeline"):
            backend_test = GithubActions("Run Tests")
            backend_lint = GithubActions("Lint Code")
            backend_deploy = GithubActions("Deploy to\nRailway")
            backend_migrate = GithubActions("Run\nMigrations")

        with Cluster("Frontend Pipeline"):
            frontend_test = GithubActions("Run Tests")
            frontend_build = GithubActions("Build Next.js")
            frontend_deploy = GithubActions("Deploy to\nVercel")

    railway = Django("Railway\nBackend")
    vercel = React("Vercel\nFrontend")
    slack = Slack("Slack\nNotification")

    # Flow
    developer >> Edge(label="git push") >> github
    github >> trigger

    # Backend flow
    trigger >> backend_test
    backend_test >> Edge(label="if pass") >> backend_lint
    backend_lint >> Edge(label="if pass") >> backend_deploy
    backend_deploy >> railway
    railway >> Edge(label="after deploy") >> backend_migrate

    # Frontend flow
    trigger >> frontend_test
    frontend_test >> Edge(label="if pass") >> frontend_build
    frontend_build >> Edge(label="if pass") >> frontend_deploy
    frontend_deploy >> vercel

    # Notifications
    backend_migrate >> Edge(label="success/fail", style="dashed") >> slack
    vercel >> Edge(label="success/fail", style="dashed") >> slack

print("✅ Diagram generated: cicd_pipeline.png")
print("This shows automated deployment flow from git push to production")
