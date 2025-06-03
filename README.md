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
```
2. 运行应用:

```bash
python app.py
```


3. 访问地址:
HTTPS: https://localhost:5000
默认密码: admin123

## 功能说明
数学公式支持
行内公式: $E = mc^2$
块级公式: $$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$
支持完整LaTeX语法
## 图片支持
支持格式: JPG, PNG, GIF, BMP, WebP, SVG等
相对路径: !描述
自动安全检查，防止路径遍历攻击
## 文件结构
app.py - 主程序入口
auth.py - 认证相关模块
config.py - 配置文件
file_handler.py - 文件处理模块
image_handler.py - 图片处理模块
markdown_reader.py - Markdown处理核心
templates.py - HTML模板
## 安全特性
HTTPS加密传输
RSA密码加密
路径遍历攻击防护
会话超时自动登出
图片访问安全检查
## 注意事项
首次运行时会自动生成自签名SSL证书，浏览器可能会显示安全警告，选择继续访问即可。

## 开发环境
Python 3.6+
Flask Web框架
MathJax数学公式渲染
RSA-2048密码加密

## 许可证
本项目采用 MIT 许可证。

详见 [LICENSE](LICENSE) 文件。

Copyright (c) 2024 MarkdownReader