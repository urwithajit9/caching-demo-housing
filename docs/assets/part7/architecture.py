"""
diagrams/architecture_decision_tree.py

Generates a decision tree diagram showing how to choose between deployment paths.

Install dependencies:
    pip install diagrams

Run:
    python architecture_decision_tree.py

Output: architecture_decision_tree.png
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User

# Note: This uses text-based flow. For actual decision tree, you might want to use
# a different library or create it manually in a tool like Figma/Excalidraw

with Diagram("Deployment Architecture Decision Tree",
             filename="architecture_decision_tree",
             show=False,
             direction="TB"):

    user = User("Your Project")

    with Cluster("Budget?"):
        free = User("$0/month")
        small = User("$20/month")
        medium = User("$15-35/month")
        enterprise = User("$90+/month")

    with Cluster("Complexity Tolerance?"):
        low = User("Low (PaaS)")
        med = User("Medium (Split)")
        high = User("High (DIY)")

    with Cluster("Traffic?"):
        demo = User("<100 users/day")
        small_traffic = User("100-1k users/day")
        medium_traffic = User("1k-10k users/day")
        high_traffic = User(">10k users/day")

    with Cluster("Deployment Paths"):
        path0 = User("Path 0\nFree Tier\nRender+Neon+Upstash")
        path1 = User("Path 1\nRailway Only\n$20/month")
        path2 = User("Path 2\nVercel+Railway\n$15-35/month")
        path3 = User("Path 3\nAWS DIY\n$90+/month")

    # Decision flows
    user >> Edge(label="Budget=$0") >> free >> path0
    user >> Edge(label="Budget=$20") >> small >> path1
    user >> Edge(label="Need Performance") >> medium >> path2
    user >> Edge(label="Need Control") >> enterprise >> path3

    demo >> path0
    small_traffic >> path1
    medium_traffic >> path2
    high_traffic >> path3

print("✅ Diagram generated: architecture_decision_tree.png")