# Quick Start Guide

## Deploy in 3 Steps

### 1. Bootstrap (First time only)
```bash
cdk bootstrap
```

### 2. Deploy
```bash
source .venv/bin/activate
cdk deploy
```

### 3. Test
```bash
# Get the bucket name and function name from the deployment outputs
aws lambda invoke --function-name <FUNCTION_NAME> --payload '{}' output.json
cat output.json
```

## Destroy Everything
```bash
cdk destroy
```

That's it! All resources including S3 objects are automatically cleaned up.

## What You Get

- ✅ S3 Bucket (with encryption)
- ✅ Lambda Function (Python 3.11)
- ✅ IAM Role for Lambda (with S3 access)
- ✅ IAM Role for S3 (standalone)
- ✅ CloudWatch Logs
- ✅ Automatic cleanup on destroy

## Verify AWS Credentials
```bash
aws sts get-caller-identity
```

## View Stack Resources
```bash
aws cloudformation describe-stack-resources --stack-name LambdaIamLabStack
```

For detailed information, see [DEPLOYMENT.md](DEPLOYMENT.md)
