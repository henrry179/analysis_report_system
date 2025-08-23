#!/usr/bin/env node
/**
 * Cursor CLI 交互式编辑示例
 * 演示如何使用Cursor CLI进行智能代码编辑
 */

const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// 示例1：智能代码补全
async function smartCompletion() {
    console.log('=== 智能代码补全 ===');
    
    const commands = [
        'cursor-cli complete --file incomplete.py --line 42',
        'cursor-cli imports --file app.js --auto-fix',
        'cursor-cli document --file api.py --style google'
    ];
    
    for (const cmd of commands) {
        console.log(`执行: ${cmd}`);
        try {
            const { stdout } = await execPromise(cmd);
            console.log(`结果: ${stdout}`);
        } catch (error) {
            console.error(`错误: ${error.message}`);
        }
    }
}

// 示例2：代码重构
async function codeRefactoring() {
    console.log('\n=== 代码重构 ===');
    
    const refactorTasks = [
        {
            desc: '重命名变量',
            cmd: 'cursor-cli refactor --file code.js --rename "oldName:newName"'
        },
        {
            desc: '提取函数',
            cmd: 'cursor-cli refactor --file long_function.py --extract-function --lines 10-30'
        },
        {
            desc: '应用设计模式',
            cmd: 'cursor-cli refactor --file service.java --pattern factory'
        }
    ];
    
    for (const task of refactorTasks) {
        console.log(`\n${task.desc}:`);
        console.log(`命令: ${task.cmd}`);
        // 实际执行时取消注释
        // await execPromise(task.cmd);
    }
}

// 示例3：AI对话编程
async function aiChatProgramming() {
    console.log('\n=== AI对话编程 ===');
    
    // 单次问答示例
    const question = "How to implement binary search in JavaScript?";
    const cmd = `cursor-cli ask "${question}"`;
    
    console.log(`提问: ${question}`);
    console.log(`命令: ${cmd}`);
    
    // 上下文感知对话
    const contextCmd = 'cursor-cli chat --context ./src --question "What does this function do?"';
    console.log(`\n上下文对话: ${contextCmd}`);
}

// 主函数
async function main() {
    console.log('Cursor CLI 交互式编辑示例');
    console.log('=' * 50);
    
    await smartCompletion();
    await codeRefactoring();
    await aiChatProgramming();
    
    console.log('\n示例演示完成！');
}

// 运行主函数
main().catch(console.error);