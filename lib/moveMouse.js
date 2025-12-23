#!/usr/bin/env node

const robot = require('robotjs');
const os = require('os');

// 禁用 robotjs 的安全功能（防止鼠标移到屏幕角落时停止）
robot.setMouseDelay(0);

/**
 * 自动移动鼠标
 * @param {number} interval - 移动间隔（秒），默认60秒
 * @param {number|null} duration - 运行时长（秒），null表示无限运行
 */
function moveMouse(interval = 60, duration = null) {
  console.log('开始自动移动鼠标...');
  console.log(`移动间隔: ${interval} 秒`);
  if (duration) {
    console.log(`运行时长: ${duration} 秒`);
  } else {
    console.log('运行时长: 无限（按 Ctrl+C 停止）');
  }
  console.log(`操作系统: ${os.platform()}`);
  console.log('-'.repeat(50));

  const startTime = Date.now();
  let moveCount = 0;

  const moveInterval = setInterval(() => {
    try {
      // 获取当前鼠标位置
      const mousePos = robot.getMousePos();
      const currentX = mousePos.x;
      const currentY = mousePos.y;

      // 获取屏幕尺寸
      const screenSize = robot.getScreenSize();
      const screenWidth = screenSize.width;
      const screenHeight = screenSize.height;

      // 移动鼠标到稍微不同的位置（移动1-2像素）
      const offsetX = moveCount % 2 === 0 ? 1 : -1;
      const offsetY = moveCount % 2 === 0 ? 1 : -1;

      let newX = currentX + offsetX;
      let newY = currentY + offsetY;

      // 确保坐标在屏幕范围内
      newX = Math.max(1, Math.min(newX, screenWidth - 1));
      newY = Math.max(1, Math.min(newY, screenHeight - 1));

      // 移动鼠标
      robot.moveMouse(newX, newY);

      moveCount++;

      // 立即移回原位置（这样用户感觉不到鼠标移动）
      robot.moveMouse(currentX, currentY);

      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      console.log(
        `[${elapsed}s] 已移动鼠标 ${moveCount} 次 (当前位置: ${currentX}, ${currentY})`
      );

      // 检查是否达到运行时长
      if (duration && elapsed >= duration) {
        console.log(`\n达到运行时长 ${duration} 秒，程序退出`);
        clearInterval(moveInterval);
        process.exit(0);
      }
    } catch (error) {
      console.error('错误:', error.message);
      clearInterval(moveInterval);
      process.exit(1);
    }
  }, interval * 1000);

  // 处理 Ctrl+C
  process.on('SIGINT', () => {
    console.log('\n\n程序被用户中断');
    console.log(`总共移动鼠标 ${moveCount} 次`);
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    console.log(`运行时长: ${elapsed} 秒`);
    clearInterval(moveInterval);
    process.exit(0);
  });
}

module.exports = { moveMouse };

