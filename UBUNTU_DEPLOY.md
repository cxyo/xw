# Ubuntu系统部署指南

## 1. 连接到Ubuntu系统

### 1.1 启用Ubuntu SSH服务

在Ubuntu系统上执行以下步骤：

1. 打开终端（快捷键：`Ctrl + Alt + T`）
2. 安装SSH服务器：
   ```bash
   sudo apt update
   sudo apt install openssh-server -y
   ```
3. 验证SSH服务是否运行：
   ```bash
   sudo systemctl status ssh
   ```
4. 设置SSH服务开机自启：
   ```bash
   sudo systemctl enable ssh
   ```

### 1.2 获取Ubuntu IP地址

在Ubuntu终端执行：
```bash
ip addr show
```

查找类似于 `inet 192.168.x.x/24` 的行，这就是你的Ubuntu IP地址。

### 1.3 远程连接Ubuntu

#### Windows系统连接方式

1. 打开PowerShell或命令提示符
2. 使用SSH命令连接：
   ```bash
   ssh 用户名@UbuntuIP地址
   ```
   例如：`ssh ubuntu@192.168.1.100`
3. 首次连接会提示确认指纹，输入 `yes` 并按回车
4. 输入Ubuntu用户密码，即可成功连接

#### 使用PuTTY连接（可选）

1. 下载并安装PuTTY：https://www.putty.org/
2. 打开PuTTY，在"Host Name (or IP address)"字段输入Ubuntu IP地址
3. 端口保持默认的22，连接类型选择SSH
4. 点击"Open"，然后按照提示输入用户名和密码

## 2. 传输项目文件到Ubuntu

### 2.1 使用SCP命令传输

在Windows PowerShell或命令提示符中执行：

```bash
scp -r d:\AI_CODE_project\DEMO\xw-main 用户名@UbuntuIP地址:~/xw-main
```

例如：
```bash
scp -r d:\AI_CODE_project\DEMO\xw-main ubuntu@192.168.1.100:~/xw-main
```

### 2.2 使用WinSCP传输（图形界面）

1. 下载并安装WinSCP：https://winscp.net/
2. 打开WinSCP，输入以下信息：
   - 主机名：Ubuntu IP地址
   - 端口号：22
   - 用户名：Ubuntu用户名
   - 密码：Ubuntu用户密码
   - 文件协议：SFTP
3. 点击"登录"，然后将本地的xw-main文件夹拖拽到Ubuntu的主目录（~/）

## 3. 安装必要的依赖

### 3.1 更新系统软件包

在已连接的Ubuntu终端执行：

```bash
sudo apt update
```

### 3.2 安装Python 3和pip

```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 3.3 安装项目依赖

1. 进入项目目录：
   ```bash
   cd ~/xw-main
   ```
2. 安装项目依赖：
   ```bash
   pip3 install -r requirements.txt
   ```

## 4. 运行项目测试

```bash
python3 app.py
```

如果运行成功，会生成`index.html`文件。

## 5. 创建桌面快捷方式

### 5.1 创建.desktop文件

在Ubuntu终端执行：

```bash
nano ~/Desktop/xw-main.desktop
```

### 5.2 编写快捷方式内容

在打开的编辑器中输入以下内容（根据实际情况修改路径）：

```
[Desktop Entry]
Name=财经新闻生成工具
Comment=自动爬取财经新闻并生成HTML文件
Exec=python3 /home/用户名/xw-main/app.py
Icon=text-html
Terminal=true
Type=Application
Categories=Utility;Application;
```

注意：
- 将`用户名`替换为你的Ubuntu用户名
- 如果需要自定义图标，可以将`Icon`字段替换为其他图标路径

### 5.3 设置文件权限

保存并退出编辑器（按`Ctrl + X`，然后按`Y`，最后按`Enter`），然后执行：

```bash
chmod +x ~/Desktop/xw-main.desktop
```

## 6. 将快捷方式添加到dock

### 6.1 使用图形界面添加

1. 在桌面上找到刚创建的"财经新闻生成工具"快捷方式
2. 右键点击快捷方式，选择"Allow Launching"（允许启动）
3. 将快捷方式拖拽到左侧dock栏中

### 6.2 使用命令行添加（可选）

```bash
mkdir -p ~/.local/share/applications/
cp ~/Desktop/xw-main.desktop ~/.local/share/applications/
```

然后打开应用程序菜单，找到"财经新闻生成工具"，右键点击并选择"Add to Favorites"（添加到收藏夹）

## 7. 配置自动运行（可选）

### 7.1 使用cron定时运行

1. 编辑crontab：
   ```bash
   crontab -e
   ```
2. 添加以下内容（每天20:00运行）：
   ```
   0 20 * * * python3 /home/用户名/xw-main/app.py
   ```
3. 保存并退出

### 7.2 查看cron任务

```bash
crontab -l
```

## 8. 常见问题及解决方案

### 8.1 SSH连接失败

- 确保Ubuntu和本地电脑在同一网络
- 检查Ubuntu IP地址是否正确
- 确保SSH服务已启动
- 检查防火墙设置：
  ```bash
  sudo ufw status
  ```
  如果防火墙开启，允许SSH端口：
  ```bash
  sudo ufw allow ssh
  ```

### 8.2 依赖安装失败

- 确保pip3已正确安装
- 尝试更新pip3：
  ```bash
  pip3 install --upgrade pip
  ```

### 8.3 快捷方式无法启动

- 检查.desktop文件中的路径是否正确
- 确保app.py有执行权限：
  ```bash
  chmod +x /home/用户名/xw-main/app.py
  ```

## 9. 卸载项目（可选）

```bash
# 删除项目文件夹
rm -rf ~/xw-main
# 删除桌面快捷方式
rm ~/Desktop/xw-main.desktop
# 删除应用程序菜单快捷方式
rm ~/.local/share/applications/xw-main.desktop
```

---

## 联系方式

如有问题或建议，欢迎联系项目维护者。
