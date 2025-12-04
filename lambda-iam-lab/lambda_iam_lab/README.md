# Lambda IAM Lab - Code Structure

## Structure

```
lambda_iam_lab/
├── lambda_iam_lab_stack.py      # Main stack (38 lines)
├── constructs/                  # Reusable components
│   ├── s3_bucket.py            # S3 bucket (20 lines)
│   ├── iam_roles.py            # IAM roles (28 lines)
│   ├── lambda_function.py      # Lambda (31 lines)
│   └── outputs.py              # Outputs (21 lines)
└── lambda_code/
    └── handler.py              # Lambda code (28 lines)
```

## Flow

1. **S3 Bucket** - Creates encrypted bucket with auto-delete
2. **IAM Roles** - Creates Lambda + S3 roles
3. **Grant Access** - Links roles to bucket
4. **Lambda** - Creates function with bucket access
5. **Outputs** - Exports resource names/ARNs

## Quick Reference

| Modify | File |
|--------|------|
| Bucket | `constructs/s3_bucket.py` |
| Permissions | `constructs/iam_roles.py` |
| Lambda code | `lambda_code/handler.py` |
| Lambda config | `constructs/lambda_function.py` |
| Outputs | `constructs/outputs.py` |
| Flow | `lambda_iam_lab_stack.py` |
