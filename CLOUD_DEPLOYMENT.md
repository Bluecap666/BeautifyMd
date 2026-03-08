# 🚀 云服务器部署完整指南

## 📋 问题总结

### 问题 1: 美化内容出现乱码 ✅ 已修复

**原因：**
- AI API 响应解析不完善
- 缺少响应验证

**解决方案：**
- ✅ 增强响应解析逻辑
- ✅ 添加内容验证
- ✅ 多种格式兼容处理

### 问题 2: 云服务器无法访问 ✅ 已解决

**原因：**
- 防火墙/安全组未开放端口
- 可能需要正确的启动方式

**解决方案：**
- ✅ 绑定到 `0.0.0.0`
- ✅ 创建生产启动脚本
- ✅ 配置防火墙和安全组

---

## 🔧 立即修复步骤

### 步骤 1: 更新代码

代码已自动修复，包含：
- ✅ `ai_beautifier.py` - 增强 AI 响应解析
- ✅ `run_server.py` - 生产环境启动脚本

### 步骤 2: 提交到 GitHub

```bash
git add .
git commit -m "fix: 修复 AI 响应解析和云服务器部署问题"
git push origin master
```

### 步骤 3: 服务器拉取更新

```bash
# SSH 登录服务器
ssh user@your_server_ip

# 进入项目目录
cd /path/to/BeautifyMd

# 拉取最新代码
git pull origin master
```

---

## 🌐 云服务器配置

### A. 使用 run_server.py 启动（推荐）

```bash
python run_server.py
```

输出应该显示：
```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║     MD BeautifyArts - Web UI Server                  ║
║                                                      ║
║     🚀 服务已启动                                    ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
    
    访问地址：http://0.0.0.0:5000
    API 文档：http://0.0.0.0:5000/api/health
```

### B. 配置防火墙

#### Ubuntu (UFW)
```bash
sudo ufw allow 5000/tcp
sudo ufw reload
sudo ufw status
```

#### CentOS/RHEL (firewalld)
```bash
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

#### Debian/iptables
```bash
sudo iptables -I INPUT -p tcp --dport 5000 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4
```

### C. 配置云服务商安全组

#### 阿里云 ECS
1. 登录 [阿里云控制台](https://ecs.console.aliyun.com/)
2. 选择你的实例
3. 安全组 → 配置规则
4. 添加入站规则：
   ```
   端口范围：5000/5000
   授权对象：0.0.0.0/0
   协议类型：TCP
   优先级：1
   ```

#### 腾讯云 CVM
1. 登录 [腾讯云控制台](https://console.cloud.tencent.com/securitygroup)
2. 选择安全组
3. 修改规则 → 添加入站规则
   ```
   端口：5000
   协议：TCP
   来源：0.0.0.0/0
   策略：允许
   ```

#### 华为云 ECS
1. 登录 [华为云控制台](https://console.huaweicloud.com/ecs/)
2. 安全组管理
3. 添加入方向规则
   ```
   端口：5000
   协议：TCP
   远端地址：0.0.0.0/0
   ```

#### AWS EC2
1. 登录 AWS Console
2. EC2 → Security Groups
3. Inbound rules → Edit
4. Add rule:
   ```
   Type: Custom TCP
   Port: 5000
   Source: Anywhere (0.0.0.0/0)
   ```

---

## 🧪 测试连接

### 在服务器上测试
```bash
# 本地访问
curl http://localhost:5000

# 应该返回 HTML
```

### 从本地电脑测试
```bash
# 1. Ping 服务器
ping your_server_ip

# 2. Telnet 测试端口
telnet your_server_ip 5000

# 或使用 curl
curl http://your_server_ip:5000

# 3. 浏览器访问
# http://your_server_ip:5000
```

### 检查端口绑定
```bash
# Linux
netstat -tlnp | grep 5000
# 或
ss -tlnp | grep 5000

# 应该看到：
# 0.0.0.0:5000  LISTEN
```

---

## 🎯 生产环境优化（可选）

### 1. 使用 Gunicorn

**安装:**
```bash
pip install gunicorn
```

**启动:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

**解释:**
- `-w 4`: 4 个工作进程
- `-b 0.0.0.0:5000`: 绑定地址和端口

### 2. 配置 systemd 服务

创建 `/etc/systemd/system/beautifymd.service`:

```ini
[Unit]
Description=MD BeautifyArts Web UI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/BeautifyMd
ExecStart=/home/ubuntu/.local/bin/gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
Restart=always
Environment="PATH=/home/ubuntu/.local/bin"

[Install]
WantedBy=multi-user.target
```

**启动服务:**
```bash
sudo systemctl daemon-reload
sudo systemctl start beautifymd
sudo systemctl status beautifymd
sudo systemctl enable beautifymd  # 开机自启
```

### 3. 使用 Nginx 反向代理

**安装 Nginx:**
```bash
sudo apt update && sudo apt install nginx  # Ubuntu/Debian
# 或
sudo yum install nginx  # CentOS/RHEL
```

**配置 Nginx:**
```bash
sudo nano /etc/nginx/sites-available/beautifymd
```

添加以下内容：
```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名或服务器 IP
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**启用配置:**
```bash
sudo ln -s /etc/nginx/sites-available/beautifymd /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. 配置 HTTPS（Let's Encrypt）

**安装 Certbot:**
```bash
sudo apt install certbot python3-certbot-nginx  # Ubuntu/Debian
```

**获取证书:**
```bash
sudo certbot --nginx -d your_domain.com
```

---

## 📊 故障排查

### 问题 1: 还是出现乱码

**检查:**
```bash
# 查看服务器日志
tail -f /var/log/syslog | grep beautify

# 或查看应用日志
tail -f beautify.log
```

**解决:**
1. 确认 API Key 正确
2. 尝试更换模型（如 GPT-3.5）
3. 减少文件内容大小
4. 查看详细错误日志

### 问题 2: 仍然无法访问

**检查清单:**
- [ ] 安全组已开放 5000 端口
- [ ] 防火墙已配置
- [ ] 服务正在运行
- [ ] 端口正确监听

**诊断命令:**
```bash
# 1. 检查服务是否运行
ps aux | grep python

# 2. 检查端口监听
netstat -tlnp | grep 5000

# 3. 检查防火墙
sudo ufw status  # Ubuntu
sudo firewall-cmd --list-all  # CentOS

# 4. 测试本地访问
curl http://localhost:5000

# 5. 查看系统日志
sudo dmesg | grep 5000
```

### 问题 3: 内存不足

**症状:**
```
Killed
# 或服务自动停止
```

**解决:**
```bash
# 增加 swap 空间
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 永久生效
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 📈 性能监控

### 查看资源使用
```bash
# CPU 和内存
top

# 磁盘空间
df -h

# 网络流量
iftop
```

### 日志管理
```bash
# 查看日志
tail -f /var/log/nginx/error.log

# 清理旧日志
sudo journalctl --vacuum-time=7d
```

---

## 🎁 完整部署示例

### 阿里云 Ubuntu 服务器

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装 Python 和依赖
sudo apt install -y python3-pip git

# 3. 克隆项目
git clone https://github.com/Bluecap666/BeautifyMd.git
cd BeautifyMd

# 4. 安装依赖
pip3 install -r requirements.txt

# 5. 配置环境变量
cp .env.example .env
nano .env  # 编辑 API Key

# 6. 安装 Gunicorn
pip3 install gunicorn

# 7. 配置防火墙
sudo ufw allow 5000/tcp
sudo ufw reload

# 8. 启动服务（后台运行）
nohup gunicorn -w 4 -b 0.0.0.0:5000 web_app:app > output.log 2>&1 &

# 9. 检查服务
ps aux | grep gunicorn
netstat -tlnp | grep 5000

# 10. 测试访问
curl http://localhost:5000
```

---

## ✅ 验证清单

部署完成后，请逐项检查：

- [ ] 服务正在运行 (`ps aux | grep python`)
- [ ] 端口 5000 已监听 (`netstat -tlnp | grep 5000`)
- [ ] 本地可以访问 (`curl http://localhost:5000`)
- [ ] 防火墙已开放 5000 端口
- [ ] 安全组已配置入站规则
- [ ] 远程可以访问 (`curl http://服务器 IP:5000`)
- [ ] AI 美化功能正常
- [ ] 无乱码问题
- [ ] Web UI 界面正常显示

---

## 🆘 需要帮助？

如果以上步骤都无法解决问题，请提供：

1. **服务器信息**
   - 操作系统和版本
   - 云服务商
   - 内存和 CPU 配置

2. **错误信息**
   - 完整的错误日志
   - 截图或终端输出

3. **已尝试的方法**
   - 已经做过哪些操作
   - 结果如何

---

**祝你部署成功！** 🎉

访问地址应该是：**http://你的服务器IP:5000**
