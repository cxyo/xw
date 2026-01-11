# Docker容器部署指南

## 1. 安装Docker和Docker Compose

### 1.1 安装Docker

在Ubuntu终端执行以下命令安装Docker：

```bash
# 更新系统软件包
sudo apt update

# 安装依赖包
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 添加Docker GPG密钥
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 设置Docker仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 再次更新系统软件包
sudo apt update

# 安装Docker Engine, Docker CLI, Docker Compose
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 验证Docker安装是否成功
sudo docker run hello-world
```

### 1.2 安装Docker Compose（如果未安装）

```bash
# 下载Docker Compose二进制文件
curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

# 设置执行权限
sudo chmod +x /usr/local/bin/docker-compose

# 验证Docker Compose安装是否成功
docker-compose --version
```

### 1.3 将用户添加到docker组（可选，避免每次使用sudo）

```bash
sudo usermod -aG docker $USER
```

**注意：** 执行完此命令后需要重新登录或重启系统才能生效。

## 2. 准备项目文件

### 2.1 克隆或传输项目文件

使用之前提到的方法（SCP或WinSCP）将项目文件传输到Ubuntu系统，例如：

```bash
scp -r d:\AI_CODE_project\DEMO\xw-main ubuntu@192.168.1.100:~/xw-main
```

### 2.2 进入项目目录

```bash
cd ~/xw-main
```

## 3. 构建Docker镜像

### 3.1 使用Docker Compose构建镜像

```bash
docker-compose build
```

### 3.2 或使用Docker命令直接构建

```bash
docker build -t finance-news-generator .
```

## 4. 运行Docker容器

### 4.1 使用Docker Compose运行

```bash
# 以后台模式运行
docker-compose up -d

# 查看容器状态
docker-compose ps

# 查看容器日志
docker-compose logs
```

### 4.2 或使用Docker命令直接运行

```bash
# 创建output目录（如果不存在）
mkdir -p output

# 运行容器
docker run -d \
  --name finance-news-generator \
  --restart unless-stopped \
  -v $(pwd)/output:/app/output \
  finance-news-generator

# 查看容器状态
docker ps

# 查看容器日志
docker logs finance-news-generator
```

## 5. 验证容器运行

### 5.1 检查生成的HTML文件

```bash
ls -la output/
```

如果容器运行成功，应该会看到`index.html`文件。

### 5.2 手动运行一次更新

```bash
# 使用Docker Compose运行一次更新
docker-compose run finance-news

# 或使用Docker命令直接运行
docker run --rm \
  -v $(pwd)/output:/app/output \
  finance-news-generator
```

## 6. 创建系统服务（可选）

### 6.1 创建systemd服务文件

```bash
sudo nano /etc/systemd/system/finance-news.service
```

### 6.2 编写服务文件内容

```ini
[Unit]
Description=Finance News Generator Docker Container
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/用户名/xw-main
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
Restart=no

[Install]
WantedBy=multi-user.target
```

**注意：** 将`用户名`替换为你的Ubuntu用户名。

### 6.3 启用并启动服务

```bash
# 重载systemd配置
sudo systemctl daemon-reload

# 启用服务（开机自启）
sudo systemctl enable finance-news.service

# 启动服务
sudo systemctl start finance-news.service

# 查看服务状态
sudo systemctl status finance-news.service
```

## 7. 将Docker容器添加到系统dock

### 7.1 创建桌面快捷方式

```bash
nano ~/Desktop/finance-news-docker.desktop
```

### 7.2 编写快捷方式内容

```
[Desktop Entry]
Name=财经新闻生成工具（Docker）
Comment=使用Docker运行的财经新闻自动爬取生成工具
Exec=bash -c "cd /home/用户名/xw-main && docker-compose run finance-news"
Icon=docker
Terminal=true
Type=Application
Categories=Utility;Application;
```

**注意：** 
- 将`用户名`替换为你的Ubuntu用户名
- 如果需要自定义图标，可以将`Icon`字段替换为其他图标路径

### 7.3 设置文件权限

```bash
chmod +x ~/Desktop/finance-news-docker.desktop
```

### 7.4 添加到dock

1. 在桌面上找到刚创建的"财经新闻生成工具（Docker）"快捷方式
2. 右键点击快捷方式，选择"Allow Launching"（允许启动）
3. 将快捷方式拖拽到左侧dock栏中

## 8. 配置定时运行

### 8.1 使用cron定时运行容器

```bash
# 编辑crontab
crontab -e
```

添加以下内容（每天20:00运行）：

```
0 20 * * * cd /home/用户名/xw-main && docker-compose run --rm finance-news
```

**注意：** 将`用户名`替换为你的Ubuntu用户名。

### 8.2 查看cron任务

```bash
crontab -l
```

## 9. 管理Docker容器

### 9.1 查看容器状态

```bash
# 使用Docker Compose
docker-compose ps

# 或使用Docker命令
docker ps
```

### 9.2 查看容器日志

```bash
# 使用Docker Compose
docker-compose logs

# 或使用Docker命令
docker logs finance-news-generator
```

### 9.3 停止容器

```bash
# 使用Docker Compose
docker-compose down

# 或使用Docker命令
docker stop finance-news-generator
docker rm finance-news-generator
```

### 9.4 重启容器

```bash
# 使用Docker Compose
docker-compose restart

# 或使用Docker命令
docker restart finance-news-generator
```

### 9.5 更新容器

当项目代码更新后，需要重新构建和运行容器：

```bash
# 使用Docker Compose
docker-compose down
docker-compose build
docker-compose up -d

# 或使用Docker命令
docker stop finance-news-generator
docker rm finance-news-generator
docker build -t finance-news-generator .
docker run -d \
  --name finance-news-generator \
  --restart unless-stopped \
  -v $(pwd)/output:/app/output \
  finance-news-generator
```

## 10. 常见问题及解决方案

### 10.1 Docker容器无法启动

- 检查容器日志：`docker-compose logs` 或 `docker logs finance-news-generator`
- 确保output目录存在且有正确的权限：`mkdir -p output && chmod 755 output`

### 10.2 生成的HTML文件为空或不完整

- 检查容器日志，查看是否有爬取错误
- 确保网络连接正常
- 检查新闻网站是否有反爬机制

### 10.3 快捷方式无法启动

- 检查快捷方式中的路径是否正确
- 确保docker-compose命令可以在终端中正常运行
- 检查文件权限：`chmod +x ~/Desktop/finance-news-docker.desktop`

## 11. 卸载Docker和项目

### 11.1 停止并删除容器

```bash
# 使用Docker Compose
docker-compose down

# 或使用Docker命令
docker stop finance-news-generator
docker rm finance-news-generator
```

### 11.2 删除Docker镜像

```bash
# 删除项目镜像
docker rmi finance-news-generator

# 删除所有未使用的镜像
docker image prune -a
```

### 11.3 删除项目文件

```bash
rm -rf ~/xw-main
rm ~/Desktop/finance-news-docker.desktop
```

### 11.4 卸载Docker（可选）

```bash
sudo apt purge -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

---

## 联系方式

如有问题或建议，欢迎联系项目维护者。
