#!/usr/bin/env python3
"""
Amazon Q Code AWS Lambda 示例
演示如何使用Amazon Q生成和优化Lambda函数
"""

import os
import json
import subprocess

class AmazonQDemo:
    """Amazon Q Code 演示类"""
    
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-east-1')
    
    def create_lambda_function(self):
        """创建Lambda函数"""
        print("=== 创建Lambda函数 ===\n")
        
        # Lambda函数生成命令
        commands = [
            {
                "desc": "创建S3事件处理函数",
                "cmd": """amazon-q create --template lambda-function \\
  --runtime python3.9 \\
  --handler index.handler \\
  --description "Process S3 events" """
            },
            {
                "desc": "创建API Gateway集成",
                "cmd": """amazon-q create --template api-gateway \\
  --method POST \\
  --integration lambda"""
            },
            {
                "desc": "创建DynamoDB CRUD操作",
                "cmd": """amazon-q generate --service dynamodb \\
  --operation "CRUD operations for user table" """
            }
        ]
        
        for item in commands:
            print(f"{item['desc']}:")
            print(f"{item['cmd']}\n")
    
    def generate_serverless_app(self):
        """生成Serverless应用"""
        print("=== 生成Serverless应用 ===\n")
        
        app_config = """amazon-q create-app --name "order-processing" \\
  --type serverless \\
  --components "
    - API Gateway for REST endpoints
    - Lambda functions for business logic
    - DynamoDB for data storage
    - SQS for message queuing
    - SNS for notifications
  " \\
  --output order-app/"""
        
        print("完整的订单处理系统:")
        print(app_config)
    
    def security_compliance(self):
        """安全与合规检查"""
        print("\n=== 安全与合规 ===\n")
        
        security_commands = [
            "安全扫描: amazon-q security --scan . --compliance 'pci-dss,hipaa'",
            "IAM策略生成: amazon-q iam --generate-policy --service s3 --actions 'read,write'",
            "密钥轮换: amazon-q secrets --rotate --secret-name 'db-password' --schedule '30 days'",
            "漏洞扫描: amazon-q vulnerability --scan . --severity critical,high"
        ]
        
        for cmd in security_commands:
            print(f"• {cmd}")
    
    def cost_optimization(self):
        """成本优化"""
        print("\n=== 成本优化 ===\n")
        
        cost_commands = {
            "成本分析": "amazon-q cost --analyze . --suggest-optimizations",
            "资源优化": "amazon-q optimize --resources --target cost-reduction",
            "Spot实例建议": "amazon-q ec2 --suggest-spot --workload batch-processing",
            "预算告警": "amazon-q budget --create --limit 1000 --alert 80%"
        }
        
        for desc, cmd in cost_commands.items():
            print(f"{desc}:")
            print(f"  {cmd}\n")
    
    def cicd_integration(self):
        """CI/CD集成"""
        print("=== CI/CD集成 ===\n")
        
        pipeline_config = """# 创建CodePipeline
amazon-q pipeline --create \\
  --source github \\
  --build codebuild \\
  --deploy ecs

# 生成BuildSpec文件
amazon-q codebuild --generate-spec \\
  --runtime nodejs14 \\
  --test jest

# 生成GitHub Actions工作流
amazon-q github-actions --create \\
  --deploy-to aws \\
  --environment production"""
        
        print(pipeline_config)
    
    def generate_cdk_code(self):
        """生成CDK代码"""
        print("\n=== CDK代码生成 ===\n")
        
        cdk_example = """import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class MyServerlessStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    // DynamoDB表
    const table = new dynamodb.Table(this, 'OrderTable', {
      partitionKey: { name: 'orderId', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST
    });
    
    // Lambda函数
    const orderHandler = new lambda.Function(this, 'OrderHandler', {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'order.handler',
      environment: {
        TABLE_NAME: table.tableName
      }
    });
    
    // 授予Lambda读写权限
    table.grantReadWriteData(orderHandler);
    
    // API Gateway
    const api = new apigateway.RestApi(this, 'OrderAPI', {
      restApiName: 'Order Service',
      description: 'This service handles orders.'
    });
    
    const orders = api.root.addResource('orders');
    orders.addMethod('POST', new apigateway.LambdaIntegration(orderHandler));
  }
}"""
        
        print("生成的CDK Stack代码:")
        print(cdk_example)

def main():
    """主函数"""
    print("=" * 70)
    print("Amazon Q Code - AWS服务集成示例")
    print("=" * 70 + "\n")
    
    demo = AmazonQDemo()
    
    # 运行各个示例
    demo.create_lambda_function()
    demo.generate_serverless_app()
    demo.security_compliance()
    demo.cost_optimization()
    demo.cicd_integration()
    demo.generate_cdk_code()
    
    print("\n" + "=" * 70)
    print("示例演示完成！")
    print("更多信息请查看文档: docs/amazon-q-code.md")
    print("=" * 70)

if __name__ == "__main__":
    main()