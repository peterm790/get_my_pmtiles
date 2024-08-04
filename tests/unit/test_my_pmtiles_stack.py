import aws_cdk as core
import aws_cdk.assertions as assertions

from my_pmtiles.my_pmtiles_stack import MyPmtilesStack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_pmtiles/my_pmtiles_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyPmtilesStack(app, "my-pmtiles")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
