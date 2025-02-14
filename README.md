# Cursor Reset Plus
直接下载Releases里的cursor2.0压缩包，安装好以来，通过命令运行即可启动程序，由于是测试软件，很多代码会报错，有大佬可以拿去重写代码，就介绍到这里
一个用于重置 Cursor IDE 设备标识的跨平台图形化工具。

## ⚠️ 免责声明

本项目仅供学习和研究使用，旨在研究 Cursor IDE 的设备标识机制。**强烈建议您购买 [Cursor](https://cursor.sh/) 的正版授权**以支持开发者。

使用本工具可能违反 Cursor 的使用条款。作者不对使用本工具导致的任何问题负责，包括但不限于：

- 软件授权失效
- 账号封禁
- 其他未知风险

如果您认可 Cursor 的价值，请支持正版，为软件开发者的工作付费。

## 🚀 功能特点

- 🖥️ 跨平台支持：Windows、macOS 和 Linux
- 🔄 自动备份和恢复功能
- 📊 实时状态显示和进度反馈
- 🎨 多主题支持
- 💾 完整的备份管理
- 📝 详细的日志记录

## 🛠️ 系统要求

### Windows
- Windows 10 或更高版本
- 管理员权限
- 2GB 以上可用内存
- 100MB 以上可用磁盘空间

### macOS
- macOS 10.13 或更高版本
- 管理员权限
- 2GB 以上可用内存
- 100MB 以上可用磁盘空间

### Linux
- 现代 Linux 发行版
- 管理员权限
- 2GB 以上可用内存
- 100MB 以上可用磁盘空间
- AppImage 支持

## 📥 安装方法

### 方法一：直接使用
1. 从 [Releases]([https://github.com/your-username/cursor-reset-plus/releases](https://github.com/pattonant/cursorPRO.git)) 页面下载最新版本
2. 解压下载的文件
3. 运行可执行文件（Windows 需要右键以管理员身份运行）

### 方法二：从源码安装
1. 克隆仓库：
```bash
git clone https://github.com/your-username/cursor-reset-plus.git
cd cursor-reset-plus
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python cursor_reset_plus.py
```

## 🎯 使用方法

1. 在使用前请确保：
   - 已完全关闭 Cursor IDE
   - 已备份重要数据
   - Windows 用户已以管理员权限运行

2. 运行程序后：
   - 选择您的操作系统
   - 点击"重置 Cursor"按钮
   - 按照界面提示完成操作

3. 重置完成后：
   - 检查备份文件是否正确保存
   - 使用新账号登录 Cursor
   - 不要使用之前的账号

## 🔧 功能说明

### Windows 系统
- 重置 MachineGuid
- 更新 storage.json 配置
- 自动备份原始标识

### macOS 系统
- 备份 Hardware UUID
- 更新 storage.json 配置
- 保护系统完整性

### Linux 系统
- 修改 AppImage 文件
- 更新 storage.json 配置
- 自动备份原始文件

## 📋 备份管理

- 自动备份所有修改的文件
- 支持查看和恢复历史备份
- 提供备份文件清理功能
- 备份存储在用户目录下的 CursorResetPlus 文件夹中

## ⚠️ 注意事项

1. 重置前注意事项：
   - 完全关闭 Cursor IDE
   - 备份重要数据
   - 确保有足够的磁盘空间

2. 安全建议：
   - 定期备份重要数据
   - 不要随意删除备份文件
   - 保持系统安全更新

3. 使用限制：
   - 不要频繁重置
   - 遵守软件使用条款
   - 注意账号安全

## 🤝 贡献指南

欢迎提交 Pull Request 或创建 Issue！在贡献代码前，请确保：

1. 代码符合项目规范
2. 添加必要的注释和文档
3. 通过所有测试
4. 遵守开源协议

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🔗 相关链接

- [Cursor 官网](https://cursor.sh/)
- [问题反馈](https://github.com/your-username/cursor-reset-plus/issues)
- [更新日志](CHANGELOG.md)

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至：your-email@example.com

## 🙏 鸣谢

感谢所有为本项目做出贡献的开发者！

---

**再次提醒：本工具仅供学习研究使用，请支持正版软件！**

[English Version](#usage)

这是一个用于重置 Cursor IDE 设备标识的 PowerShell 脚本。该脚本支持 Cursor 0.45.x 版本（已在 0.45.8 版本上测试通过）。

## ⚠️ 免责声明

本项目仅供学习和研究使用，旨在研究 Cursor IDE 的设备标识机制。**强烈建议您购买 [Cursor](https://cursor.sh/) 的正版授权**以支持开发者。

使用本脚本可能违反 Cursor 的使用条款。作者不对使用本脚本导致的任何问题负责，包括但不限于：

- 软件授权失效
- 账号封禁
- 其他未知风险

如果您认可 Cursor 的价值，请支持正版，为软件开发者的工作付费。

## 使用方法

⚠️ 为避免新账号立即失效，请严格按照以下步骤操作：

### Windows

1. 在 Cursor IDE 中退出当前登录的账号
2. 完全关闭 Cursor IDE
3. 以管理员身份打开命令提示符或 PowerShell
4. 复制粘贴执行以下命令：

   ```batch
   powershell -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iwr -Uri 'https://raw.githubusercontent.com/hamflx/cursor-reset/main/reset.ps1' -UseBasicParsing | iex"
   ```

5. 重置完成后打开 Cursor IDE，使用新的账号登录（不要使用之前的账号）

如果脚本卡在"正在等待 Cursor 进程退出..."，可以在管理员权限的命令行中执行以下命令强制结束所有 Cursor 进程：

```powershell
taskkill /f /im cursor.exe
```

### macOS

1. 在 Cursor IDE 中退出当前登录的账号
2. 完全关闭 Cursor IDE
3. 打开终端，执行以下命令：

   ```bash
   curl -fsSL https://raw.githubusercontent.com/hamflx/cursor-reset/main/reset.sh | bash
   ```

4. 启动 Cursor 并使用新账号登录（不要使用之前的账号）

如果需要恢复到原始状态，可以使用以下命令：

```bash
curl -fsSL https://raw.githubusercontent.com/hamflx/cursor-reset/main/reset.sh | bash -s -- --restore
```

如果脚本卡在"正在等待 Cursor 进程退出..."，可以在终端中执行以下命令强制结束 Cursor 进程：

```bash
pkill -9 Cursor
```

### Linux

1. 在 Cursor IDE 中退出当前登录的账号
2. 完全关闭 Cursor IDE
3. 打开终端，执行以下命令：

   ```bash
   curl -fsSL https://raw.githubusercontent.com/hamflx/cursor-reset/main/linux/bash.sh | bash -s -- --appimage /path/to/cursor.AppImage
   ```

   将 `/path/to/cursor.AppImage` 替换为你的 Cursor AppImage 文件路径。

4. 启动 Cursor 并使用新账号登录（不要使用之前的账号）

如果脚本卡在"正在等待 Cursor 进程退出..."，可以在终端中执行以下命令强制结束 Cursor 进程：

```bash
pkill -9 Cursor
```

## ⚠️ 重要注意事项

### Windows

脚本会修改系统注册表中的 `HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid`，这个值可能被其他软件用作设备标识，如果你购买了 Cursor 的正版授权或其他使用此注册表项作为设备标识的正版软件，修改后可能会导致这些软件的授权失效。

原始的 MachineGuid 会被自动备份到 `%USERPROFILE%\MachineGuid_Backups` 目录下，如果需要恢复原始 MachineGuid，可以从备份目录中找到对应的备份文件，然后通过注册表编辑器恢复该值。

## 系统要求

### Windows

- Windows 操作系统
- PowerShell
- 管理员权限
- Cursor IDE 0.45.x 版本（已在 0.45.8 版本测试通过）

### macOS

- macOS 10.13 或更高版本
- Cursor IDE 0.45.x 版本

### Linux

- Linux 操作系统
- Python 3
- Cursor IDE 0.45.x 版本（仅支持 AppImage 安装方式）
- appimagetool（用于重新打包 AppImage）
- 安装路径必须为 `/opt/cursor-bin/cursor-bin.AppImage`

---

This is a PowerShell script for resetting Cursor IDE device identifiers. The script supports Cursor 0.45.x.

## ⚠️ Disclaimer

This project is for educational and research purposes only, aimed at studying the device identification mechanism of Cursor IDE. **It is strongly recommended to purchase a [Cursor](https://cursor.sh/) license** to support the developers.

Using this script may violate Cursor's terms of service. The author assumes no responsibility for any issues arising from the use of this script, including but not limited to:

- Software license invalidation
- Account suspension
- Other unknown risks

If you value Cursor, please support the official version and pay for the developers' work.

## Usage

⚠️ To prevent the new account from being immediately invalidated, please follow these steps strictly:

### Windows

1. Sign out of your current account in Cursor IDE
2. Completely close Cursor IDE
3. Open Command Prompt or PowerShell as Administrator
4. Copy and paste the following command:

   ```batch
   powershell -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iwr -Uri 'https://raw.githubusercontent.com/hamflx/cursor-reset/main/reset.ps1' -UseBasicParsing | iex"
   ```

5. After reset is complete, open Cursor IDE and sign in with a new account (do not use the previous account)

If the script is stuck at "Waiting for Cursor process to exit...", you can force kill Cursor processes by running the following command in the terminal:

```powershell
taskkill /f /im cursor.exe
```

### macOS

1. Sign out of your current account in Cursor IDE
2. Completely close Cursor IDE
3. Open terminal and execute the following command:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/hamflx/cursor-reset/main/reset.sh | bash
   ```

4. Start Cursor and sign in with a new account (do not use the previous account)

To restore to the original state, you can use the following command:

```bash
curl -fsSL https://raw.githubusercontent.com/hamflx/cursor-reset/main/reset.sh | bash -s -- --restore
```

If the script is stuck at "Cursor is running", you can force kill Cursor processes by running the following command in the terminal:

```bash
pkill -9 Cursor
```

### Linux

1. Sign out of your current account in Cursor IDE
2. Completely close Cursor IDE
3. Open terminal and execute the following command:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/hamflx/cursor-reset/main/linux/bash.sh | bash -s -- --appimage /path/to/cursor.AppImage
   ```

   Replace `/path/to/cursor.AppImage` with the path to your Cursor AppImage file.

4. Start Cursor and sign in with a new account (do not use the previous account)

If the script is stuck at "Waiting for Cursor process to exit...", you can force kill Cursor processes by running the following command in the terminal:

```bash
pkill -9 Cursor
```

## ⚠️ Important Notes

### Windows

The script modifies the system registry key `HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid`, which may be used by other software as a device identifier. If you have purchased a license for Cursor or other software that uses this registry key for device identification, modifying it may invalidate these software licenses.

The original MachineGuid will be automatically backed up to the `%USERPROFILE%\MachineGuid_Backups` directory. If you need to restore the original MachineGuid, you can find the corresponding backup file in this directory and restore it using the registry editor.

## System Requirements

### Windows

- Windows OS
- PowerShell
- Administrator privileges
- Cursor IDE 0.45.x (tested on version 0.45.8)

### macOS

- macOS 10.13 or higher
- Cursor IDE 0.45.x

### Linux

- Linux operating system
- Cursor IDE 0.45.x (AppImage format)
- appimagetool (will be automatically downloaded if not present)
