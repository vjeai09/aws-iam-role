# YouTube Recording Script: AWS Lambda + IAM Role + S3 Bucket Setup

## 📺 Video Overview
Learn how to set up AWS Lambda with a unified IAM role and S3 bucket using AWS CDK in Python. Perfect for beginners and DevOps engineers!

---

## 🎬 PART 1: ARCHITECTURE OVERVIEW (0:00 - 2:00)

### Scene 1: Title Slide
**Voiceover:**
"Today, we're building a production-ready AWS infrastructure using Infrastructure as Code. We'll set up Lambda, S3, and IAM roles using AWS CDK."

**Show on screen:**
- Title: "AWS Lambda + S3 + Unified IAM Role with CDK"
- Your GitHub repo: github.com/vjeai09/aws-iam-role

### Scene 2: Architecture Diagram
**Voiceover:**
"Let's start with the architecture. We have three main components:"

**Show diagram and explain each:**
1. **S3 Bucket (vjeai-data-bucket)**
   - "The S3 bucket stores our data securely"
   - AES-256 encryption enabled
   - Auto-delete objects on stack destruction

2. **Unified IAM Role (vjeai-unified-role)**
   - "One role that handles everything"
   - Lambda execution permissions
   - S3 read/write access
   - CloudWatch Logs for monitoring

3. **Lambda Function (vjeai-s3-processor)**
   - "Our Lambda function processes S3 events"
   - Uses the unified IAM role
   - 128MB memory, 30-second timeout
   - Python 3.11 runtime

**Voiceover:** "All three components are connected through infrastructure as code, making them reproducible and version-controlled."

---

## 🎬 PART 2: CODE WALKTHROUGH (2:00 - 8:00)

### Scene 3: Project Structure
**Voiceover:**
"Let's explore the code structure. It's modular and clean."

**Show directory tree:**
```
lambda-iam-lab/
├── app.py                    # Entry point
├── lambda_iam_lab_stack.py   # Main orchestrator
├── constructs/
│   ├── iam_roles.py         # Unified IAM role
│   ├── s3_bucket.py         # S3 bucket configuration
│   ├── lambda_function.py   # Lambda function setup
│   └── outputs.py           # Stack outputs
└── lambda_code/
    └── handler.py           # Lambda handler code
```

**Voiceover:** "Each module has a single responsibility, making the code easy to understand and maintain."

### Scene 4: Unified IAM Role (iam_roles.py)
**Voiceover:**
"Here's the heart of our setup - the unified IAM role. Instead of managing two separate roles, we use one role for everything."

**Code to show and explain:**
```python
self.unified_role = iam.Role(
    self,
    "VjeaiUnifiedRole",
    role_name="vjeai-unified-role",
    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
    managed_policies=[
        iam.ManagedPolicy.from_aws_managed_policy_name(
            "service-role/AWSLambdaBasicExecutionRole"
        )
    ],
)
```

**Voiceover:**
- "This role can be assumed by the Lambda service"
- "It has basic Lambda execution permissions for CloudWatch Logs"
- "We grant it S3 read/write access in the next step"

### Scene 5: S3 Bucket (s3_bucket.py)
**Voiceover:**
"Now let's look at the S3 bucket configuration. Security and clean deletion are built in."

**Code to show:**
```python
self.bucket = s3.Bucket(
    self,
    "VjeaiDataBucket",
    bucket_name="vjeai-data-bucket",
    removal_policy=RemovalPolicy.DESTROY,
    auto_delete_objects=True,
    encryption=s3.BucketEncryption.S3_MANAGED,
)
```

**Voiceover:**
- "AES-256 encryption is enabled by default"
- "RemovalPolicy.DESTROY ensures clean deletion"
- "auto_delete_objects=True removes all objects when the stack is destroyed"
- "No orphaned resources left behind"

### Scene 6: Lambda Function (lambda_function.py)
**Voiceover:**
"Here's our Lambda function that uses the unified role and can access the S3 bucket."

**Code to show:**
```python
self.function = lambda_.Function(
    self,
    "VjeaiS3ProcessorFunction",
    function_name="vjeai-s3-processor",
    runtime=lambda_.Runtime.PYTHON_3_11,
    handler="index.lambda_handler",
    code=lambda_.Code.from_inline(LAMBDA_HANDLER_CODE),
    role=role,  # Our unified role!
    environment={"BUCKET_NAME": bucket_name},
    timeout=Duration.seconds(30),
    memory_size=128,
)
```

**Voiceover:**
- "128MB memory for processing"
- "30-second timeout for operations"
- "The unified role is passed here"
- "Bucket name is passed as an environment variable"

### Scene 7: Lambda Handler (handler.py)
**Voiceover:**
"The Lambda handler code is simple and focused on the core task."

**Code to show excerpt:**
```python
def lambda_handler(event, context):
    bucket_name = os.environ.get('BUCKET_NAME')
    # Process S3 events
    return {'statusCode': 200, 'body': 'Success'}
```

### Scene 8: Main Stack (lambda_iam_lab_stack.py)
**Voiceover:**
"Finally, the main stack orchestrates everything. Notice how clean and simple it is."

**Code to show:**
```python
s3_bucket = S3BucketConstruct(self, "VjeaiS3Bucket")
iam_roles = IAMRolesConstruct(self, "VjeaiIAMRoles")
iam_roles.grant_s3_access(s3_bucket.bucket)
lambda_function = LambdaFunctionConstruct(
    self, "VjeaiLambdaFunction",
    bucket_name=s3_bucket.bucket_name,
    role=iam_roles.unified_role,
)
```

**Voiceover:** "The flow is clear: S3 → IAM → Lambda. Each component knows only what it needs to know."

---

## 🎬 PART 3: DEPLOYMENT (8:00 - 12:00)

### Scene 9: Prerequisites
**Voiceover:**
"Before we deploy, make sure you have these installed:"

**Show checklist:**
- ✅ AWS CLI configured
- ✅ Node.js and npm
- ✅ AWS CDK
- ✅ Python 3.x

### Scene 10: Setup Steps
**Voiceover:**
"Here's how to set everything up:"

**Show terminal commands:**
```bash
# 1. Clone the repository
git clone https://github.com/vjeai09/aws-iam-role.git
cd aws-iam-role/lambda-iam-lab

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Scene 11: Bootstrap
**Voiceover:**
"CDK needs to bootstrap your AWS account. This is a one-time setup."

**Show command:**
```bash
cdk bootstrap
```

**Voiceover:** "This creates the necessary S3 bucket and IAM roles that CDK uses internally."

### Scene 12: Deploy
**Voiceover:**
"Now comes the exciting part - deploying our infrastructure!"

**Show command:**
```bash
cdk deploy
```

**Voiceover:**
- "CDK synthesizes the CloudFormation template"
- "Shows a preview of what will be created"
- "Deploys in about 80 seconds"
- "All resources are now live in AWS!"

### Scene 13: Verify Deployment
**Voiceover:**
"Let's verify everything is deployed correctly."

**Show AWS Console:**
1. IAM Roles - Show `vjeai-unified-role`
2. S3 Buckets - Show `vjeai-data-bucket`
3. Lambda Functions - Show `vjeai-s3-processor`

**Voiceover:** "Perfect! All three components are live and ready to work together."

---

## 🎬 PART 4: PERMISSIONS & SECURITY (12:00 - 15:00)

### Scene 14: IAM Permissions
**Voiceover:**
"Let's review the permissions of our unified role."

**Show in AWS Console - Role Details:**
- Trust Policy: Lambda service can assume this role
- Permissions: S3 read/write, CloudWatch Logs write

**Voiceover:**
- "The role follows the principle of least privilege"
- "Lambda can only access this specific S3 bucket"
- "CloudWatch Logs permissions for monitoring"

### Scene 15: S3 Security
**Voiceover:**
"The S3 bucket has built-in security features."

**Show S3 bucket properties:**
- Encryption: AES-256
- Block Public Access: Enabled
- Versioning: Disabled
- Auto-delete: Enabled

**Voiceover:** "Even if you forget to delete resources, the auto-delete feature ensures no orphaned objects remain."

---

## 🎬 PART 5: TESTING & CLEANUP (15:00 - 18:00)

### Scene 16: Test the Lambda
**Voiceover:**
"Let's test the Lambda function to make sure everything works."

**Show in AWS Console:**
1. Go to Lambda Console
2. Select `vjeai-s3-processor`
3. Create a test event
4. Run the test
5. Check CloudWatch Logs

**Voiceover:**
- "The function executed successfully"
- "We can see the logs in CloudWatch"
- "The unified role is doing its job"

### Scene 17: Upload to S3
**Voiceover:**
"Let's upload a file to S3 and see the Lambda process it."

**Show:**
```bash
aws s3 cp testfile.txt s3://vjeai-data-bucket/
```

**Voiceover:** "The Lambda would now process this event. In a production setup, you'd configure S3 event notifications."

### Scene 18: Cleanup
**Voiceover:**
"When you're done, cleanup is just one command!"

**Show:**
```bash
cdk destroy
```

**Voiceover:**
- "All resources are deleted cleanly"
- "No orphaned S3 objects"
- "No leftover IAM roles"
- "No charges accumulating"

---

## 🎬 PART 6: KEY TAKEAWAYS (18:00 - 20:00)

### Scene 19: Benefits Summary
**Voiceover:**
"Here's why this approach is powerful:"

**Show on screen:**
1. **Infrastructure as Code** - Version controlled, reproducible
2. **Unified Role** - Simpler management, less cognitive overhead
3. **Modular Design** - Easy to understand and modify
4. **Clean Destruction** - No orphaned resources
5. **Production Ready** - Security best practices built in

### Scene 20: Next Steps
**Voiceover:**
"Here are some next steps you can take:"

**Show suggestions:**
- Add S3 event notifications to trigger Lambda
- Add monitoring with CloudWatch alarms
- Implement DLQ (Dead Letter Queue)
- Scale to multiple Lambda functions
- Add CI/CD pipeline with GitHub Actions

### Scene 21: Call to Action
**Voiceover:**
"If you found this helpful, please like and subscribe. Check out the GitHub repository for the complete code. Happy coding!"

**Show on screen:**
- GitHub link: github.com/vjeai09/aws-iam-role
- Subscribe button animation
- Like button animation

---

## 📊 VISUAL AIDS TO CREATE

### Diagram 1: Architecture Overview
```
┌─────────────────────────────────────────────────────────┐
│                    AWS Account                          │
│                   (005173136176)                        │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │           AWS Lambda Function                    │  │
│  │      (vjeai-s3-processor)                       │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │  Unified IAM Role                          │ │  │
│  │  │ (vjeai-unified-role)                       │ │  │
│  │  │                                            │ │  │
│  │  │ ✓ Lambda Execution                         │ │  │
│  │  │ ✓ CloudWatch Logs Access                   │ │  │
│  │  │ ✓ S3 Read/Write Access                     │ │  │
│  │  └────────────────────────────────────────────┘ │  │
│  │                    │                            │  │
│  │                    ▼                            │  │
│  │         Processes S3 Events                    │  │
│  └──────────────────────────────────────────────────┘  │
│           │                        │                   │
│           ▼                        ▼                   │
│  ┌──────────────────┐      ┌─────────────────────┐   │
│  │   S3 Bucket      │      │  CloudWatch Logs    │   │
│  │(vjeai-data-      │      │  (Monitoring)       │   │
│  │  bucket)         │      │                     │   │
│  │                  │      │ ✓ Lambda Logs       │   │
│  │ ✓ Encryption     │      │ ✓ Error Tracking    │   │
│  │ ✓ Auto-delete    │      │ ✓ Performance       │   │
│  └──────────────────┘      └─────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Diagram 2: Permission Flow
```
┌─────────────────────────────────────────────────────┐
│          AWS Lambda Service                         │
│    Assumes vjeai-unified-role                       │
└──────────────┬──────────────────────────────────────┘
               │
               │ (Role provides permissions)
               ▼
        ┌──────────────────┐
        │  Unified Role    │
        │ vjeai-unified-   │
        │ role             │
        └────┬───────┬─────┘
             │       │
    ┌────────┘       └────────┐
    │                         │
    ▼                         ▼
S3 Bucket Access      CloudWatch Logs
✓ Get Objects         ✓ Create Log Groups
✓ Put Objects         ✓ Put Log Events
✓ Delete Objects      ✓ Describe Log Streams
```

### Diagram 3: CDK Stack Structure
```
LambdaIamLabStack
│
├─ VjeaiS3Bucket
│  └─ VjeaiDataBucket
│
├─ VjeaiIAMRoles
│  └─ VjeaiUnifiedRole
│
├─ VjeaiLambdaFunction
│  └─ VjeaiS3ProcessorFunction
│
└─ VjeaiOutputs
   ├─ BucketName: vjeai-data-bucket
   ├─ LambdaFunctionName: vjeai-s3-processor
   └─ UnifiedRoleArn: arn:aws:iam::...role/vjeai-unified-role
```

---

## 🎙️ RECORDING TIPS

1. **Pacing**: Speak clearly and slowly. Pause for emphasis.
2. **Screen Share**: Use a large font size (18+ on terminal)
3. **Zoom**: Show code at 150% zoom for readability
4. **Background Music**: Use royalty-free background music during slides
5. **Transitions**: Add fade transitions between scenes
6. **Captions**: Add captions for accessibility
7. **Graphics**: Animate the architecture diagrams

---

## ⏱️ TIMING BREAKDOWN

- Part 1 (Architecture): 0:00 - 2:00 (2 minutes)
- Part 2 (Code): 2:00 - 8:00 (6 minutes)
- Part 3 (Deployment): 8:00 - 12:00 (4 minutes)
- Part 4 (Security): 12:00 - 15:00 (3 minutes)
- Part 5 (Testing): 15:00 - 18:00 (3 minutes)
- Part 6 (Conclusion): 18:00 - 20:00 (2 minutes)

**Total: ~20 minutes**

---

## 📹 EQUIPMENT NEEDED

- Screen recording software (OBS, ScreenFlow)
- AWS Console access
- Terminal/IDE
- Microphone
- Editing software (DaVinci Resolve, Adobe Premiere)

---

## 🎬 START RECORDING!

You're all set. Use this script as a guide and make it your own. Good luck with your YouTube video! 🚀
