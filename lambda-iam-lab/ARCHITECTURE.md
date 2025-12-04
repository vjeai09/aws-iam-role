# Architecture Overview

## Infrastructure Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS Account                              │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Lambda Function                        │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │  S3ProcessorFunction (Python 3.11)          │  │    │
│  │  │  - Handler: index.lambda_handler             │  │    │
│  │  │  - Memory: 128MB                             │  │    │
│  │  │  - Timeout: 30s                              │  │    │
│  │  │  - Env: BUCKET_NAME                          │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  │                    │                                 │    │
│  │                    │ Uses                            │    │
│  │                    ▼                                 │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │  IAM Role: LambdaExecutionRole              │  │    │
│  │  │  ─────────────────────────────────────────  │  │    │
│  │  │  Permissions:                               │  │    │
│  │  │  ✓ CloudWatch Logs (write)                  │  │    │
│  │  │  ✓ S3 Bucket (read/write)                   │  │    │
│  │  │                                              │  │    │
│  │  │  Trust Policy:                              │  │    │
│  │  │  - lambda.amazonaws.com                      │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────┘    │
│                           │                                 │
│                           │ Access                          │
│                           ▼                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │              S3 Bucket                              │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │  LambdaDataBucket                           │  │    │
│  │  │  - Encryption: AES256 (SSE-S3)              │  │    │
│  │  │  - Auto-delete: Enabled                     │  │    │
│  │  │  - Versioning: Disabled                     │  │    │
│  │  │  - RemovalPolicy: DESTROY                   │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────┘    │
│                           ▲                                 │
│                           │ Access                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │  IAM Role: S3AccessRole                            │    │
│  │  ─────────────────────────────────────────────────  │    │
│  │  Permissions:                                       │    │
│  │  ✓ S3 Bucket (read/write)                          │    │
│  │                                                     │    │
│  │  Trust Policy:                                      │    │
│  │  - Your AWS Account (AssumeRole)                   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         CloudWatch Logs                             │    │
│  │  /aws/lambda/S3ProcessorFunction                   │    │
│  │  - Retention: 731 days                             │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### S3 Bucket
- **Purpose**: Store data that Lambda can process
- **Encryption**: Server-side encryption with S3-managed keys (SSE-S3)
- **Cleanup**: Automatically deletes all objects when stack is destroyed
- **Access Control**: Only accessible via IAM roles

### Lambda Function
- **Language**: Python 3.11
- **Purpose**: Demonstrate S3 access with proper IAM permissions
- **Functionality**: Lists objects in the S3 bucket
- **Environment**: Receives bucket name as environment variable
- **Logging**: All execution logs sent to CloudWatch

### IAM Roles

#### 1. LambdaExecutionRole
```
Trust Relationship:
  lambda.amazonaws.com (Service Principal)

Managed Policies:
  - AWSLambdaBasicExecutionRole (CloudWatch Logs)

Inline Policies:
  - S3 Read/Write access to specific bucket:
    * s3:GetObject*
    * s3:PutObject*
    * s3:DeleteObject*
    * s3:List*
    * s3:GetBucket*
```

#### 2. S3AccessRole
```
Trust Relationship:
  Your AWS Account (can be assumed by IAM users/roles)

Inline Policies:
  - S3 Read/Write access to specific bucket:
    * s3:GetObject*
    * s3:PutObject*
    * s3:DeleteObject*
    * s3:List*
    * s3:GetBucket*
```

## Data Flow

1. **Lambda Invocation**
   ```
   User/Event → Lambda Function
   ```

2. **Lambda Execution**
   ```
   Lambda → Assumes LambdaExecutionRole
         → Reads BUCKET_NAME from environment
         → Calls s3_client.list_objects_v2()
         → Returns object count
   ```

3. **CloudWatch Logging**
   ```
   Lambda → CloudWatch Logs
         → Stores execution logs
         → Retention: 2 years
   ```

## Security Features

### Principle of Least Privilege
- Lambda role only has access to:
  - CloudWatch Logs (write)
  - Specific S3 bucket (read/write)
- No wildcard permissions
- No broad service access

### Encryption
- S3 data encrypted at rest (AES256)
- CloudWatch Logs encrypted by default
- No data in transit encryption needed (AWS internal)

### No Hardcoded Secrets
- Bucket name passed via environment variable
- IAM roles used for authentication
- No access keys or credentials in code

### Automatic Cleanup
- S3 bucket configured to auto-delete objects
- No orphaned resources after stack destroy
- Clean separation of concerns

## Resource Naming

All resources are named with CDK-generated logical IDs:
- Stack: `LambdaIamLabStack`
- Bucket: `LambdaDataBucket` (physical name auto-generated)
- Lambda: `S3ProcessorFunction` (physical name auto-generated)
- Role 1: `LambdaExecutionRole`
- Role 2: `S3AccessRole`

## CloudFormation Stack

This CDK app generates a CloudFormation stack with:
- 8+ resources
- 4 outputs (bucket name, function name, role ARNs)
- Custom resources for S3 auto-delete
- Proper dependencies and ordering

## Cost Analysis

| Resource | Free Tier | Typical Cost |
|----------|-----------|--------------|
| S3 Bucket | 5GB storage | ~$0.023/GB/month |
| Lambda | 1M requests | ~$0.20/1M requests |
| CloudWatch Logs | 5GB | ~$0.50/GB ingested |
| IAM Roles | Unlimited | Free |
| **Total** | Within Free Tier | <$1/month for light usage |

## Deployment Time

- Initial Bootstrap: 2-3 minutes (one-time)
- Stack Deploy: 1-2 minutes
- Stack Destroy: 1-2 minutes

## Scalability

- Lambda: Scales automatically (up to account limits)
- S3: Unlimited storage and requests
- CloudWatch: Automatic scaling
- No manual scaling required
