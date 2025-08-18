#!/bin/bash
# 蓝绿部署脚本
# 用于生产环境的零停机部署

set -e

VERSION=$1
NAMESPACE="production"
APP_NAME="analysis-system"

if [ -z "$VERSION" ]; then
    echo "❌ 错误: 请提供版本号"
    echo "用法: $0 <version>"
    exit 1
fi

echo "🚀 开始蓝绿部署..."
echo "📦 版本: $VERSION"
echo "🌍 命名空间: $NAMESPACE"

# 检查当前活跃环境
CURRENT_ENV=$(kubectl get service $APP_NAME -n $NAMESPACE -o jsonpath='{.spec.selector.environment}' 2>/dev/null || echo "blue")
if [ "$CURRENT_ENV" = "blue" ]; then
    NEW_ENV="green"
else
    NEW_ENV="blue"
fi

echo "🔵 当前环境: $CURRENT_ENV"
echo "🟢 新环境: $NEW_ENV"

# 更新新环境的部署
echo "📝 更新 $NEW_ENV 环境配置..."
sed -i "s|IMAGE_TAG|$VERSION|g" k8s/production/deployment-$NEW_ENV.yaml
sed -i "s|ENVIRONMENT|$NEW_ENV|g" k8s/production/deployment-$NEW_ENV.yaml

# 部署到新环境
echo "🚀 部署到 $NEW_ENV 环境..."
kubectl apply -f k8s/production/deployment-$NEW_ENV.yaml

# 等待新环境就绪
echo "⏳ 等待 $NEW_ENV 环境就绪..."
kubectl rollout status deployment/$APP_NAME-$NEW_ENV -n $NAMESPACE --timeout=600s

# 健康检查
echo "🏥 健康检查 $NEW_ENV 环境..."
NEW_POD=$(kubectl get pods -n $NAMESPACE -l app=$APP_NAME,environment=$NEW_ENV -o jsonpath='{.items[0].metadata.name}')
kubectl exec $NEW_POD -n $NAMESPACE -- curl -f http://localhost:8000/health

# 运行烟雾测试
echo "🧪 运行烟雾测试..."
kubectl port-forward service/$APP_NAME-$NEW_ENV 18000:8000 -n $NAMESPACE &
PF_PID=$!
sleep 10

# 测试关键API端点
curl -f http://localhost:18000/api/info || { echo "❌ API测试失败"; kill $PF_PID; exit 1; }
curl -f http://localhost:18000/health || { echo "❌ 健康检查失败"; kill $PF_PID; exit 1; }

kill $PF_PID

# 切换流量到新环境
echo "🔄 切换流量到 $NEW_ENV 环境..."
kubectl patch service $APP_NAME -n $NAMESPACE -p '{"spec":{"selector":{"environment":"'$NEW_ENV'"}}}'

# 等待流量切换完成
echo "⏳ 等待流量切换完成..."
sleep 30

# 验证新环境正常工作
echo "✅ 验证新环境..."
for i in {1..5}; do
    kubectl exec $NEW_POD -n $NAMESPACE -- curl -f http://localhost:8000/api/info || { 
        echo "❌ 验证失败，回滚到 $CURRENT_ENV"; 
        kubectl patch service $APP_NAME -n $NAMESPACE -p '{"spec":{"selector":{"environment":"'$CURRENT_ENV'"}}}';
        exit 1; 
    }
    sleep 2
done

# 缩放旧环境
echo "📉 缩放旧环境 $CURRENT_ENV..."
kubectl scale deployment $APP_NAME-$CURRENT_ENV --replicas=1 -n $NAMESPACE

echo "🎉 蓝绿部署完成!"
echo "✅ 新版本 $VERSION 已成功部署到 $NEW_ENV 环境"
echo "🔵 旧环境 $CURRENT_ENV 已保留1个副本用于快速回滚"

# 记录部署信息
echo "📝 记录部署信息..."
kubectl annotate deployment $APP_NAME-$NEW_ENV -n $NAMESPACE \
    deployment.kubernetes.io/revision-history="$(date): Deployed version $VERSION via blue-green deployment"

echo "🏁 部署完成!"