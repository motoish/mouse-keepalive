#!/usr/bin/env node
/**
 * npm CLI: delegates to Python module mouse_keepalive.
 * npm CLI：委托给 Python 模块 mouse_keepalive。
 */

const { spawn } = require('child_process');

function tryPython(cmd) {
  return new Promise((resolve) => {
    const proc = spawn(cmd, ['--version'], { stdio: 'pipe' });
    proc.on('close', (code) => resolve(code === 0 ? cmd : null));
    proc.on('error', () => resolve(null));
  });
}

async function findPython() {
  for (const cmd of ['python3', 'python']) {
    const found = await tryPython(cmd);
    if (found) return found;
  }
  throw new Error('Python not found. Please install Python 3.11 or higher.');
}

function checkPyAutogui(pythonCmd) {
  return new Promise((resolve) => {
    const proc = spawn(pythonCmd, ['-c', 'import pyautogui'], { stdio: 'pipe' });
    proc.on('close', (code) => resolve(code === 0));
    proc.on('error', () => resolve(false));
  });
}

function installPyAutogui(pythonCmd) {
  return new Promise((resolve, reject) => {
    console.log('警告: pyautogui 未安装，正在尝试安装...');
    console.log('Warning: pyautogui not installed, attempting install...');

    const pip = spawn(pythonCmd, ['-m', 'pip', 'install', 'pyautogui'], {
      stdio: 'inherit',
    });

    pip.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error('Failed to install pyautogui. Please run: pip install pyautogui'));
    });
    pip.on('error', reject);
  });
}

function runPythonModule(pythonCmd, args) {
  const child = spawn(pythonCmd, ['-m', 'mouse_keepalive', ...args], {
    stdio: 'inherit',
  });

  child.on('close', (code) => process.exit(code || 0));
  child.on('error', (err) => {
    console.error('错误: 无法启动 Python 模块 / Error: Failed to start Python module');
    console.error(err.message);
    process.exit(1);
  });

  process.on('SIGINT', () => child.kill('SIGINT'));
  process.on('SIGTERM', () => child.kill('SIGTERM'));
}

async function main() {
  try {
    const pythonCmd = await findPython();
    const hasPyAutogui = await checkPyAutogui(pythonCmd);
    if (!hasPyAutogui) {
      await installPyAutogui(pythonCmd);
    }
    runPythonModule(pythonCmd, process.argv.slice(2));
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
}

main();
