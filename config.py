import secrets

# 配置
CONFIG = {
    'password_hash': None,
    'session_timeout': 10000,
}

# 支持的图片格式
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico'}

# Session密钥
SECRET_KEY = secrets.token_hex(32)


password = 'admin123'