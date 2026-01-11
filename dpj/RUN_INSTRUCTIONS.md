# 运行说明

## 错误原因

当你在Windows/Mac/Linux的标准Python环境中运行代码时，会遇到以下错误：

```
ModuleNotFoundError: No module named 'network'
```

这是因为代码中使用了`network`、`machine`、`urequests`等**MicroPython特有的模块**，这些模块只能在MicroPython环境中运行，而不能在标准Python环境中运行。

## 正确运行方法

### 方法一：上传到ESP32开发板运行（推荐）

这是代码的**设计运行环境**，需要以下步骤：

1. **准备硬件**：
   - ESP32开发板
   - 2个LED灯（红、绿）
   - 2个220Ω电阻
   - 杜邦线若干

2. **烧录MicroPython固件**：
   - 下载ESP32的MicroPython固件：[https://micropython.org/download/esp32/](https://micropython.org/download/esp32/)
   - 使用Thonny IDE或ESP-IDF烧录固件到ESP32

3. **上传代码**：
   - 打开Thonny IDE，连接ESP32开发板
   - 将`main.py`文件上传到ESP32的根目录

4. **运行代码**：
   - 在Thonny IDE中点击运行按钮，或重启ESP32开发板
   - 代码会自动运行

### 方法二：使用MicroPython模拟器（测试用）

如果你没有ESP32开发板，可以使用MicroPython模拟器进行测试：

1. **推荐模拟器**：
   - [Wokwi ESP32 Simulator](https://wokwi.com/esp32)
   - [MicroPython Online Simulator](https://micropython.org/unicorn/)

2. **使用步骤**：
   - 在模拟器中创建ESP32项目
   - 复制`main.py`的代码到模拟器
   - 运行代码查看效果

## 注意事项

1. **不要在标准Python环境中运行**：代码使用的是MicroPython特有的模块，无法在Windows/Mac/Linux的标准Python环境中运行。

2. **必须使用MicroPython环境**：
   - 实际ESP32开发板 + MicroPython固件
   - 或MicroPython模拟器

3. **硬件连接**：
   - 绿色LED连接到GPIO23引脚
   - 红色LED连接到GPIO22引脚
   - 每个LED串联220Ω电阻到GND

4. **首次配置**：
   - 运行代码后，ESP32会创建名为`IndexMonitor`的WiFi热点
   - 连接该热点，密码：`12345678`
   - 在浏览器中输入`192.168.4.1`进行配置

## 调试方法

1. **使用Thonny IDE的串口监视器**：
   - 连接ESP32开发板
   - 打开Thonny IDE的串口监视器
   - 可以查看代码运行的输出信息和错误信息

2. **检查网络连接**：
   - 确保ESP32已连接到WiFi
   - 可以通过路由器管理页面查看ESP32的IP地址

3. **检查硬件连接**：
   - 确保LED和电阻连接正确
   - 确保GPIO引脚连接正确

## 常见错误及解决方法

### 错误1：ModuleNotFoundError: No module named 'network'
- **原因**：在标准Python环境中运行MicroPython代码
- **解决方法**：使用ESP32开发板+MicroPython固件，或MicroPython模拟器

### 错误2：无法连接到IndexMonitor热点
- **原因**：ESP32可能已连接到其他WiFi，或代码运行异常
- **解决方法**：重启ESP32开发板，或长按Reset按钮

### 错误3：配置页面无法打开
- **原因**：设备未连接到正确的WiFi网络
- **解决方法**：
  - 首次配置：连接`IndexMonitor`热点
  - 已配置：连接到ESP32所在的WiFi网络

### 错误4：LED灯不亮
- **原因**：硬件连接错误，或指数涨跌未达到阈值
- **解决方法**：
  - 检查硬件连接
  - 在串口监视器查看指数数据和LED控制信息

## 联系信息

如果遇到其他问题，可以查看README.md文件，或参考MicroPython官方文档：[https://docs.micropython.org/en/latest/](https://docs.micropython.org/en/latest/)
