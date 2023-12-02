import aws_cdk as core
import aws_cdk.assertions as assertions

from sf api endpoints.sf api endpoints_stack import SfApiEndpointsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sf api endpoints/sf api endpoints_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SfApiEndpointsStack(app, "sf-api-endpoints")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
