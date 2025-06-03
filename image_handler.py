import re
import os
from config import ALLOWED_IMAGE_EXTENSIONS
from file_handler import get_safe_path, is_safe_path
import mimetypes
from flask import send_file, jsonify

def process_markdown_images(html_content, file_path):
    """处理Markdown中的图片链接"""
    if not file_path:
        return html_content
    
    file_dir = os.path.dirname(file_path)
    img_pattern = r'<img([^>]*?)src=[\'"](.*?)[\'"]([^>]*?)>'
    
    def replace_img(match):
        pre_attrs = match.group(1)
        src = match.group(2)
        post_attrs = match.group(3)
        
        if src.startswith(('http://', 'https://', 'data:', '/')):
            return match.group(0)
        
        if file_dir:
            image_path = os.path.join(file_dir, src).replace('\\', '/')
        else:
            image_path = src
        
        new_src = f'/api/image?path={image_path}'
        return f'<img{pre_attrs}src="{new_src}"{post_attrs}>'
    
    return re.sub(img_pattern, replace_img, html_content)

def serve_image(image_path):
    """处理图片请求"""
    try:
        if not image_path or not is_safe_path(image_path):
            return jsonify({'error': '无效的图片路径'}), 400
        
        base_dir = os.getcwd()
        full_path = get_safe_path(base_dir, image_path)
        
        if not full_path or not os.path.exists(full_path):
            return jsonify({'error': '图片文件不存在'}), 404
        
        file_ext = os.path.splitext(full_path)[1].lower()
        if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
            return jsonify({'error': '不支持的图片格式'}), 400
        
        mime_type, _ = mimetypes.guess_type(full_path)
        if not mime_type or not mime_type.startswith('image/'):
            mime_type = 'image/jpeg'
        
        return send_file(
            full_path,
            mimetype=mime_type,
            as_attachment=False,
            conditional=True
        )
    except Exception as e:
        print(f"图片API错误: {e}")
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500
