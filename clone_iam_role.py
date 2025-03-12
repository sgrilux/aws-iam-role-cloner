#!/usr/bin/env python3
import sys
import argparse
import json
import boto3
from botocore.exceptions import ClientError
from typing import Any


def clone_iam_role(source_role: str, new_role: str) -> None:
    iam = boto3.client("iam")

    try:
        # Retrieve source role details
        response: dict[str, Any] = iam.get_role(RoleName=source_role)
        source_role_data: dict[str, Any] = response["Role"]
    except ClientError as e:
        print(f"Error retrieving role {source_role}: {e}")
        sys.exit(1)

    # Get the assume role policy document from the source role
    assume_role_policy = source_role_data["AssumeRolePolicyDocument"]
    description: str = source_role_data.get("Description", "")
    max_session_duration: int = source_role_data.get("MaxSessionDuration", 3600)

    try:
        iam.create_role(
            RoleName=new_role,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            Description=description,
            MaxSessionDuration=max_session_duration,
        )
        print(f"Created new role: {new_role}")
    except ClientError as e:
        print(f"Error creating role {new_role}: {e}")
        sys.exit(1)

    # Clone inline policies
    try:
        inline_policies = iam.list_role_policies(RoleName=source_role)["PolicyNames"]
        for policy_name in inline_policies:
            policy = iam.get_role_policy(
                RoleName=source_role, PolicyName=policy_name
            )["PolicyDocument"]
            iam.put_role_policy(
                RoleName=new_role,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy),
            )
            print(f"Cloned inline policy: {policy_name}")
    except ClientError as e:
        print(f"Error cloning inline policies: {e}")
        sys.exit(1)

    # Clone attached managed policies
    try:
        attached_policies = iam.list_attached_role_policies(RoleName=source_role)[
            "AttachedPolicies"
        ]
        for policy in attached_policies:
            policy_arn = policy["PolicyArn"]
            iam.attach_role_policy(RoleName=new_role, PolicyArn=policy_arn)
            print(f"Attached managed policy: {policy_arn}")
    except ClientError as e:
        print(f"Error cloning attached policies: {e}")
        sys.exit(1)

    # Add Tag to the new role with the value of the source role
    try:
        iam.tag_role(
            RoleName=new_role,
            Tags=[{"Key": "clonedFrom", "Value": source_role}],
        )
        print(f"Added tag to the new role: {new_role}") 
    except ClientError as e:
        print(f"Error adding tag to the new role: {e}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Clone an AWS IAM role.")
    parser.add_argument(
        "source_role", help="The name of the source IAM role to clone"
    )
    parser.add_argument(
        "new_role",
        nargs="?",
        help="The name for the new IAM role. If not provided, '_cloned' is appended to the source role name.",
    )
    args = parser.parse_args()

    source_role: str = args.source_role
    new_role: str = args.new_role if args.new_role else f"{source_role}_cloned"

    clone_iam_role(source_role, new_role)


if __name__ == "__main__":
    main()
