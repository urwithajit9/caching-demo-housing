"""
diagrams/aws_full_architecture.py

Generates architecture diagram for Path 3 (AWS DIY).

Install dependencies:
    pip install diagrams

Run:
    python aws_full_architecture.py

Output: aws_full_architecture.png
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.aws.network import Route53, ELB, VPC, InternetGateway
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.security import CertificateManager
from diagrams.onprem.inmemory import Redis
from diagrams.saas.cdn import Cloudflare

with Diagram(
    "Path 3: AWS DIY (Enterprise)",
    filename="aws_full_architecture",
    show=False,
    direction="TB",
):

    users = Users("Users")
    dns = Route53("Route 53\nDNS")
    ssl = CertificateManager("ACM\nSSL Cert")
    cdn = CloudFront("CloudFront\nCDN")

    with Cluster("AWS Region (us-east-1)"):
        with Cluster("VPC"):
            igw = InternetGateway("Internet\nGateway")
            alb = ELB("Application\nLoad Balancer")

            with Cluster("Public Subnet"):
                ec2_1 = EC2("Django EC2\n+ Nginx\n+ Gunicorn")
                ec2_2 = EC2("Django EC2\n(Auto-scaled)")

            with Cluster("Private Subnet - Data"):
                rds = RDS("RDS PostgreSQL\n(Multi-AZ)")
                elasticache = Redis("ElastiCache\nRedis")

            with Cluster("Private Subnet - Storage"):
                s3 = S3("S3 Bucket\nStatic Files")

    cloudinary = Cloudflare("Cloudinary\nImages CDN")

    # Request flow
    users >> dns >> ssl >> cdn
    cdn >> Edge(label="Cache miss") >> igw >> alb
    alb >> [ec2_1, ec2_2]

    ec2_1 >> rds
    ec2_1 >> elasticache
    ec2_2 >> rds
    ec2_2 >> elasticache

    ec2_1 >> Edge(label="Static files") >> s3 >> cdn
    ec2_1 >> Edge(label="Images") >> cloudinary

print("✅ Diagram generated: aws_full_architecture.png")
print("This shows full AWS setup with VPC, security, scaling, and redundancy")
