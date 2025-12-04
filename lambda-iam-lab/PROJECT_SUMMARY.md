# AWS Lambda & S3 with IAM Roles - Project Summary

## 🎯 Project Overview

This project demonstrates Infrastructure as Code (IaC) using AWS CDK to create:
- Lambda function with S3 access
- IAM roles with least-privilege permissions
- S3 bucket with encryption
- **Clean destroy capability** - no orphaned resources!

## 📁 Project Structure

```
lambda-iam-lab/
├── app.py                          # CDK app entry point
├── lambda_iam_lab/
│   ├── __init__.py
│   └── lambda_iam_lab_stack.py    # Main infrastructure stack
├── tests/                          # Unit tests
├── cdk.json                        # CDK configuration
├── requirements.txt                # Python dependencies
├── DEPLOYMENT.md                   # Detailed deployment guide
├── QUICK_START.md                  # Quick reference
├── ARCHITECTURE.md                 # Architecture documentation
└── PROJECT_SUMMARY.md              # This file
```

## 🚀 Quick Commands

```bash
# Setup
cdk bootstrap                  # One-time AWS setup

# Deploy
source .venv/bin/activate     # Activate Python environment
cdk synth                      # Preview CloudFormation template
cdk deploy                     # Deploy to AWS

# Manage
cdk diff                       # Compare with deployed version
cdk ls                         # List stacks

# Destroy
cdk destroy                    # Remove all resources cleanly
```

## 🏗️ What Gets Created

### 1. S3 Bucket
```python
✓ Encryption: AES256 (SSE-S3)
✓ Auto-delete objects: Enabled
✓ Removal policy: DESTROY
✓ Cost: Free tier eligible
```

### 2. Lambda Function
```python
✓ Runtime: Python 3.11
✓ Memory: 128 MB
✓ Timeout: 30 seconds
✓ Function: Lists S3 objects
✓ Cost: Free tier eligible (1M requests/month)
```

### 3. IAM Roles

**LambdaExecutionRole:**
- CloudWatch Logs (write)
- S3 bucket (read/write)
- Trust: lambda.amazonaws.com

**S3AccessRole:**
- S3 bucket (read/write)
- Trust: Your AWS account

## ✨ Key Features

### 1. Clean Destroy ⭐
```python
removal_policy=RemovalPolicy.DESTROY
auto_delete_objects=True
```
**Result:** `cdk destroy` removes EVERYTHING, including S3 objects!

### 2. Least Privilege Security
- No wildcard permissions
- Bucket-specific access only
- Service principal authentication

### 3. Infrastructure as Code
- Version controlled
- Reproducible deployments
- Easy to modify and extend

### 4. Cost Optimized
- All resources within AWS Free Tier
- Estimated cost: <$1/month for light usage

## 📊 Outputs After Deployment

```
LambdaIamLabStack.BucketName = lambdaiamlab-lambdadatabucket123abc
LambdaIamLabStack.LambdaFunctionName = LambdaIamLabStack-S3ProcessorFunction456def
LambdaIamLabStack.LambdaRoleArn = arn:aws:iam::123456789012:role/...
LambdaIamLabStack.S3RoleArn = arn:aws:iam::123456789012:role/...
```

## 🧪 Testing

### Test Lambda Function
```bash
aws lambda invoke \
  --function-name <FUNCTION_NAME> \
  --payload '{}' \
  output.json

cat output.json
```

Expected output:
```json
{
    "statusCode": 200,
    "body": "{\"message\": \"Successfully accessed bucket: ...\", \"object_count\": 0}"
}
```

### Test S3 Access
```bash
# Upload a file
echo "test" > test.txt
aws s3 cp test.txt s3://<BUCKET_NAME>/

# List objects
aws s3 ls s3://<BUCKET_NAME>/

# Test Lambda again - should show 1 object
aws lambda invoke --function-name <FUNCTION_NAME> --payload '{}' output.json
```

## 🔐 Security Best Practices Implemented

✅ **Encryption at Rest**: S3 bucket uses AES256  
✅ **Least Privilege**: Minimal necessary permissions  
✅ **No Hardcoded Credentials**: IAM roles for authentication  
✅ **CloudWatch Logging**: All Lambda invocations logged  
✅ **Resource Cleanup**: Auto-delete prevents orphaned resources  
✅ **Separate Concerns**: Different roles for different purposes  

## 💰 Cost Breakdown

| Service | Free Tier | Pricing After Free Tier |
|---------|-----------|------------------------|
| Lambda | 1M requests/month | $0.20 per 1M requests |
| S3 | 5 GB storage | $0.023 per GB/month |
| CloudWatch Logs | 5 GB | $0.50 per GB ingested |
| IAM Roles | Unlimited | Free |

**Typical Monthly Cost**: $0 (within free tier)

## 🛠️ Common Customizations

### Change Lambda Runtime
```python
runtime=lambda_.Runtime.PYTHON_3_12
```

### Add DynamoDB Access
```python
lambda_role.add_managed_policy(
    iam.ManagedPolicy.from_aws_managed_policy_name(
        "AmazonDynamoDBReadOnlyAccess"
    )
)
```

### Enable S3 Versioning
```python
versioned=True
```

### Change Region
```python
# In app.py
env=cdk.Environment(account='123456789012', region='us-west-2')
```

## 📚 Documentation Files

- **QUICK_START.md**: Fast deployment (3 steps)
- **DEPLOYMENT.md**: Complete deployment guide
- **ARCHITECTURE.md**: System architecture and diagrams
- **PROJECT_SUMMARY.md**: This overview

## 🐛 Troubleshooting

### "CDK not bootstrapped"
```bash
cdk bootstrap
```

### "Access Denied" during deploy
Ensure AWS credentials have:
- IAM: CreateRole, PutRolePolicy
- S3: CreateBucket
- Lambda: CreateFunction
- CloudFormation: Full access

### Stack fails to delete
```bash
# Check CloudFormation console for errors
# Usually auto-resolves with auto_delete_objects=True
```

## �� What You Learned

1. ✅ How to create IAM roles for Lambda
2. ✅ How to grant S3 permissions to Lambda
3. ✅ How to use AWS CDK with Python
4. ✅ How to implement clean resource destruction
5. ✅ How to follow AWS security best practices
6. ✅ How to use Infrastructure as Code

## 🔗 Useful Links

- [AWS CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [S3 User Guide](https://docs.aws.amazon.com/s3/index.html)

## 📝 License

This is a learning/demonstration project. Feel free to use and modify as needed.

## 🤝 Contributing

This is a lab project, but suggestions are welcome!

---

**Happy Cloud Computing! ☁️**
