#!/usr/bin/env node

const { moveMouse } = require('../lib/moveMouse');

// 解析命令行参数 / Parse command line arguments
const args = process.argv.slice(2);
let interval = 60;
let duration = null;

// 简单的参数解析 / Simple argument parsing
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '-i' || arg === '--interval') {
    interval = parseInt(args[++i], 10);
    if (isNaN(interval) || interval < 1) {
      console.error('错误: 移动间隔必须大于0');
      console.error('Error: Interval must be greater than 0');
      process.exit(1);
    }
  } else if (arg === '-d' || arg === '--duration') {
    duration = parseInt(args[++i], 10);
    if (isNaN(duration) || duration < 1) {
      console.error('错误: 运行时长必须大于0');
      console.error('Error: Duration must be greater than 0');
      process.exit(1);
    }
  } else if (arg === '-h' || arg === '--help') {
    console.log(`
自动移动鼠标工具（防止系统进入休眠或锁定）
Mouse Keepalive Tool (prevents system sleep or lock)

用法 / Usage:
  mouse-keepalive [选项 / options]
  mka [选项 / options]

选项 / Options:
  -i, --interval <秒>    鼠标移动间隔（秒），默认60秒 / Movement interval (seconds), default 60
  -d, --duration <秒>    运行时长（秒），默认无限运行 / Duration (seconds), default infinite
  -h, --help             显示帮助信息 / Show help information

示例 / Examples:
  mouse-keepalive                    # 每60秒移动一次，无限运行 / Move every 60s, infinite
  mouse-keepalive -i 30              # 每30秒移动一次 / Move every 30s
  mouse-keepalive -i 120 -d 3600     # 每120秒移动一次，运行1小时 / Move every 120s, run 1 hour
  mka -i 30                          # 使用简短别名 / Use short alias

别名 / Alias:
  可以使用 'mka' 作为 'mouse-keepalive' 的简短别名
  You can use 'mka' as a short alias for 'mouse-keepalive'
    `);
    process.exit(0);
  }
}

// 运行主函数 / Run main function
try {
  moveMouse(interval, duration);
} catch (error) {
  console.error('错误:', error.message);
  console.error('Error:', error.message);
  process.exit(1);
}

