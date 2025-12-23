# 自动发布版本指南

项目已配置 GitHub Actions 工作流，支持自动发布到 npm 和 PyPI。

## 🚀 快速开始

### 方式一：使用 Git 标签发布（最简单，推荐）

这是最简单的方式，只需要创建并推送一个版本标签：

```bash
# 1. 更新版本号（三个文件都要更新）
# 编辑以下文件，将版本号改为新版本（如 1.0.1）：
# - package.json
# - pyproject.toml  
# - auto_mouse_mover/__init__.py

# 2. 提交版本更新
git add package.json pyproject.toml auto_mouse_mover/__init__.py
git commit -m "chore: bump version to 1.0.1"
git push origin main

# 3. 创建并推送版本标签
git tag v1.0.1
git push origin v1.0.1

# 4. 完成！GitHub Actions 会自动：
#    - 发布到 npm
#    - 发布到 PyPI
#    - 创建 GitHub Release
```

### 方式二：使用 GitHub Actions 版本升级工作流

1. **访问 GitHub Actions**：
   - 打开 https://github.com/motoish/auto-mouse-mover/actions
   - 点击左侧 "Version Bump Helper" 工作流

2. **运行工作流**：
   - 点击 "Run workflow"
   - 选择版本类型：
     - `patch`: 1.0.0 → 1.0.1 (修复 bug)
     - `minor`: 1.0.0 → 1.1.0 (新功能)
     - `major`: 1.0.0 → 2.0.0 (破坏性更改)
   - 选择是否创建 Pull Request
   - 点击 "Run workflow"

3. **如果创建了 PR**：
   - 审查并合并 PR
   - 然后创建标签触发发布（见方式一第3步）

4. **如果没有创建 PR**：
   - 工作流会直接更新版本号并推送到 main 分支
   - 然后创建标签触发发布（见方式一第3步）

### 方式三：手动触发发布工作流

如果你已经手动更新了版本号并推送到 main：

1. **访问 GitHub Actions**：
   - 打开 https://github.com/motoish/auto-mouse-mover/actions
   - 点击左侧 "Publish to npm and PyPI" 工作流

2. **运行工作流**：
   - 点击 "Run workflow"
   - 输入版本号（如：1.0.1）
   - 点击 "Run workflow"

3. **工作流会自动**：
   - 更新版本文件
   - 发布到 npm
   - 发布到 PyPI
   - 创建 GitHub Release

## 📋 前置条件

### 1. 配置 GitHub Secrets

在发布前，需要在 GitHub 仓库设置中配置以下 Secrets：

**访问路径**：`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

#### NPM_TOKEN
1. 访问 https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. 点击 "Generate New Token"
3. 选择 "Automation" 类型
4. 复制生成的 token
5. 在 GitHub 中添加为 Secret：`NPM_TOKEN`

#### PYPI_TOKEN
1. 访问 https://pypi.org/manage/account/token/
2. 点击 "Add API token"
3. 输入 token 名称（如：`github-actions`）
4. 选择作用域（整个账户或特定项目）
5. 复制生成的 token（只显示一次！）
6. 在 GitHub 中添加为 Secret：`PYPI_TOKEN`

### 2. 验证配置

推送标签后，访问 GitHub Actions 页面查看发布进度：
- https://github.com/motoish/auto-mouse-mover/actions

## 🔍 发布流程说明

### 工作流触发条件

发布工作流会在以下情况自动触发：

1. **推送版本标签**（格式：`v*.*.*`）
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

2. **手动触发**（workflow_dispatch）
   - 在 GitHub Actions 页面手动运行

### 发布步骤

工作流会自动执行以下步骤：

1. ✅ **提取版本号**（从标签或输入）
2. ✅ **更新版本文件**（package.json, pyproject.toml, __init__.py）
3. ✅ **构建包**
   - npm: `npm pack`
   - PyPI: `python -m build`
4. ✅ **发布到 npm**
5. ✅ **发布到 PyPI**
6. ✅ **创建 GitHub Release**

### 验证发布

发布完成后，可以验证：

```bash
# 验证 npm
npm view auto-mouse-mover version

# 验证 PyPI
pip index versions auto-mouse-mover
```

## 📝 版本号规范

使用 [语义化版本](https://semver.org/)：

- **MAJOR** (主版本号): 不兼容的 API 修改
- **MINOR** (次版本号): 向下兼容的功能性新增
- **PATCH** (修订号): 向下兼容的问题修正

示例：
- `1.0.0` → `1.0.1` (patch: 修复 bug)
- `1.0.0` → `1.1.0` (minor: 新功能)
- `1.0.0` → `2.0.0` (major: 破坏性更改)

## 🎯 完整发布示例

假设要发布版本 `1.0.1`：

```bash
# 1. 更新版本号
# 编辑 package.json: "version": "1.0.1"
# 编辑 pyproject.toml: version = "1.0.1"
# 编辑 auto_mouse_mover/__init__.py: __version__ = "1.0.1"

# 2. 提交更改
git add package.json pyproject.toml auto_mouse_mover/__init__.py
git commit -m "chore: bump version to 1.0.1"
git push origin main

# 3. 创建并推送标签
git tag v1.0.1
git push origin v1.0.1

# 4. 等待 GitHub Actions 完成发布
# 查看进度：https://github.com/motoish/auto-mouse-mover/actions

# 5. 验证发布
npm view auto-mouse-mover version
pip index versions auto-mouse-mover
```

## ⚠️ 注意事项

1. **版本号唯一性**：
   - npm 和 PyPI 都不允许覆盖已发布的版本
   - 如果版本号已存在，需要更新版本号

2. **标签格式**：
   - 必须使用 `v` 前缀：`v1.0.1`
   - 格式：`v*.*.*`

3. **强制推送**：
   - 如果标签已存在，需要先删除：
     ```bash
     git tag -d v1.0.1
     git push origin :refs/tags/v1.0.1
     ```

4. **发布失败处理**：
   - 查看 GitHub Actions 日志
   - 检查 Secrets 配置是否正确
   - 确认版本号未被使用

## 🔗 相关链接

- [GitHub Actions](https://github.com/motoish/auto-mouse-mover/actions)
- [npm 包页面](https://www.npmjs.com/package/auto-mouse-mover)
- [PyPI 包页面](https://pypi.org/project/auto-mouse-mover/)
- [详细发布文档](PUBLISH.md)

