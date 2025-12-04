# AWS IAM Role Lab

> Complete AWS CDK project demonstrating Lambda functions, S3 buckets, and IAM roles with Infrastructure as Code

## 📂 Repository Structure

```
aws-iam-role/
├── README.md                    # This file
├── Steps.MD                     # Complete setup documentation
└── lambda-iam-lab/             # CDK project folder
    ├── README.md               # Project overview
    ├── QUICK_START.md          # 3-step deployment
    ├── DEPLOYMENT.md           # Detailed guide
    ├── ARCHITECTURE.md         # System architecture
    ├── PROJECT_SUMMARY.md      # Complete summary
    ├── app.py                  # CDK entry point
    ├── lambda_iam_lab/         # Infrastructure stack
    │   └── lambda_iam_lab_stack.py
    ├── cdk.json                # CDK configuration
    └── requirements.txt        # Dependencies
```

## 🎯 What This Project Does

Creates a complete AWS infrastructure with:
- ✅ **Lambda Function** - Python 3.11 that lists S3 objects
- ✅ **S3 Bucket** - Encrypted with auto-delete enabled
- ✅ **IAM Roles** - Proper permissions for Lambda and S3 access
- ✅ **Clean Destroy** - One command removes everything (including S3 objects!)

## 🚀 Quick Start

```bash
# Navigate to project
cd lambda-iam-lab

# Activate virtual environment
source .venv/bin/activate

# Bootstrap AWS (first time only)
cdk bootstrap

# Deploy infrastructure
cdk deploy

# Destroy everything cleanly
cdk destroy
```

## 📚 Documentation

| File | Description |
|------|-------------|
| [Steps.MD](./Steps.MD) | Complete setup and deployment steps |
| [lambda-iam-lab/README.md](./lambda-iam-lab/README.md) | Main project documentation |
| [lambda-iam-lab/QUICK_START.md](./lambda-iam-lab/QUICK_START.md) | 3-step deployment guide |
| [lambda-iam-lab/DEPLOYMENT.md](./lambda-iam-lab/DEPLOYMENT.md) | Detailed deployment instructions |
| [lambda-iam-lab/ARCHITECTURE.md](./lambda-iam-lab/ARCHITECTURE.md) | Architecture diagrams |
| [lambda-iam-lab/PROJECT_SUMMARY.md](./lambda-iam-lab/PROJECT_SUMMARY.md) | Comprehensive overview |

## ⭐ Key Features

### 1. Clean Destroy
```python
removal_policy=RemovalPolicy.DESTROY
auto_delete_objects=True
```
**No orphaned resources!** Everything is automatically cleaned up.

### 2. Security Best Practices
- Encryption at rest (AES256)
- Least privilege IAM permissions
- No hardcoded credentials
- CloudWatch logging enabled

### 3. Cost Optimized
- All resources within AWS Free Tier
- $0/month for typical usage

## 🏗️ Infrastructure Components

```
AWS Resources:
├── S3 Bucket
│   ├── Encryption: AES256
│   ├── Auto-delete: Enabled
│   └── Removal policy: DESTROY
│
├── Lambda Function
│   ├── Runtime: Python 3.11
│   ├── Memory: 128 MB
│   ├── Timeout: 30 seconds
│   └── Function: Lists S3 objects
│
├── IAM Role: LambdaExecutionRole
│   ├── CloudWatch Logs access
│   └── S3 read/write access
│
└── IAM Role: S3AccessRole
    └── S3 read/write access
```

## 🛠️ Prerequisites

- AWS Account with configured credentials
- AWS CLI installed (`aws configure`)
- Node.js and npm
- Python 3.x
- AWS CDK (`npm install -g aws-cdk`)

## 📊 Getting Started

### Option 1: Quick Deploy (Recommended)
```bash
cd lambda-iam-lab
cat QUICK_START.md
# Follow the 3 steps
```

### Option 2: Detailed Setup
```bash
# Read complete setup instructions
cat Steps.MD

# Read project documentation
cd lambda-iam-lab
cat README.md
```

## 🧪 Testing Your Deployment

After deployment, test your Lambda function:

```bash
# Get the function name from deployment outputs
aws lambda invoke \
  --function-name <FUNCTION_NAME> \
  --payload '{}' \
  output.json

cat output.json
```

Upload a test file to S3:

```bash
echo "Hello World" > test.txt
aws s3 cp test.txt s3://<BUCKET_NAME>/

# Lambda should now see 1 object
aws lambda invoke \
  --function-name <FUNCTION_NAME> \
  --payload '{}' \
  output.json
```

## 🗑️ Clean Removal

```bash
cd lambda-iam-lab
cdk destroy
```

This will:
- ✅ Automatically delete all S3 objects
- ✅ Remove the S3 bucket
- ✅ Delete the Lambda function
- ✅ Remove all IAM roles and policies
- ✅ Delete the CloudFormation stack

## 📝 Useful Commands

```bash
cdk ls              # List all stacks
cdk synth           # Show CloudFormation template
cdk deploy          # Deploy to AWS
cdk diff            # Compare with deployed version
cdk destroy         # Remove all resources
cdk doctor          # Check CDK setup
```

## 🎓 What You'll Learn

1. ✅ AWS CDK with Python
2. ✅ Lambda function creation and configuration
3. ✅ IAM role management and permissions
4. ✅ S3 bucket configuration and security
5. ✅ Clean resource destruction patterns
6. ✅ Infrastructure as Code best practices
7. ✅ AWS security best practices

## 💰 Cost Estimate

All resources are within AWS Free Tier:
- **Lambda**: 1M requests/month free
- **S3**: 5GB storage free
- **CloudWatch Logs**: 5GB free
- **IAM Roles**: Always free

**Expected cost: $0/month** for typical usage

## 🔐 Security Features

- ✅ S3 bucket encryption (AES256)
- ✅ Least privilege IAM permissions
- ✅ No hardcoded credentials
- ✅ CloudWatch logging for audit
- ✅ Service principal authentication
- ✅ Bucket-specific access only

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
Ensure AWS credentials have permissions for:
- IAM (CreateRole, PutRolePolicy)
- S3 (CreateBucket)
- Lambda (CreateFunction)
- CloudFormation (Full access)

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

**Ready to deploy?** Start with [Steps.MD](./Steps.MD) or jump to [lambda-iam-lab/QUICK_START.md](./lambda-iam-lab/QUICK_START.md)

**Built with ❤️ using AWS CDK**
