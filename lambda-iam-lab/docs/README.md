# AWS Lambda & IAM Role Lab with Clean Destroy

> **Infrastructure as Code** project demonstrating AWS Lambda, S3, and IAM roles using AWS CDK with Python.

## 🎯 Project Goal

Create a fully functional AWS infrastructure with:
- ✅ Lambda function that accesses S3
- ✅ Proper IAM roles with least-privilege permissions
- ✅ **Clean destroy** - all resources deleted cleanly (including S3 objects!)

## 🚀 Quick Start

```bash
# 1. Bootstrap AWS (first time only)
cdk bootstrap

# 2. Deploy
source .venv/bin/activate
cdk deploy

# 3. Destroy (clean removal)
cdk destroy
```

👉 **See [QUICK_START.md](QUICK_START.md) for detailed 3-step guide**

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](QUICK_START.md) | Fast 3-step deployment |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Complete deployment guide |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture & diagrams |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Comprehensive project overview |

## 🏗️ What This Creates

```
AWS Resources Created:
├── S3 Bucket (encrypted, auto-delete enabled)
├── Lambda Function (Python 3.11)
│   └── Lists objects in S3 bucket
├── IAM Role: LambdaExecutionRole
│   ├── CloudWatch Logs access
│   └── S3 read/write access
└── IAM Role: S3AccessRole
    └── S3 read/write access
```

## ⭐ Key Features

### 1. Clean Destroy
```python
removal_policy=RemovalPolicy.DESTROY
auto_delete_objects=True
```
**No orphaned resources!** The S3 bucket and all its objects are automatically deleted when you run `cdk destroy`.

### 2. Security Best Practices
- ✅ Encryption at rest (AES256)
- ✅ Least privilege IAM permissions
- ✅ No hardcoded credentials
- ✅ CloudWatch logging enabled

### 3. Cost Optimized
- All resources within AWS Free Tier
- Estimated cost: **$0/month** for typical usage

## 🧪 Test Your Deployment

```bash
# Invoke Lambda function
aws lambda invoke \
  --function-name <FUNCTION_NAME> \
  --payload '{}' \
  output.json

# Upload test file to S3
echo "Hello" > test.txt
aws s3 cp test.txt s3://<BUCKET_NAME>/

# Check Lambda sees the file
aws lambda invoke \
  --function-name <FUNCTION_NAME> \
  --payload '{}' \
  output.json
```

## 📦 Project Structure

```
lambda-iam-lab/
├── app.py                      # CDK entry point
├── lambda_iam_lab/
│   └── lambda_iam_lab_stack.py # Infrastructure definition
├── cdk.json                    # CDK configuration
├── requirements.txt            # Dependencies
└── docs/                       # Documentation
```

## 🛠️ Requirements

- AWS Account with configured credentials
- AWS CLI installed
- Node.js & npm (for CDK CLI)
- Python 3.x
- AWS CDK (`npm install -g aws-cdk`)

## 📊 Stack Outputs

After deployment, you'll see:
```
✅ LambdaIamLabStack.BucketName = lambdaiamlab-lambdadatabucket...
✅ LambdaIamLabStack.LambdaFunctionName = LambdaIamLabStack-S3Processor...
✅ LambdaIamLabStack.LambdaRoleArn = arn:aws:iam::123456789012:role/...
✅ LambdaIamLabStack.S3RoleArn = arn:aws:iam::123456789012:role/...
```

## 🔐 IAM Permissions

### Lambda Execution Role
- **CloudWatch Logs**: Write logs
- **S3 Bucket**: Read/Write access (specific bucket only)
- **Trust**: lambda.amazonaws.com

### S3 Access Role
- **S3 Bucket**: Read/Write access (specific bucket only)
- **Trust**: Your AWS Account (for AssumeRole)

## 💡 Why This Matters

Traditional S3 bucket deletion requires manual cleanup:
```bash
# ❌ Old way - manual cleanup required
aws s3 rm s3://bucket-name --recursive
aws s3 rb s3://bucket-name
aws cloudformation delete-stack --stack-name MyStack
```

With this CDK setup:
```bash
# ✅ New way - automatic cleanup
cdk destroy
```

**Everything is removed automatically!**

## 🎓 What You'll Learn

1. How to create IAM roles for AWS services
2. How to grant S3 permissions to Lambda
3. How to use AWS CDK with Python
4. How to implement clean resource destruction
5. Infrastructure as Code best practices
6. AWS security best practices

## 🐛 Troubleshooting

### CDK not found
```bash
npm install -g aws-cdk
```

### Not bootstrapped
```bash
cdk bootstrap
```

### Access denied
Ensure your AWS credentials have permissions for:
- IAM, S3, Lambda, CloudFormation

## 📝 Useful Commands

```bash
cdk ls          # List stacks
cdk synth       # Show CloudFormation template
cdk deploy      # Deploy to AWS
cdk diff        # Compare with deployed version
cdk destroy     # Remove all resources
cdk doctor      # Check CDK setup
```

## 🌟 Next Steps

1. **Deploy the stack**: Follow [QUICK_START.md](QUICK_START.md)
2. **Explore the code**: Check `lambda_iam_lab/lambda_iam_lab_stack.py`
3. **Customize**: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for customization options
4. **Extend**: Add more AWS services (DynamoDB, API Gateway, etc.)

## 📚 Additional Resources

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

## 🤝 Contributing

This is a learning/lab project. Suggestions and improvements welcome!

## 📄 License

Educational/demonstration project - feel free to use and modify.

---

**Built with ❤️ using AWS CDK**

**Ready to deploy?** → Start with [QUICK_START.md](QUICK_START.md)
