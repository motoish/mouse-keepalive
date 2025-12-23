# 发布到 npm 指南

## 准备工作

### 1. 注册 npm 账号

如果还没有 npm 账号，访问 [npmjs.com](https://www.npmjs.com/signup) 注册。

### 2. 登录 npm

```bash
npm login
```

输入你的用户名、密码和邮箱。

### 3. 检查包名可用性

```bash
npm view auto-mouse-mover
```

如果返回 404，说明包名可用。如果已被占用，需要修改 `package.json` 中的 `name` 字段。

## 发布步骤

### 1. 更新版本号

使用语义化版本号（Semantic Versioning）：

```bash
# Patch 版本（修复 bug）
npm version patch

# Minor 版本（新功能）
npm version minor

# Major 版本（破坏性更改）
npm version major
```

或者手动编辑 `package.json` 中的 `version` 字段。

### 2. 测试本地安装

```bash
# 在项目根目录
npm link

# 测试命令
auto-mouse-mover --help
amm --help
```

### 3. 构建和检查

```bash
# 检查将要发布的文件
npm pack --dry-run

# 实际打包（不发布）
npm pack
```

### 4. 发布

```bash
# 发布到 npm
npm publish

# 如果包名包含作用域，需要指定访问权限
npm publish --access public
```

### 5. 验证发布

```bash
# 查看已发布的包信息
npm view auto-mouse-mover

# 测试安装
npm install -g auto-mouse-mover
auto-mouse-mover --help
```

## 发布后

### 1. 创建 Git 标签

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 2. 更新 GitHub Release

在 GitHub 上创建 Release，包含：
- 版本号
- 更新日志
- 下载链接

### 3. 更新文档

确保 README 中的安装说明和示例都是最新的。

## 常见问题

### 包名已被占用

修改 `package.json` 中的 `name` 字段，可以使用：
- 添加作用域：`@your-username/auto-mouse-mover`
- 使用不同的名称

### 发布权限错误

确保：
1. 已登录正确的 npm 账号
2. 包名没有被其他人占用
3. 如果使用作用域包，需要设置 `"access": "public"`

### 版本号冲突

如果版本号已存在，需要更新版本号后再发布。

## 自动化发布（可选）

可以使用 GitHub Actions 自动发布：

1. 创建 `.github/workflows/publish.yml`
2. 配置 npm token 为 GitHub Secret
3. 在发布标签时自动触发发布

## 维护

发布后需要：
- 及时响应 Issue 和 PR
- 定期更新依赖
- 修复 bug 并发布补丁版本
- 添加新功能并发布小版本

