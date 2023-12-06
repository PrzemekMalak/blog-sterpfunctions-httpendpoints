#!/usr/bin/env python3
import os
from constructs import Construct
from aws_cdk import (
    CfnOutput,
    aws_lambda as lambda_,
aws_logs as logs_
)
import aws_cdk.aws_apigatewayv2_alpha as apigw_
import aws_cdk.aws_apigatewayv2_integrations_alpha as integrations_


DIRNAME = os.path.dirname(__file__)

class ApigwHttpApiLambdaConstruct(Construct):

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)
        self.fn = self._build_lambda()
        self.api = self._build_api()


    def _build_lambda(self) -> lambda_:
        lambda_fn = lambda_.Function(
            self, "ReceiverFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.Code.from_asset(os.path.join(DIRNAME, "src")),
            log_retention=logs_.RetentionDays.ONE_DAY
        )

        return lambda_fn

    def _build_api(self) -> apigw_.HttpApi:
        # Create the HTTP API with CORS
        http_api = apigw_.HttpApi(
            self, "ReceiverApi",
        )

        http_api.add_routes(
            path="/",
            methods=[apigw_.HttpMethod.ANY],
            integration=integrations_.HttpLambdaIntegration("LambdaProxyIntegration", handler=self.fn),
        )

        # Outputs
        CfnOutput(self, "API Endpoint", description="API Endpoint", value=http_api.api_endpoint)

        return  http_api

