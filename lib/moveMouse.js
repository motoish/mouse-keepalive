#!/usr/bin/env node
/**
 * Mouse Keepalive - JavaScript Wrapper
 * 
 * This is a wrapper script that delegates to the Python core module.
 * The core logic is implemented in Python (mouse_keepalive.move_mouse) for
 * better maintainability, testability, and cross-platform compatibility.
 * 
 * 这是一个包装脚本，将调用委托给 Python 核心模块。
 * 核心逻辑在 Python (mouse_keepalive.move_mouse) 中实现，以便于维护、测试和跨平台兼容。
 */

const { spawn } = require('child_process');
const path = require('path');
const os = require('os');

/**
 * Find Python executable
 * @returns {Promise<string>} Path to Python executable
 */
function findPython() {
  return new Promise((resolve, reject) => {
    const commands = ['python3', 'python'];
    let index = 0;

    function tryNext() {
      if (index >= commands.length) {
        reject(new Error('Python not found. Please install Python 3.6 or higher.'));
        return;
      }

      const cmd = commands[index++];
      const python = spawn(cmd, ['--version'], { stdio: 'pipe' });

      python.on('close', (code) => {
        if (code === 0) {
          resolve(cmd);
        } else {
          tryNext();
        }
      });

      python.on('error', () => {
        tryNext();
      });
    }

    tryNext();
  });
}

/**
 * Check if pyautogui is installed
 * @param {string} pythonCmd - Python command to use
 * @returns {Promise<boolean>} Whether pyautogui is installed
 */
function checkPyAutogui(pythonCmd) {
  return new Promise((resolve) => {
    const python = spawn(pythonCmd, ['-c', 'import pyautogui'], { stdio: 'pipe' });
    python.on('close', (code) => {
      resolve(code === 0);
    });
    python.on('error', () => {
      resolve(false);
    });
  });
}

/**
 * Install pyautogui if not present
 * @param {string} pythonCmd - Python command to use
 * @returns {Promise<void>}
 */
function installPyAutogui(pythonCmd) {
  return new Promise((resolve, reject) => {
    console.log('警告: pyautogui 未安装');
    console.log('Warning: pyautogui not installed');
    console.log('正在尝试安装...');
    console.log('Attempting to install...');

    const pip = spawn(pythonCmd, ['-m', 'pip', 'install', 'pyautogui'], {
      stdio: 'inherit',
    });

    pip.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error('Failed to install pyautogui. Please run: pip install pyautogui'));
      }
    });

    pip.on('error', (err) => {
      reject(err);
    });
  });
}

/**
 * Run Python module with arguments
 * @param {string} pythonCmd - Python command to use
 * @param {Array<string>} args - Arguments to pass
 */
function runPythonModule(pythonCmd, args) {
  const python = spawn(pythonCmd, ['-m', 'mouse_keepalive', ...args], {
    stdio: 'inherit',
  });

  python.on('close', (code) => {
    process.exit(code || 0);
  });

  python.on('error', (err) => {
    console.error('错误: 无法启动 Python 模块');
    console.error('Error: Failed to start Python module');
    console.error(err.message);
    process.exit(1);
  });

  // Forward signals to Python process
  process.on('SIGINT', () => {
    python.kill('SIGINT');
  });

  process.on('SIGTERM', () => {
    python.kill('SIGTERM');
  });
}

/**
 * Main entry point - delegates to Python core module
 * @param {number} interval - Movement interval in seconds
 * @param {number|null} duration - Duration in seconds, null for infinite
 */
async function moveMouse(interval = 60, duration = null) {
  try {
    // Find Python
    const pythonCmd = await findPython();

    // Check if pyautogui is installed
    const hasPyAutogui = await checkPyAutogui(pythonCmd);
    if (!hasPyAutogui) {
      try {
        await installPyAutogui(pythonCmd);
      } catch (err) {
        console.error(err.message);
        process.exit(1);
      }
    }

    // Build arguments
    const args = [];
    if (interval !== 60) {
      args.push('-i', interval.toString());
    }
    if (duration !== null) {
      args.push('-d', duration.toString());
    }

    // Run Python module
    runPythonModule(pythonCmd, args);
  } catch (err) {
    console.error('错误:', err.message);
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { moveMouse };

