# Terminal Commands for YouTube Video Recording

## 🎬 Terminal Recording Commands Reference

Use these commands in sequence while recording your video. Clear your terminal before starting!

---

## 📝 SECTION 1: SETUP & PREREQUISITES (0:00 - 1:00)

### Show Python & Node versions
```bash
python3 --version
```
**Expected Output:**
```
Python 3.11.x
```

### Show Node.js version
```bash
node --version
```
**Expected Output:**
```
v23.0.0
```

### Show AWS CLI version
```bash
aws --version
```
**Expected Output:**
```
aws-cli/2.x.x
```

### Verify AWS Account (Show you're logged in)
```bash
aws sts get-caller-identity
```
**Expected Output:**
```json
{
    "UserId": "005173136176",
    "Account": "005173136176",
    "Arn": "arn:aws:iam::005173136176:root"
}
```

---

## 📂 SECTION 2: PROJECT STRUCTURE (1:00 - 2:30)

### Navigate to project
```bash
cd /Users/tusshar/aws-iam-role/lambda-iam-lab
```

### Show directory tree structure
```bash
tree -L 2 -I '__pycache__|*.pyc|.venv'
```
**Expected Output:**
```
.
├── app.py
├── requirements.txt
├── lambda_iam_lab/
│   ├── __init__.py
│   ├── lambda_iam_lab_stack.py
│   ├── README.md
│   ├── constructs/
│   │   ├── __init__.py
│   │   ├── iam_roles.py
│   │   ├── lambda_function.py
│   │   ├── outputs.py
│   │   └── s3_bucket.py
│   └── lambda_code/
│       ├── __init__.py
│       └── handler.py
```

### Show requirements.txt
```bash
cat requirements.txt
```
**Expected Output:**
```
aws-cdk-lib==2.215.0
constructs>=10.0.0,<11.0.0
```

### List Python files and line counts
```bash
find lambda_iam_lab -name "*.py" -type f -exec wc -l {} + | sort -n
```

---

## 🔧 SECTION 3: VIRTUAL ENVIRONMENT SETUP (2:30 - 4:00)

### Activate virtual environment
```bash
source .venv/bin/activate
```
**Expected:** Prompt shows `(.venv)` at the beginning

### Show virtual environment location
```bash
which python
```
**Expected Output:**
```
/Users/tusshar/aws-iam-role/lambda-iam-lab/.venv/bin/python
```

### Verify CDK is installed
```bash
cdk --version
```
**Expected Output:**
```
2.1033.0 (build 1ec3310)
```

### List installed packages
```bash
pip list | grep -E "aws-cdk|constructs"
```
**Expected Output:**
```
aws-cdk-lib                  2.215.0
constructs                   10.4.3
```

---

## 📖 SECTION 4: CODE WALKTHROUGH (4:00 - 10:00)

### Show main stack file
```bash
cat lambda_iam_lab/lambda_iam_lab_stack.py
```

### Show IAM roles construct
```bash
cat lambda_iam_lab/constructs/iam_roles.py
```

### Show S3 bucket construct
```bash
cat lambda_iam_lab/constructs/s3_bucket.py
```

### Show Lambda function construct
```bash
cat lambda_iam_lab/constructs/lambda_function.py
```

### Show Lambda handler code
```bash
cat lambda_iam_lab/constructs/outputs.py
```

### Show Lambda handler
```bash
cat lambda_iam_lab/lambda_code/handler.py
```

### Show app.py entry point
```bash
cat app.py
```

---

## 🏗️ SECTION 5: CDK SYNTHESIS (10:00 - 11:00)

### Synthesize the stack (generates CloudFormation)
```bash
cdk synth
```
**Expected:** Shows CloudFormation template in JSON format

### Synthesize without output noise
```bash
cdk synth --quiet
```
**Expected:** No output if successful

### Check for errors
```bash
cdk synth 2>&1 | grep -i "error"
```
**Expected:** No errors

---

## 🚀 SECTION 6: BOOTSTRAP & DEPLOY (11:00 - 16:00)

### Bootstrap CDK (one-time setup)
```bash
cdk bootstrap
```
**Expected Output:**
```
✅ Environment aws://005173136176/us-east-1 bootstrapped.
```

### Deploy the stack
```bash
cdk deploy
```
**When prompted, type:** `y` and press Enter

**Expected Output:**
```
✅ LambdaIamLabStack
✨ Deployment time: 75-85 seconds

Outputs:
LambdaIamLabStack.VjeaiOutputsBucketNameAF7D8C86 = vjeai-data-bucket
LambdaIamLabStack.VjeaiOutputsLambdaFunctionName7C20415B = vjeai-s3-processor
LambdaIamLabStack.VjeaiOutputsUnifiedRoleArn7CAACF64 = arn:aws:iam::005173136176:role/vjeai-unified-role
```

---

## ✅ SECTION 7: VERIFICATION (16:00 - 17:30)

### Verify S3 bucket created
```bash
aws s3 ls | grep vjeai
```
**Expected Output:**
```
2025-12-04 13:02:51 vjeai-data-bucket
```

### List S3 bucket details
```bash
aws s3api list-buckets --query "Buckets[?contains(Name, 'vjeai')].Name"
```
**Expected Output:**
```
[
    "vjeai-data-bucket"
]
```

### Verify IAM role created
```bash
aws iam list-roles --query "Roles[?contains(RoleName, 'vjeai')].RoleName" --output table
```
**Expected Output:**
```
-----------------------
|     ListRoles       |
+-----------+---------+
|  vjeai-unified-role |
+-----------+---------+
```

### Get IAM role details
```bash
aws iam get-role --role-name vjeai-unified-role --query "Role.[RoleName, Arn, CreateDate]"
```
**Expected Output:**
```
[
    "vjeai-unified-role",
    "arn:aws:iam::005173136176:role/vjeai-unified-role",
    "2025-12-04T13:02:18+00:00"
]
```

### Verify Lambda function created
```bash
aws lambda list-functions --query "Functions[?contains(FunctionName, 'vjeai')].FunctionName" --output table
```
**Expected Output:**
```
----------------------------------
|      ListFunctions              |
+----------+---------------------+
|  vjeai-s3-processor             |
+----------+---------------------+
```

### Get Lambda function details
```bash
aws lambda get-function --function-name vjeai-s3-processor --query "Configuration.[FunctionName, Runtime, Role, Timeout, MemorySize]"
```
**Expected Output:**
```
[
    "vjeai-s3-processor",
    "python3.11",
    "arn:aws:iam::005173136176:role/vjeai-unified-role",
    30,
    128
]
```

---

## 📤 SECTION 8: TEST UPLOAD TO S3 (17:30 - 18:30)

### Create a test file
```bash
echo "This is a test file for vjeai Lambda" > testfile.txt
```

### Upload to S3
```bash
aws s3 cp testfile.txt s3://vjeai-data-bucket/
```
**Expected Output:**
```
upload: ./testfile.txt to s3://vjeai-data-bucket/testfile.txt
```

### List files in S3 bucket
```bash
aws s3 ls s3://vjeai-data-bucket/
```
**Expected Output:**
```
2025-12-04 13:05:10         36 testfile.txt
```

### Download the file back
```bash
aws s3 cp s3://vjeai-data-bucket/testfile.txt testfile-downloaded.txt
```
**Expected Output:**
```
download: s3://vjeai-data-bucket/testfile.txt to ./testfile-downloaded.txt
```

### Verify file was downloaded
```bash
cat testfile-downloaded.txt
```
**Expected Output:**
```
This is a test file for vjeai Lambda
```

---

## 📊 SECTION 9: CLOUDWATCH LOGS (18:30 - 19:00)

### List log groups
```bash
aws logs describe-log-groups --query "logGroups[?contains(logGroupName, 'vjeai')].logGroupName"
```
**Expected Output:**
```
[
    "/aws/lambda/vjeai-s3-processor"
]
```

### Get log streams
```bash
aws logs describe-log-streams --log-group-name /aws/lambda/vjeai-s3-processor --query "logStreams[0].[logStreamName, creationTime]"
```

### View log events (if Lambda was triggered)
```bash
aws logs tail /aws/lambda/vjeai-s3-processor --follow
```

---

## 🧹 SECTION 10: CLEANUP (19:00 - 20:00)

### Show CloudFormation stacks
```bash
aws cloudformation list-stacks --query "StackSummaries[?contains(StackName, 'LambdaIamLab')].StackName"
```
**Expected Output:**
```
[
    "LambdaIamLabStack"
]
```

### Destroy the stack
```bash
cdk destroy
```
**When prompted, type:** `y` and press Enter

**Expected Output:**
```
✅  LambdaIamLabStack: destroyed
```

### Verify everything is deleted
```bash
aws s3 ls | grep vjeai
```
**Expected:** No output (bucket deleted)

### Verify IAM role deleted
```bash
aws iam list-roles --query "Roles[?contains(RoleName, 'vjeai')].RoleName"
```
**Expected Output:**
```
[]
```

### Verify Lambda function deleted
```bash
aws lambda list-functions --query "Functions[?contains(FunctionName, 'vjeai')].FunctionName"
```
**Expected Output:**
```
[]
```

---

## 💡 BONUS COMMANDS (For Q&A or Exploration)

### Show Git history
```bash
git log --oneline -n 5
```

### Show Git remote
```bash
git remote -v
```

### Check Git status
```bash
git status
```

### Show your GitHub repo
```bash
echo "https://github.com/vjeai09/aws-iam-role"
```

### Count total lines of code
```bash
find lambda_iam_lab -name "*.py" -type f -exec cat {} + | wc -l
```

### Show AWS region
```bash
echo $AWS_DEFAULT_REGION
```

### List all CDK commands
```bash
cdk --help
```

### Validate CloudFormation template
```bash
cdk synth | aws cloudformation validate-template --template-body file:///dev/stdin
```

---

## 🎬 RECORDING TIPS

1. **Clear Terminal Before Starting**
   ```bash
   clear
   ```

2. **Increase Font Size** (Make it readable!)
   - Terminal → Preferences → Text Size: 16-18pt

3. **Run Commands Slowly** - Pause after each command so viewers can read

4. **Explain While Running** - Give context for what each command does

5. **Copy/Paste Long Commands** - Don't type them; copy-paste to avoid typos

6. **Use `--quiet` flags** - For verbose commands to keep output clean

7. **Pipe to `grep`** - Filter output to show only relevant info

8. **Take Screenshots** - Save key outputs for later editing

---

## ⏱️ TIMING BREAKDOWN

- **Section 1**: 1 minute (Setup)
- **Section 2**: 1.5 minutes (Project structure)
- **Section 3**: 1.5 minutes (Virtual environment)
- **Section 4**: 6 minutes (Code walkthrough)
- **Section 5**: 1 minute (Synthesis)
- **Section 6**: 5 minutes (Deploy)
- **Section 7**: 1.5 minutes (Verification)
- **Section 8**: 1 minute (S3 test)
- **Section 9**: 0.5 minutes (CloudWatch)
- **Section 10**: 1 minute (Cleanup)

**Total**: ~20 minutes

---

## 🚀 Quick Copy-Paste Command Sets

### Fast Setup (Complete flow)
```bash
cd /Users/tusshar/aws-iam-role/lambda-iam-lab
source .venv/bin/activate
cdk synth --quiet
cdk bootstrap
cdk deploy
```

### Quick Verification
```bash
aws s3 ls | grep vjeai
aws iam list-roles --query "Roles[?contains(RoleName, 'vjeai')].RoleName"
aws lambda list-functions --query "Functions[?contains(FunctionName, 'vjeai')].FunctionName"
```

### Quick Cleanup
```bash
cdk destroy
aws s3 ls | grep vjeai  # Verify it's gone
aws iam list-roles --query "Roles[?contains(RoleName, 'vjeai')].RoleName"  # Verify deleted
```

---

## ✨ GOOD LUCK WITH YOUR RECORDING! 🎥

Remember to:
- ✓ Speak clearly and slowly
- ✓ Pause between commands
- ✓ Show outputs on screen
- ✓ Explain what each command does
- ✓ Have fun and be enthusiastic!

You've got this! 🚀
