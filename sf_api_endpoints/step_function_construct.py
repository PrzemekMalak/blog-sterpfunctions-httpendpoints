from aws_cdk import aws_stepfunctions as sf
from aws_cdk import aws_iam, aws_events,CfnOutput, SecretValue
from constructs import Construct
from aws_cdk.aws_iam import Effect
from sf_api_endpoints.get_file import get_file
from typing import Final

DEFINITION_FILE: Final[str] = './sf_api_endpoints/asl.json'

class StepFunctionConstruct(Construct):
    # pylint: disable=too-many-instance-attributes, line-too-long

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)

        self.connection = self._build_api_connection()
        self.sf_role = self._build_step_function_role()
        self.step_function = self._build_step_function()

        # Outputs
        CfnOutput(self, "Connection Arn", description="Connection Arn", value=self.connection.connection_arn)

    def _build_api_connection(self) -> aws_events.Connection:
        connection = aws_events.Connection(self, "Connection",
            authorization=aws_events.Authorization.api_key("x-api-key", SecretValue.unsafe_plain_text('secret-value')),
            description="Connection with API Key x-api-key",
            )
        return connection

    def _build_step_function_role(self) -> aws_iam.Role:
        policy_document = aws_iam.PolicyDocument()

        states_policy_statement = aws_iam.PolicyStatement(actions=[
            'states:InvokeHTTPEndpoint',
        ], effect=Effect.ALLOW, resources=['*'])

        connection_policy_statement = aws_iam.PolicyStatement(actions=[
            'events:RetrieveConnectionCredentials',
        ], effect=Effect.ALLOW, resources=[self.connection.connection_arn])

        sm_policy_statement = aws_iam.PolicyStatement(actions=[
            'secretsmanager:DescribeSecret',
            'secretsmanager:GetSecretValue'
        ], effect=Effect.ALLOW, resources=[self.connection.connection_secret_arn])

        policy_document.add_statements(states_policy_statement)
        policy_document.add_statements(connection_policy_statement)
        policy_document.add_statements(sm_policy_statement)

        policy = aws_iam.Policy(self, 'APISFPolicy', document=policy_document)

        role = aws_iam.Role(self, 'StepFunctionServiceRole', description='API SF Service Role',
                            assumed_by=aws_iam.ServicePrincipal('states.amazonaws.com'))
        role.attach_inline_policy(policy=policy)
        aws_iam.PolicyDocument(
            statements=[aws_iam.PolicyStatement(effect=aws_iam.Effect.ALLOW, actions=['sts:AssumeRole'],
                                                resources=[role.role_arn])])

        return role
    def _build_step_function(self) -> sf.CfnStateMachine:
        return sf.CfnStateMachine(
            self,
            'ApiEndpoints-StepFunction',
            definition_string=get_file(DEFINITION_FILE),
            role_arn=self.sf_role.role_arn,
        )
