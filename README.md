# AWS IAM Role Cloner

A Python script for cloning an AWS IAM role—including its trust policies, inline policies, and attached managed policies.

## Features
- **Clones Trust Policies:** Copies the source role’s trust policy.
- **Inline Policies:** Retrieves and clones all inline policies attached to the source role.
- **Managed Policies:** Attaches all managed policies from the source role to the new role.
- **Create Tag:** A tag (clonedFrom) is created to the cloned role with the source role name as value. 
- **Automatic Naming:** Defaults to `<source_role>_cloned` when no new role name is provided.

## Prerequisites
- **Python 3.10+**
- **boto3** library  

- AWS credentials configured (using AWS CLI or environment variables) with permissions to manage IAM roles, including:
	-	iam:GetRole
	-	iam:CreateRole
	-	iam:ListRolePolicies
	-	iam:GetRolePolicy
	-	iam:PutRolePolicy
	-	iam:ListAttachedRolePolicies
	-	iam:AttachRolePolicy
    -   iam.tag_role

## Installation & Usage

**Clone the repository:**
```bash
git clone https://github.com/sgrilux/aws-iam-role-cloner.git
cd aws-iam-role-cloner
```

**Make the script executable (on Unix/Linux):**
```bash
chmod +x clone_iam_role.py
```

**Create the Virtual Environment**
```bash
python3 -m venv venv
```

**Activate the Virtual Environment**
```bash
source venv/bin/activate
```

**Install Dependencies**
Once the virtual environment is activated, install the required libraries:
```bash
pip install boto3
```

**Run the script** by providing the source IAM role name and an optional new role name:

```bash
./clone_iam_role.py <source_role_name> [new_role_name]
```

**Example**
```bash
./clone_iam_role.py MySourceRole MyClonedRole
```

If the new_role_name is omitted, the script will create a role named MySourceRole_cloned.

## How It Works

**1. Retrieve Source Role:**

Uses iam.get_role to obtain the source role’s details (trust policy, description, max session duration).

**2. Create New Role:**

Calls iam.create_role to create a new role with the same trust policy and settings as the source role.

**3. Clone Inline Policies:**
Lists and copies all inline policies from the source role using `iam.list_role_policies` and `iam.put_role_policy`.

**4. Attach Managed Policies:**

Retrieves and attaches all managed policies from the source role using `iam.list_attached_role_policies` and `iam.attach_role_policy`.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue in the repository.
