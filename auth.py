from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from functools import wraps
from flask import session, redirect, url_for
from datetime import datetime, timedelta
import base64
from config import CONFIG,password

def generate_key_pair():
    """生成RSA密钥对"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# 全局密钥对
PRIVATE_KEY, PUBLIC_KEY = generate_key_pair()

# 将公钥转换为PEM格式字符串
PUBLIC_KEY_PEM = PUBLIC_KEY.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

def decrypt_password(encrypted_password_b64):
    """解密密码"""
    try:
        encrypted_password = base64.b64decode(encrypted_password_b64)
        decrypted_password = PRIVATE_KEY.decrypt(
            encrypted_password,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_password.decode('utf-8')
    except Exception as e:
        print(f"解密失败: {e}")
        return None

def verify_password(encrypted_password_b64, stored_password = password):
    """验证密码"""
    decrypted_password = decrypt_password(encrypted_password_b64)
    return decrypted_password == stored_password

def require_auth(f):
    """装饰器：要求认证"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        
        if session.get('login_time'):
            login_time = datetime.fromisoformat(session['login_time'])
            if datetime.now() - login_time > timedelta(seconds=CONFIG['session_timeout']):
                session.clear()
                return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function
