from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import markdown
import ssl
from datetime import datetime
from auth import require_auth, verify_password, PUBLIC_KEY_PEM
from image_handler import process_markdown_images, serve_image
from file_handler import get_safe_path, is_safe_path, list_directory
from templates import LOGIN_TEMPLATE, MAIN_TEMPLATE
from config import SECRET_KEY, CONFIG
import os
app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/login')
def login():
    if session.get('authenticated'):
        return redirect(url_for('index'))
    error = request.args.get('error')
    return render_template_string(LOGIN_TEMPLATE, public_key=PUBLIC_KEY_PEM, error=error)

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        encrypted_password = data.get('encrypted_password')
        
        if not encrypted_password:
            return jsonify({'success': False, 'error': '缺少密码'})
        
        if verify_password(encrypted_password):
            session['authenticated'] = True
            session['login_time'] = datetime.now().isoformat()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': '密码错误'})
            
    except Exception as e:
        print(f"登录错误: {e}")
        return jsonify({'success': False, 'error': '登录失败'})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/')
@require_auth
def index():
    return render_template_string(MAIN_TEMPLATE)

@app.route('/api/files')
@require_auth
def list_files():
    path = request.args.get('path', '')
    items, error = list_directory(path)
    
    if error:
        return jsonify({'error': error})
    
    return jsonify({
        'current_path': path,
        'items': items
    })

@app.route('/api/markdown')
@require_auth
def get_markdown():
    try:
        file_path = request.args.get('file', '')
        
        if not file_path or not is_safe_path(file_path):
            return jsonify({'error': '无效的文件路径'})
        
        if not file_path.lower().endswith(('.md', '.markdown')):
            return jsonify({'error': '不是Markdown文件'})
        
        base_dir = os.getcwd()
        full_path = get_safe_path(base_dir, file_path)
        
        if not full_path or not os.path.exists(full_path):
            return jsonify({'error': '文件不存在'})
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(full_path, 'r', encoding='gbk') as f:
                content = f.read()
        
        html = markdown.markdown(
            content,
            extensions=['codehilite', 'tables', 'toc', 'fenced_code', 'extra'],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight'
                }
            }
        )
        
        html = process_markdown_images(html, file_path)
        
        return jsonify({
            'html': html,
            'file_path': file_path
        })
        
    except Exception as e:
        return jsonify({'error': f'读取文件失败: {str(e)}'})

@app.route('/api/image')
@require_auth
def get_image():
    image_path = request.args.get('path', '')
    return serve_image(image_path)

def create_ssl_context():
    cert_file = 'server.crt'
    key_file = 'server.key'
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("正在生成自签名SSL证书...")
        os.system(f'''
        openssl req -x509 -newkey rsa:4096 -keyout {key_file} -out {cert_file} -days 365 -nodes -subj "/C=CN/ST=State/L=City/O=Organization/CN=localhost"
        ''')
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(cert_file, key_file)
    return context

if __name__ == '__main__':
    # ... 启动信息打印代码 ...
    ssl_context = create_ssl_context()
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context=ssl_context)
