# 📁 目录结构

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
