# GitHub 仓库设置指南

## 将项目推送到 GitHub

### 1. 在 GitHub 上创建新仓库

1. 登录 GitHub
2. 点击右上角的 "+" 号，选择 "New repository"
3. 输入仓库名称（例如：`auto-mouse-mover`）
4. 选择 Public 或 Private
5. **不要**勾选 "Initialize this repository with a README"（因为本地已有文件）
6. 点击 "Create repository"

### 2. 连接本地仓库到 GitHub

在终端中运行以下命令（将 `YOUR_USERNAME` 替换为你的 GitHub 用户名）：

```bash
cd ~/repository/auto-mouse-mover

# 添加远程仓库（替换 YOUR_USERNAME 和 REPO_NAME）
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 或者使用 SSH（如果你配置了 SSH key）
# git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git

# 推送到 GitHub
git push -u origin main
```

### 3. 验证推送

访问你的 GitHub 仓库页面，应该能看到所有文件已经上传。

## 后续更新

当你修改了代码后，使用以下命令推送更新：

```bash
git add .
git commit -m "你的提交信息"
git push
```

