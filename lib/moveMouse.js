#!/usr/bin/env node

const robot = require('robotjs');
const os = require('os');

// 禁用 robotjs 的安全功能（防止鼠标移到屏幕角落时停止）
// Disable robotjs failsafe (prevents stopping when mouse moves to screen corner)
robot.setMouseDelay(0);

/**
 * 自动移动鼠标 / Automatically move mouse
 * @param {number} interval - 移动间隔（秒），默认60秒 / Movement interval (seconds), default 60
 * @param {number|null} duration - 运行时长（秒），null表示无限运行 / Duration (seconds), null means infinite
 */
function moveMouse(interval = 60, duration = null) {
  console.log('开始自动移动鼠标...');
  console.log('Starting auto mouse mover...');
  console.log(`移动间隔: ${interval} 秒 / Interval: ${interval} seconds`);
  if (duration) {
    console.log(`运行时长: ${duration} 秒 / Duration: ${duration} seconds`);
  } else {
    console.log('运行时长: 无限（按 Ctrl+C 停止） / Duration: Infinite (Press Ctrl+C to stop)');
  }
  console.log(`操作系统: ${os.platform()} / OS: ${os.platform()}`);
  console.log('-'.repeat(50));

  const startTime = Date.now();
  let moveCount = 0;

  const moveInterval = setInterval(() => {
    try {
      // 获取当前鼠标位置 / Get current mouse position
      const mousePos = robot.getMousePos();
      const currentX = mousePos.x;
      const currentY = mousePos.y;

      // 获取屏幕尺寸 / Get screen size
      const screenSize = robot.getScreenSize();
      const screenWidth = screenSize.width;
      const screenHeight = screenSize.height;

      // 移动鼠标到稍微不同的位置（移动1-2像素）
      // Move mouse to slightly different position (move 1-2 pixels)
      const offsetX = moveCount % 2 === 0 ? 1 : -1;
      const offsetY = moveCount % 2 === 0 ? 1 : -1;

      let newX = currentX + offsetX;
      let newY = currentY + offsetY;

      // 确保坐标在屏幕范围内 / Ensure coordinates are within screen bounds
      newX = Math.max(1, Math.min(newX, screenWidth - 1));
      newY = Math.max(1, Math.min(newY, screenHeight - 1));

      // 移动鼠标 / Move mouse
      robot.moveMouse(newX, newY);

      moveCount++;

      // 立即移回原位置（这样用户感觉不到鼠标移动）
      // Immediately move back to original position (user won't notice the movement)
      robot.moveMouse(currentX, currentY);

      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      console.log(
        `[${elapsed}s] 已移动鼠标 ${moveCount} 次 (当前位置: ${currentX}, ${currentY})`
      );
      console.log(
        `[${elapsed}s] Moved mouse ${moveCount} times (current position: ${currentX}, ${currentY})`
      );

      // 检查是否达到运行时长 / Check if duration is reached
      if (duration && elapsed >= duration) {
        console.log(`\n达到运行时长 ${duration} 秒，程序退出`);
        console.log(`Duration ${duration} seconds reached, exiting`);
        clearInterval(moveInterval);
        process.exit(0);
      }
    } catch (error) {
      console.error('错误:', error.message);
      console.error('Error:', error.message);
      clearInterval(moveInterval);
      process.exit(1);
    }
  }, interval * 1000);

  // 处理 Ctrl+C / Handle Ctrl+C
  process.on('SIGINT', () => {
    console.log('\n\n程序被用户中断');
    console.log('Program interrupted by user');
    console.log(`总共移动鼠标 ${moveCount} 次 / Total moves: ${moveCount}`);
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    console.log(`运行时长: ${elapsed} 秒 / Duration: ${elapsed} seconds`);
    clearInterval(moveInterval);
    process.exit(0);
  });
}

module.exports = { moveMouse };

