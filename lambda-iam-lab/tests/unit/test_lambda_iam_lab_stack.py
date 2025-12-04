import aws_cdk as core
import aws_cdk.assertions as assertions

from lambda_iam_lab.lambda_iam_lab_stack import LambdaIamLabStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_iam_lab/lambda_iam_lab_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LambdaIamLabStack(app, "lambda-iam-lab")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
