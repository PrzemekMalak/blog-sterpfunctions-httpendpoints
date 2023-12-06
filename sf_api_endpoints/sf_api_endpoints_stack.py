from aws_cdk import (
    Stack,
)
from constructs import Construct
import json
from sf_api_endpoints.api_construct import ApigwHttpApiLambdaConstruct
from sf_api_endpoints.step_function_construct import StepFunctionConstruct
class SfApiEndpointsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        api = ApigwHttpApiLambdaConstruct(self, "ApigwHttpApiReceiver")
        sf = StepFunctionConstruct(self, 'ApiStepFunction')

