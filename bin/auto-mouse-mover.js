#!/usr/bin/env node

const { moveMouse } = require('../lib/moveMouse');

// 解析命令行参数
const args = process.argv.slice(2);
let interval = 60;
let duration = null;

// 简单的参数解析
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '-i' || arg === '--interval') {
    interval = parseInt(args[++i], 10);
    if (isNaN(interval) || interval < 1) {
      console.error('错误: 移动间隔必须大于0');
      process.exit(1);
    }
  } else if (arg === '-d' || arg === '--duration') {
    duration = parseInt(args[++i], 10);
    if (isNaN(duration) || duration < 1) {
      console.error('错误: 运行时长必须大于0');
      process.exit(1);
    }
  } else if (arg === '-h' || arg === '--help') {
    console.log(`
自动移动鼠标工具（防止系统进入休眠或锁定）

用法:
  auto-mouse-mover [选项]

选项:
  -i, --interval <秒>    鼠标移动间隔（秒），默认60秒
  -d, --duration <秒>    运行时长（秒），默认无限运行
  -h, --help             显示帮助信息

示例:
  auto-mouse-mover                    # 每60秒移动一次，无限运行
  auto-mouse-mover -i 30              # 每30秒移动一次
  auto-mouse-mover -i 120 -d 3600     # 每120秒移动一次，运行1小时

别名:
  可以使用 'amm' 作为 'auto-mouse-mover' 的简短别名
    `);
    process.exit(0);
  }
}

// 运行主函数
try {
  moveMouse(interval, duration);
} catch (error) {
  console.error('错误:', error.message);
  process.exit(1);
}

