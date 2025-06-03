# 安全Markdown阅读器

一个基于Flask的安全Markdown阅读器，支持数学公式和本地图片显示。

## 主要特性

- 🔐 HTTPS加密传输
- 🔑 RSA-2048非对称加密密码验证 
- 📝 完整Markdown语法支持
- ∑ LaTeX数学公式渲染
- 🖼️ 本地图片显示
- 🛡️ 路径遍历攻击防护
- ⌛ 会话管理和超时控制

## 安装和运行

1. 安装依赖:

```bash
pip install flask markdown cryptography pillow -i https://pypi.tuna.tsinghua.edu.cn/simple --user