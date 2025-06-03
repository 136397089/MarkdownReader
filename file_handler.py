import os

def is_safe_path(path):
    """检查路径是否安全"""
    try:
        normalized = os.path.normpath(path)
        if '..' in normalized or normalized.startswith('/') or normalized.startswith('\\'):
            return False
        return True
    except:
        return False

def get_safe_path(base_dir, relative_path):
    """获取安全的绝对路径"""
    if not is_safe_path(relative_path):
        return None
    
    full_path = os.path.join(base_dir, relative_path)
    try:
        full_path = os.path.abspath(full_path)
        base_dir = os.path.abspath(base_dir)
        if not full_path.startswith(base_dir):
            return None
        return full_path
    except:
        return False

def list_directory(path):
    """列出目录内容"""
    try:
        base_dir = os.getcwd()
        full_path = get_safe_path(base_dir, path)
        
        if not full_path or not os.path.exists(full_path):
            return None, '路径不存在'
            
        dir_items = []
        file_items = []
        
        for item in sorted(os.listdir(full_path)):
            if item.startswith('.'):
                continue
                
            item_path = os.path.join(full_path, item)
            relative_path = os.path.join(path, item) if path else item
            relative_path = relative_path.replace('\\', '/')
            
            if os.path.isdir(item_path):
                dir_items.append({
                    'name': item,
                    'type': 'folder',
                    'path': relative_path
                })
            elif item.lower().endswith(('.md', '.markdown')):
                file_items.append({
                    'name': item,
                    'type': 'markdown',
                    'path': relative_path
                })
                
        return dir_items + file_items, None
        
    except PermissionError:
        return None, '没有权限访问此目录'
    except Exception as e:
        return None, f'服务器错误: {str(e)}'
