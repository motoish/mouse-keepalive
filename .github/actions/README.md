# GitHub Actions 模块化结构

本项目采用模块化的 GitHub Actions 架构，将各个功能拆分为独立的 Composite Actions，由主工作流统一调用。

## 📁 目录结构

```
.github/
├── actions/              # Composite Actions（可复用的操作模块）
│   ├── lint/            # 代码检查
│   │   └── action.yml
│   ├── build/           # 构建可执行文件
│   │   └── action.yml
│   ├── release/         # 版本管理和 Release PR
│   │   └── action.yml
│   └── publish/         # 发布到 npm 和 PyPI
│       └── action.yml
└── workflows/           # 主工作流（编排各个 actions）
    ├── ci.yml           # CI 主工作流
    ├── release.yml      # Release 主工作流
    └── release-please.yml  # Release Please 工作流
```

## 🔧 Actions 说明

### 1. Lint Action (`lint/action.yml`)

运行所有代码检查工具：
- Python: flake8, black, pylint, mypy
- Shell: ShellCheck
- Markdown: markdownlint
- YAML: yamllint
- Batch: 语法检查

**使用示例：**
```yaml
- name: Run Lint
  uses: ./.github/actions/lint
  with:
    python-version: '3.11'
```

### 2. Build Action (`build/action.yml`)

使用 PyInstaller 构建跨平台可执行文件。

**输入参数：**
- `version`: 版本号
- `platform`: 平台 (linux, darwin, win32)
- `artifact-name`: 产物名称

**使用示例：**
```yaml
- name: Build executable
  uses: ./.github/actions/build
  with:
    version: '1.0.0'
    platform: 'linux'
    artifact-name: 'mouse-keepalive-linux-x86_64'
```

### 3. Release Action (`release/action.yml`)

运行 release-please 管理版本和创建 Release PR。

**输入参数：**
- `config-file`: release-please 配置文件路径（默认：`release-please-config.json`）
- `manifest-file`: release-please manifest 文件路径（默认：`release-please-config.json`）

**输出：**
- `release-created`: 是否创建了 release
- `tag-name`: 标签名称
- `version`: 版本号

**使用示例：**
```yaml
- name: Run release-please
  id: release
  uses: ./.github/actions/release
```

### 4. Publish Action (`publish/action.yml`)

发布到 npm 和/或 PyPI。

**输入参数：**
- `version`: 要发布的版本号
- `publish-npm`: 是否发布到 npm（默认：`true`）
- `publish-pypi`: 是否发布到 PyPI（默认：`true`）

**使用示例：**
```yaml
- name: Publish packages
  uses: ./.github/actions/publish
  with:
    version: '1.0.0'
    publish-npm: 'true'
    publish-pypi: 'true'
```

## 🚀 工作流说明

### CI 工作流 (`ci.yml`)

在 push 或 PR 时运行：
- 调用 `lint` action 进行代码检查

### Release 工作流 (`release.yml`)

在推送 tag 或创建 release 时运行：
- 并行构建多个平台的可执行文件（使用 `build` action）
- 发布到 npm 和 PyPI（使用 `publish` action）
- 上传产物到 GitHub Release

### Release Please 工作流 (`release-please.yml`)

在 Lint 工作流成功后运行：
- 使用 `release` action 管理版本和创建 Release PR

## 💡 优势

1. **模块化**：每个功能独立，易于维护和测试
2. **可复用**：Actions 可以在多个工作流中复用
3. **清晰**：主工作流只负责编排，具体逻辑在 actions 中
4. **灵活**：可以轻松添加新的 actions 或修改现有功能
5. **测试友好**：可以单独测试每个 action

## 📝 添加新的 Action

1. 在 `.github/actions/` 下创建新目录
2. 创建 `action.yml` 文件
3. 定义 inputs、outputs 和 steps
4. 在主工作流中调用

**示例：**
```yaml
# .github/actions/test/action.yml
name: 'Run Tests'
description: 'Run test suite'

inputs:
  test-type:
    description: 'Type of tests to run'
    required: false
    default: 'all'

runs:
  using: 'composite'
  steps:
    - name: Run tests
      shell: bash
      run: |
        pytest tests/
```

## 🔗 相关文档

- [GitHub Actions Composite Actions](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- [GitHub Actions Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)

