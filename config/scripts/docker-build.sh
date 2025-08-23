#!/bin/bash
# Docker 构建脚本 - 业务分析报告自动化系统
# 版本: v4.0 Production Ready

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
}

# 构建Docker镜像
build_image() {
    local env=${1:-production}
    
    log_info "开始构建 Docker 镜像 (环境: $env)..."
    
    # 设置镜像标签
    local image_tag="analysis-report-system:latest"
    if [ "$env" = "dev" ]; then
        image_tag="analysis-report-system:dev"
    fi
    
    # 构建镜像
    docker build \
        --tag "$image_tag" \
        --build-arg BUILD_ENV="$env" \
        .
    
    if [ $? -eq 0 ]; then
        log_success "Docker 镜像构建成功: $image_tag"
    else
        log_error "Docker 镜像构建失败"
        exit 1
    fi
}

# 启动服务
start_services() {
    local env=${1:-production}
    local compose_file="docker-compose.yml"
    
    if [ "$env" = "dev" ]; then
        compose_file="docker-compose.dev.yml"
    fi
    
    log_info "启动服务 (环境: $env)..."
    
    # 创建必要的目录
    mkdir -p output/reports output/charts pdf_reports data logs
    
    # 启动服务
    docker-compose -f "$compose_file" up -d
    
    if [ $? -eq 0 ]; then
        log_success "服务启动成功"
        
        # 等待服务就绪
        log_info "等待服务就绪..."
        sleep 10
        
        # 检查服务状态
        check_services "$compose_file"
    else
        log_error "服务启动失败"
        exit 1
    fi
}

# 检查服务状态
check_services() {
    local compose_file=${1:-docker-compose.yml}
    
    log_info "检查服务状态..."
    
    # 显示容器状态
    docker-compose -f "$compose_file" ps
    
    # 检查主应用健康状态
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s -f http://localhost:8000/api/info > /dev/null 2>&1; then
            log_success "应用服务健康检查通过"
            break
        else
            log_info "等待应用服务启动... ($((attempt + 1))/$max_attempts)"
            sleep 2
            ((attempt++))
        fi
    done
    
    if [ $attempt -eq $max_attempts ]; then
        log_error "应用服务健康检查失败"
        return 1
    fi
    
    # 显示访问信息
    echo
    log_success "🎉 系统部署成功！"
    echo
    echo "📊 访问地址："
    echo "   - 主应用: http://localhost:8000"
    echo "   - API文档: http://localhost:8000/docs"
    echo "   - 数据库管理: http://localhost:8080 (仅开发环境)"
    echo "   - Redis管理: http://localhost:8081 (仅开发环境)"
    echo
}

# 停止服务
stop_services() {
    local env=${1:-production}
    local compose_file="docker-compose.yml"
    
    if [ "$env" = "dev" ]; then
        compose_file="docker-compose.dev.yml"
    fi
    
    log_info "停止服务 (环境: $env)..."
    
    docker-compose -f "$compose_file" down
    
    if [ $? -eq 0 ]; then
        log_success "服务已停止"
    else
        log_error "停止服务失败"
        exit 1
    fi
}

# 清理资源
cleanup() {
    log_warning "清理 Docker 资源..."
    
    # 停止所有相关容器
    docker-compose -f docker-compose.yml down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    
    # 删除镜像
    docker rmi analysis-report-system:latest 2>/dev/null || true
    docker rmi analysis-report-system:dev 2>/dev/null || true
    
    # 清理未使用的资源
    docker system prune -f
    
    log_success "清理完成"
}

# 显示帮助信息
show_help() {
    echo "业务分析报告自动化系统 - Docker 管理脚本"
    echo
    echo "用法: $0 [命令] [环境]"
    echo
    echo "命令:"
    echo "  build     构建 Docker 镜像"
    echo "  start     启动服务"
    echo "  stop      停止服务"
    echo "  restart   重启服务"
    echo "  status    查看服务状态"
    echo "  logs      查看服务日志"
    echo "  cleanup   清理 Docker 资源"
    echo "  help      显示帮助信息"
    echo
    echo "环境:"
    echo "  production  生产环境 (默认)"
    echo "  dev         开发环境"
    echo
    echo "示例:"
    echo "  $0 build dev          # 构建开发环境镜像"
    echo "  $0 start production   # 启动生产环境服务"
    echo "  $0 logs app           # 查看应用日志"
}

# 查看日志
show_logs() {
    local service=${1:-app}
    local env=${2:-production}
    local compose_file="docker-compose.yml"
    
    if [ "$env" = "dev" ]; then
        compose_file="docker-compose.dev.yml"
    fi
    
    log_info "查看服务日志: $service"
    docker-compose -f "$compose_file" logs -f "$service"
}

# 主函数
main() {
    local command=${1:-help}
    local env=${2:-production}
    
    # 检查Docker环境
    if [ "$command" != "help" ]; then
        check_docker
    fi
    
    case "$command" in
        "build")
            build_image "$env"
            ;;
        "start")
            build_image "$env"
            start_services "$env"
            ;;
        "stop")
            stop_services "$env"
            ;;
        "restart")
            stop_services "$env"
            sleep 2
            build_image "$env"
            start_services "$env"
            ;;
        "status")
            local compose_file="docker-compose.yml"
            if [ "$env" = "dev" ]; then
                compose_file="docker-compose.dev.yml"
            fi
            docker-compose -f "$compose_file" ps
            ;;
        "logs")
            show_logs "$env" "production"
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# 执行主函数
main "$@"