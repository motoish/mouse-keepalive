# GitHub Actions 工作流说明

## 工作流列表

### 1. Lint (`lint.yml`)

**触发条件**：
- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request

**功能**：
- Python 代码检查（flake8, black, pylint, mypy）
- Shell 脚本检查（ShellCheck）
- Markdown 检查（markdownlint）
- YAML 检查（yamllint）
- Batch 脚本检查

### 2. Publish (`publish.yml`)

**触发条件**：
- 推送版本标签（格式：`v*.*.*`，如 `v1.0.0`）
- 手动触发（workflow_dispatch）

**功能**：
- 自动发布到 npm
- 自动发布到 PyPI
- 自动创建 GitHub Release

**所需 Secrets**：
- `NPM_TOKEN`: npm 访问令牌（必需，用于发布到 npm）
- `PYPI_TOKEN`: PyPI API 令牌（必需，用于发布到 PyPI）
- `TEST_PYPI_TOKEN` (可选): TestPyPI 令牌（用于测试发布）

**如何配置 Secrets：**

详见下方 [配置 Secrets](#配置-secrets) 章节。

**使用示例**：
```bash
# 创建标签触发发布
git tag v1.0.1
git push origin v1.0.1
```

### 3. Version Bump Helper (`version-bump.yml`)

**触发条件**：手动触发（workflow_dispatch）

**功能**：
- 自动升级版本号（patch/minor/major）
- 更新 `package.json`
- 更新 `pyproject.toml`
- 更新 `mouse_keepalive/__init__.py`
- 可选创建 Pull Request

**使用步骤**：
1. 访问 GitHub Actions 页面
2. 选择 "Version Bump Helper" 工作流
3. 点击 "Run workflow"
4. 选择版本类型（patch/minor/major）
5. 选择是否创建 Pull Request
6. 运行工作流

### 4. Renovate Auto-Approve (`renovate-auto-approve.yml`)

**触发条件**：Renovate 创建的 Pull Request

**功能**：
- 自动测试 Renovate 的依赖更新
- 测试通过后自动批准 PR（仅限 patch 版本）

## 发布流程示例

### 完整发布流程

1. **开发功能**：
   ```bash
   git checkout -b feature/new-feature
   # ... 开发代码 ...
   git commit -m "feat: add new feature"
   git push origin feature/new-feature
   ```

2. **创建 Pull Request**：
   - 在 GitHub 上创建 PR
   - Lint 工作流会自动运行检查

3. **合并 PR**：
   - 审查并合并 PR 到 main 分支

4. **升级版本**：
   - 方式 A：使用 Version Bump Helper 工作流
   - 方式 B：手动编辑版本文件

5. **创建标签并发布**：
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```
   - Publish 工作流会自动运行并发布到 npm 和 PyPI

## 配置 Secrets

### 步骤 1: 获取 npm Token

1. **登录 npm 账户**
   - 访问 https://www.npmjs.com/
   - 如果没有账户，先注册：https://www.npmjs.com/signup

2. **创建 Access Token**
   - 访问 https://www.npmjs.com/settings/YOUR_USERNAME/tokens
   - 点击 "Generate New Token" 按钮
   - 选择类型：**"Automation"**（用于 CI/CD，推荐）
   - 点击 "Generate Token"
   - **⚠️ 重要：立即复制 token**（只显示一次！格式类似：`npm_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

3. **验证包名可用性（可选）**
   ```bash
   npm view mouse-keepalive
   ```
   - 如果返回 404，说明包名可用
   - 如果包名已被占用，需要修改 `package.json` 中的 `name` 字段

### 步骤 2: 获取 PyPI Token

1. **登录 PyPI 账户**
   - 访问 https://pypi.org/
   - 如果没有账户，先注册：https://pypi.org/account/register/

2. **创建 API Token**
   - 访问 https://pypi.org/manage/account/token/
   - 点击 "Add API token" 按钮
   - 输入 token 名称（如：`github-actions-mouse-keepalive`）
   - 选择作用域：
     - **"Entire account"** - 可以发布所有项目（推荐用于个人项目）
     - **"Project: mouse-keepalive"** - 只能发布特定项目（更安全，需要先注册包名）
   - 点击 "Add token"
   - **⚠️ 重要：立即复制 token**（只显示一次！格式类似：`pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

3. **验证包名可用性（可选）**
   - 访问 https://pypi.org/project/mouse-keepalive/
   - 如果显示 404，说明包名可用
   - 如果包名已被占用，需要修改 `pyproject.toml` 中的 `name` 字段

### 步骤 3: 在 GitHub 中配置 Secrets

1. **打开仓库设置**
   - 访问你的 GitHub 仓库：`https://github.com/YOUR_USERNAME/mouse-keepalive`
   - 点击顶部菜单的 **"Settings"**（设置）

2. **进入 Secrets 配置**
   - 在左侧菜单中找到 **"Secrets and variables"**
   - 点击 **"Actions"**

3. **添加 NPM_TOKEN**
   - 点击 **"New repository secret"** 按钮
   - **Name（名称）**：输入 `NPM_TOKEN`（必须完全一致）
   - **Secret（值）**：粘贴之前复制的 npm token
   - 点击 **"Add secret"**

4. **添加 PYPI_TOKEN**
   - 再次点击 **"New repository secret"** 按钮
   - **Name（名称）**：输入 `PYPI_TOKEN`（必须完全一致）
   - **Secret（值）**：粘贴之前复制的 PyPI token
   - 点击 **"Add secret"**

5. **（可选）添加 TEST_PYPI_TOKEN**
   - 如果需要测试发布到 TestPyPI
   - 访问 https://test.pypi.org/manage/account/token/
   - 创建 token（步骤与 PyPI 相同）
   - 在 GitHub 中添加为 `TEST_PYPI_TOKEN`

### 步骤 4: 验证配置

1. **检查 Secrets 是否已添加**
   - 在 GitHub 仓库 Settings → Secrets and variables → Actions
   - 应该能看到：
     - ✅ `NPM_TOKEN`
     - ✅ `PYPI_TOKEN`
     - （可选）`TEST_PYPI_TOKEN`

2. **测试发布（可选）**
   - 可以手动触发 `publish.yml` 工作流进行测试
   - 或者等待 release-please 自动触发

### 常见问题

**Q: npm token 需要什么权限？**
- Automation token 默认有发布权限，无需额外配置
- 确保你的 npm 账户有权限发布到 `mouse-keepalive` 包名

**Q: PyPI token 需要什么权限？**
- 选择 "Entire account" 或 "Project: mouse-keepalive" 都可以
- 如果选择项目级别，需要先注册包名（首次发布时会自动注册）

**Q: 如何验证 token 是否有效？**
- npm: 运行 `npm whoami --registry=https://registry.npmjs.org/`（需要先配置 token）
- PyPI: 可以尝试手动发布一次测试

**Q: token 泄露了怎么办？**
- 立即在对应平台删除旧 token
- 在 GitHub 中更新 Secret 为新 token

**Q: 发布失败怎么办？**
- 检查 Secrets 是否正确配置（名称必须完全一致）
- 检查包名是否已被占用（npm/PyPI）
- 检查版本号是否已存在
- 查看 GitHub Actions 日志获取详细错误信息

## 故障排除

### 发布失败

1. **检查 Secrets**：确保所有必需的 Secrets 都已配置
2. **检查版本号**：确保版本号格式正确且未被使用
3. **查看日志**：在 GitHub Actions 中查看详细错误信息

### 版本冲突

如果版本号已存在：
- npm: 需要更新版本号
- PyPI: 无法覆盖已发布的版本，必须使用新版本号

### 权限错误

确保：
- npm token 有发布权限
- PyPI token 有效且未过期
- GitHub token 有创建 Release 的权限

