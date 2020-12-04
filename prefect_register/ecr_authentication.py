import boto3
import base64
import subprocess


def ecr_authenticate():
    aws_session = boto3.Session()
    ecr_client = aws_session.client("ecr")

    ecr_credentials = ecr_client.get_authorization_token()["authorizationData"][0]

    ecr_username = "AWS"

    ecr_password = (
        base64.b64decode(ecr_credentials["authorizationToken"])
        .replace(b"AWS:", b"")
        .decode("utf-8")
    )

    ecr_url = ecr_credentials["proxyEndpoint"]

    subprocess.run(["docker", "login", "-u", ecr_username, "-p", ecr_password, ecr_url])
