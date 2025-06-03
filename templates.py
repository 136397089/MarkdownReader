# 登录页面HTML模板
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录 - Markdown阅读器</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .login-header h1 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .login-header p {
            color: #666;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }
        
        .login-btn {
            width: 100%;
            background: #667eea;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .login-btn:hover {
            background: #5a67d8;
        }
        
        .login-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .error {
            color: #dc3545;
            background-color: #f8d7da;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .security-info {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            font-size: 12px;
            color: #666;
        }
        
        .security-info h4 {
            margin-bottom: 8px;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>🔐 安全登录</h1>
            <p>Markdown阅读器 - 安全访问</p>
        </div>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form id="loginForm">
            <div class="form-group">
                <label for="password">密码：</label>
                <input type="password" id="password" name="password" required 
                       placeholder="请输入密码" autocomplete="current-password">
            </div>
            
            <button type="submit" class="login-btn" id="loginBtn">
                <span id="btnText">登录</span>
            </button>
        </form>
        
        <div class="security-info">
            <h4>🛡️ 安全说明</h4>
            <p>• 密码使用RSA-2048非对称加密传输</p>
            <p>• 所有通信均通过HTTPS加密</p>
            <p>• 会话将在1小时后自动过期</p>
            <p>• 支持本地图片显示</p>
        </div>
    </div>

    <script>
        const PUBLIC_KEY = `{{ public_key }}`;
        
        async function encryptPassword(password) {
            try {
                const keyData = PUBLIC_KEY.replace(/-----BEGIN PUBLIC KEY-----/, '')
                                        .replace(/-----END PUBLIC KEY-----/, '')
                                        .replace(/\\s/g, '');
                
                const binaryKey = Uint8Array.from(atob(keyData), c => c.charCodeAt(0));
                
                const publicKey = await window.crypto.subtle.importKey(
                    'spki',
                    binaryKey,
                    {
                        name: 'RSA-OAEP',
                        hash: 'SHA-256',
                    },
                    false,
                    ['encrypt']
                );
                
                const encodedPassword = new TextEncoder().encode(password);
                const encrypted = await window.crypto.subtle.encrypt(
                    'RSA-OAEP',
                    publicKey,
                    encodedPassword
                );
                
                return btoa(String.fromCharCode(...new Uint8Array(encrypted)));
            } catch (error) {
                console.error('加密失败:', error);
                throw new Error('密码加密失败');
            }
        }
        
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const password = document.getElementById('password').value;
            const loginBtn = document.getElementById('loginBtn');
            const btnText = document.getElementById('btnText');
            
            if (!password) {
                alert('请输入密码');
                return;
            }
            
            loginBtn.disabled = true;
            btnText.textContent = '加密中...';
            
            try {
                const encryptedPassword = await encryptPassword(password);
                
                btnText.textContent = '登录中...';
                
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        encrypted_password: encryptedPassword
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    window.location.href = '/';
                } else {
                    alert('登录失败: ' + (result.error || '密码错误'));
                }
            } catch (error) {
                console.error('登录错误:', error);
                alert('登录失败: ' + error.message);
            } finally {
                loginBtn.disabled = false;
                btnText.textContent = '登录';
                document.getElementById('password').value = '';
            }
        });
    </script>
</body>
</html>
'''

# 主页面HTML模板 - 添加了图片支持说明
MAIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown阅读器</title>
    
    <!-- MathJax配置 -->
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\$', '\\\$']],
                displayMath: [['$$', '$$'], ['\\\$', '\\\$']],
                processEscapes: true,
                processEnvironments: true,
                tags: 'ams',
                macros: {
                    // 常用数学宏定义
                    RR: "\\\\mathbb{R}",
                    NN: "\\\\mathbb{N}",
                    ZZ: "\\\\mathbb{Z}",
                    QQ: "\\\\mathbb{Q}",
                    CC: "\\\\mathbb{C}",
                    dd: "\\\\mathrm{d}",
                    ee: "\\\\mathrm{e}",
                    ii: "\\\\mathrm{i}",
                    jj: "\\\\mathrm{j}",
                    Re: "\\\\operatorname{Re}",
                    Im: "\\\\operatorname{Im}",
                    Tr: "\\\\operatorname{Tr}",
                    rank: "\\\\operatorname{rank}",
                    span: "\\\\operatorname{span}",
                    dim: "\\\\operatorname{dim}",
                    ker: "\\\\operatorname{ker}",
                    det: "\\\\operatorname{det}",
                    gcd: "\\\\operatorname{gcd}",
                    lcm: "\\\\operatorname{lcm}",
                    max: "\\\\operatorname{max}",
                    min: "\\\\operatorname{min}",
                    sup: "\\\\operatorname{sup}",
                    inf: "\\\\operatorname{inf}",
                    lim: "\\\\operatorname{lim}",
                    limsup: "\\\\operatorname{limsup}",
                    liminf: "\\\\operatorname{liminf}"
                }
            },
            svg: {
                fontCache: 'global'
            },
            options: {
                renderActions: {
                    addMenu: [0, '', '']
                }
            },
            startup: {
                ready: () => {
                    MathJax.startup.defaultReady();
                    console.log('MathJax已加载完成');
                }
            }
        };
    </script>
    
    <!-- 加载MathJax -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            height: 100vh;
            overflow: hidden;
        }
        
        .app-container {
            display: flex;
            height: 100vh;
        }
        
        .sidebar {
            width: 350px;
            background: white;
            border-right: 1px solid #dee2e6;
            display: flex;
            flex-direction: column;
            transition: margin-left 0.3s ease;
        }
        
        .sidebar.hidden {
            margin-left: -350px;
        }
        
        .sidebar-header {
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
            background-color: #f8f9fa;
        }
        
        .sidebar-header h2 {
            margin-bottom: 5px;
            color: #495057;
            font-size: 18px;
        }
        
        .sidebar-content {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }
        
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            min-width: 0;
        }
        
        .header {
            background: white;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .header-left {
            display: flex;
            align-items: center;
        }
        
        .header-right {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .toggle-sidebar {
            background: #6c757d;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 15px;
            font-size: 14px;
        }
        
        .toggle-sidebar:hover {
            background: #5a6268;
        }
        
        .logout-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .logout-btn:hover {
            background: #c82333;
        }
        
        .user-info {
            color: #666;
            font-size: 14px;
        }
        
        .security-badge {
            background: #28a745;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .math-badge {
            background: #17a2b8;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .image-badge {
            background: #6f42c1;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        
        .content {
            flex: 1;
            background: white;
            padding: 30px;
            overflow-y: auto;
            margin: 0;
        }
        
        .file-list {
            list-style: none;
        }
        
        .file-item {
            padding: 10px 12px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-bottom: 2px;
        }
        
        .file-item:hover {
            background-color: #f5f5f5;
        }
        
        .file-item.folder {
            font-weight: 500;
            color: #007bff;
        }
        
        .file-item.markdown {
            color: #28a745;
        }
        
        .file-item.active {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        
        .current-path {
            font-size: 12px;
            color: #666;
            margin-bottom: 15px;
            padding: 8px 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #e9ecef;
        }
        
        .markdown-content {
            line-height: 1.8;
            max-width: none;
        }
        
        .markdown-content h1, .markdown-content h2, .markdown-content h3 {
            margin-top: 2em;
            margin-bottom: 1em;
            color: #2c3e50;
        }
        
        .markdown-content h1 {
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        
        .markdown-content pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 1em 0;
        }
        
        .markdown-content code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        
        .markdown-content blockquote {
            border-left: 4px solid #007bff;
            margin: 1em 0;
            padding-left: 1em;
            color: #666;
        }
        
        .markdown-content table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        
        .markdown-content th, .markdown-content td {
            border: 1px solid #dee2e6;
            padding: 8px 12px;
            text-align: left;
        }
        
        .markdown-content th {
            background-color: #f8f9fa;
            font-weight: 600;
        }
        
        /* 图片样式优化 */
        .markdown-content img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 1em 0;
            cursor: zoom-in;
            transition: transform 0.3s ease;
        }
        
        .markdown-content img:hover {
            transform: scale(1.02);
        }
        
        /* 图片加载失败样式 */
        .markdown-content img[alt]:after {
            content: " (图片: " attr(alt) ")";
            color: #666;
            font-style: italic;
        }
        
        /* MathJax数学公式样式优化 */
        .markdown-content .MathJax {
            font-size: 1.1em !important;
        }
        
        .markdown-content .MathJax_Display {
            margin: 1.5em 0 !important;
            text-align: center;
        }
        
        .markdown-content mjx-container[jax="CHTML"][display="true"] {
            margin: 1.5em 0;
            text-align: center;
        }
        
        .markdown-content mjx-container[jax="CHTML"] {
            line-height: 1.2;
        }
        
        /* 数学公式背景高亮 */
        .markdown-content .math-inline {
            background-color: rgba(0, 123, 255, 0.05);
            padding: 2px 4px;
            border-radius: 3px;
            margin: 0 2px;
        }
        
        .markdown-content .math-display {
            background-color: rgba(0, 123, 255, 0.02);
            padding: 15px;
            border-radius: 5px;
            margin: 1.5em 0;
            border-left: 3px solid #007bff;
        }
        
        .loading {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 50px;
        }
        
        .error {
            color: #dc3545;
            background-color: #f8d7da;
            padding: 15px;
            border-radius: 5px;
            margin: 1em 0;
        }
        
        .back-button {
            background-color: #6c757d;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 15px;
            font-size: 12px;
        }
        
        .back-button:hover {
            background-color: #5a6268;
        }
        
        .welcome-message {
            text-align: center;
            color: #666;
            padding: 50px;
        }
        
        .welcome-message h2 {
            margin-bottom: 15px;
            color: #495057;
        }
        
        .math-examples {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #17a2b8;
        }
        
        .math-examples h3 {
            color: #17a2b8;
            margin-bottom: 15px;
        }
        
        .math-examples p {
            margin-bottom: 10px;
            font-size: 14px;
        }
        
        .image-examples {
            margin-top: 20px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #6f42c1;
        }
        
        .image-examples h3 {
            color: #6f42c1;
            margin-bottom: 15px;
        }
        
        .image-examples p {
            margin-bottom: 10px;
            font-size: 14px;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .sidebar {
                width: 280px;
            }
            
            .sidebar.hidden {
                margin-left: -280px;
            }
            
            .content {
                padding: 20px 15px;
            }
            
            .header {
                padding: 15px 20px;
            }
            
            .header-right {
                flex-direction: column;
                gap: 8px;
            }
        }
        
        /* 滚动条样式 */
        .sidebar-content::-webkit-scrollbar,
        .content::-webkit-scrollbar {
            width: 6px;
        }
        
        .sidebar-content::-webkit-scrollbar-track,
        .content::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        .sidebar-content::-webkit-scrollbar-thumb,
        .content::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 3px;
        }
        
        .sidebar-content::-webkit-scrollbar-thumb:hover,
        .content::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- 左侧文件浏览器 -->
        <div class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <h2>📁 文件浏览器</h2>
            </div>
            <div class="sidebar-content">
                <div class="current-path" id="currentPath">当前路径: /</div>
                <button class="back-button" id="backButton" onclick="goBack()" style="display: none;">← 返回上级</button>
                <ul class="file-list" id="fileList">
                    <!-- 文件列表将通过JavaScript动态加载 -->
                </ul>
            </div>
        </div>
        
        <!-- 主内容区域 -->
        <div class="main-content">
            <div class="header">
                <div class="header-left">
                    <button class="toggle-sidebar" onclick="toggleSidebar()">
                        <span id="toggleIcon">◀</span> 文件
                    </button>
                    <h1>📖 Markdown阅读器</h1>
                </div>
                <div class="header-right">
                    <span class="security-badge">🔒 HTTPS</span>
                    <span class="math-badge">∑ LaTeX</span>
                    <span class="image-badge">🖼️ 图片</span>
                    <span class="user-info">已认证用户</span>
                    <button class="logout-btn" onclick="logout()">退出登录</button>
                </div>
            </div>
            
            <div class="content">
                <div id="markdownContent">
                    <div class="welcome-message">
                        <h2>欢迎使用安全Markdown阅读器</h2>
                        <p>请从左侧文件浏览器选择一个Markdown文件开始阅读...</p>
                        <p>点击左上角的"文件"按钮可以隐藏/显示文件浏览器</p>
                        <p>🔐 当前连接已通过HTTPS加密保护</p>
                        <p>∑ 支持LaTeX数学公式渲染</p>
                        <p>🖼️ 支持本地图片显示</p>
                        
                        <div class="math-examples">
                            <h3>📐 数学公式示例</h3>
                            <p><strong>行内公式：</strong>使用单个$符号包围，如 $E = mc^2$</p>
                            <p><strong>块级公式：</strong>使用双$符号包围：</p>
                            $$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$
                            <p><strong>矩阵示例：</strong></p>
                            $$\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$$
                            <p><strong>求和公式：</strong></p>
                            $$\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}$$
                        </div>
                        
                        <div class="image-examples">
                            <h3>🖼️ 图片支持说明</h3>
                            <p><strong>支持格式：</strong>JPG, PNG, GIF, BMP, WebP, SVG等</p>
                            <p><strong>相对路径：</strong>![描述](./images/pic.jpg)</p>
                            <p><strong>绝对路径：</strong>![描述](/path/to/image.png)</p>
                            <p><strong>网络图片：</strong>![描述](https://example.com/image.jpg)</p>
                            <p><strong>安全特性：</strong>自动防护路径遍历攻击，确保文件访问安全</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentPath = '';
        let currentFile = '';
        let sidebarVisible = true;
        
        // 页面加载时获取文件列表
        window.onload = function() {
            loadFileList('');
        };
        
        // 退出登录
        function logout() {
            if (confirm('确定要退出登录吗？')) {
                fetch('/api/logout', { method: 'POST' })
                .then(() => {
                    window.location.href = '/login';
                });
            }
        }
        
        // 切换侧边栏显示/隐藏
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const toggleIcon = document.getElementById('toggleIcon');
            
            sidebarVisible = !sidebarVisible;
            
            if (sidebarVisible) {
                sidebar.classList.remove('hidden');
                toggleIcon.textContent = '◀';
            } else {
                sidebar.classList.add('hidden');
                toggleIcon.textContent = '▶';
            }
        }
        
        // 加载文件列表
        function loadFileList(path) {
            fetch(`/api/files?path=${encodeURIComponent(path)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('fileList').innerHTML = 
                            `<li class="error">错误: ${data.error}</li>`;
                        return;
                    }
                    
                    currentPath = data.current_path;
                    document.getElementById('currentPath').textContent = 
                        `当前路径: ${currentPath || '/'}`;
                    
                    const backButton = document.getElementById('backButton');
                    if (currentPath) {
                        backButton.style.display = 'inline-block';
                    } else {
                        backButton.style.display = 'none';
                    }
                    
                    const fileList = document.getElementById('fileList');
                    fileList.innerHTML = '';
                    
                    data.items.forEach(item => {
                        const li = document.createElement('li');
                        li.className = `file-item ${item.type}`;
                        
                        if (item.type === 'folder') {
                            li.innerHTML = `📁 ${item.name}`;
                            li.onclick = () => loadFileList(item.path);
                        } else if (item.type === 'markdown') {
                            li.innerHTML = `📄 ${item.name}`;
                            li.onclick = () => {
                                loadMarkdownFile(item.path);
                                document.querySelectorAll('.file-item').forEach(el => 
                                    el.classList.remove('active'));
                                li.classList.add('active');
                                currentFile = item.path;
                            };
                        } else {
                            li.innerHTML = `📄 ${item.name}`;
                            li.style.color = '#999';
                        }
                        
                        fileList.appendChild(li);
                    });
                    
                    if (currentFile) {
                        const items = document.querySelectorAll('.file-item.markdown');
                        items.forEach(item => {
                            if (item.textContent.includes(currentFile.split('/').pop())) {
                                item.classList.add('active');
                            }
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('fileList').innerHTML = 
                        '<li class="error">加载文件列表失败</li>';
                });
        }
        
        // 返回上级目录
        function goBack() {
            const parentPath = currentPath.split('/').slice(0, -1).join('/');
            loadFileList(parentPath);
        }
        
        // 加载Markdown文件
        function loadMarkdownFile(filePath) {
            document.getElementById('markdownContent').innerHTML = 
                '<div class="loading">正在加载...</div>';
            
            fetch(`/api/markdown?file=${encodeURIComponent(filePath)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('markdownContent').innerHTML = 
                            `<div class="error">错误: ${data.error}</div>`;
                        return;
                    }
                    
                    document.getElementById('markdownContent').innerHTML = 
                        `<div class="markdown-content">${data.html}</div>`;
                    
                    // 重新渲染MathJax
                    if (window.MathJax) {
                        MathJax.typesetPromise([document.getElementById('markdownContent')])
                        .then(() => {
                            console.log('MathJax渲染完成');
                            // 为数学公式添加样式类
                            addMathStyles();
                        })
                        .catch((err) => console.log('MathJax渲染错误:', err));
                    }
                    
                    // 处理图片加载错误
                    const images = document.querySelectorAll('#markdownContent img');
                    images.forEach(img => {
                        img.onerror = function() {
                            this.style.border = '2px dashed #dc3545';
                            this.style.padding = '10px';
                            this.style.backgroundColor = '#f8d7da';
                            this.style.color = '#721c24';
                            this.title = '图片加载失败: ' + this.src;
                        };
                        
                        // 添加图片点击放大功能
                        img.onclick = function() {
                            if (this.style.transform === 'scale(2)') {
                                this.style.transform = 'scale(1)';
                                this.style.cursor = 'zoom-in';
                                this.style.position = 'relative';
                                this.style.zIndex = '1';
                            } else {
                                this.style.transform = 'scale(2)';
                                this.style.cursor = 'zoom-out';
                                this.style.position = 'relative';
                                this.style.zIndex = '1000';
                            }
                        };
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('markdownContent').innerHTML = 
                        '<div class="error">加载Markdown文件失败</div>';
                });
        }
        
        // 为数学公式添加样式类
        function addMathStyles() {
            // 为行内数学公式添加样式
            const inlineMath = document.querySelectorAll('mjx-container[jax="CHTML"]:not([display="true"])');
            inlineMath.forEach(el => {
                if (!el.classList.contains('math-inline')) {
                    el.classList.add('math-inline');
                }
            });
            
            // 为块级数学公式添加样式
            const displayMath = document.querySelectorAll('mjx-container[jax="CHTML"][display="true"]');
            displayMath.forEach(el => {
                if (!el.parentElement.classList.contains('math-display')) {
                    const wrapper = document.createElement('div');
                    wrapper.classList.add('math-display');
                    el.parentNode.insertBefore(wrapper, el);
                    wrapper.appendChild(el);
                }
            });
        }
        
        // 键盘快捷键支持
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
                e.preventDefault();
                toggleSidebar();
            }
        });
    </script>
</body>
</html>
'''

