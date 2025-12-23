# GitHub 仓库设置指南

## 在 GitHub 上创建仓库

1. 访问 [GitHub](https://github.com) 并登录
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `auto-mouse-mover`
   - Description: `自动移动鼠标工具，支持 macOS 和 Windows`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（因为我们已经有了）
4. 点击 "Create repository"

## 连接本地仓库到 GitHub

创建仓库后，GitHub 会显示设置说明。运行以下命令：

```bash
cd /Users/mtngtnsh/repository/auto-mouse-mover

# 添加远程仓库（将 YOUR_USERNAME 替换为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/auto-mouse-mover.git

# 或者使用 SSH（如果你配置了 SSH key）
# git remote add origin git@github.com:YOUR_USERNAME/auto-mouse-mover.git

# 推送代码到 GitHub
git branch -M main
git push -u origin main
```

## 使用 GitHub CLI（如果已安装）

如果你安装了 GitHub CLI (`gh`)，可以使用以下命令快速创建仓库：

```bash
cd /Users/mtngtnsh/repository/auto-mouse-mover

# 创建并推送仓库
gh repo create auto-mouse-mover --public --source=. --remote=origin --push
```

## 验证

推送成功后，访问 `https://github.com/YOUR_USERNAME/auto-mouse-mover` 查看你的仓库。

