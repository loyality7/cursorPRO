import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import sys
import json
import uuid
import random
import shutil
import time
import webbrowser
import threading
import psutil
from datetime import datetime
import platform
import logging
from pathlib import Path
import requests
from ttkthemes import ThemedStyle
import ctypes
from PIL import Image, ImageTk

def is_admin():
    """检查是否具有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员权限重新运行程序"""
    try:
        if sys.platform == 'win32':
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:])
            ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            if int(ret) > 32:
                return True
        return False
    except Exception as e:
        print(f"提升权限时出错: {str(e)}")
        return False

class CursorResetPlus:
    VERSION = "v2.0.0"  # 将版本号定义为类常量
    
    def __init__(self, root):
        self.root = root
        self.setup_logging()
        self.init_theme()
        
        # 设置窗口图标
        self.icon_path = "icon.ico"
        if os.path.exists(self.icon_path):
            self.root.iconbitmap(self.icon_path)
            
        self.init_ui()
        self.os_type = platform.system().lower()
        self.running_threads = []  # 添加线程管理列表
        
    def setup_logging(self):
        """设置日志系统"""
        log_dir = Path.home() / "CursorResetPlus" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"cursor_reset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def init_theme(self):
        """初始化主题"""
        try:
            # 尝试使用 ThemedStyle
            self.style = ThemedStyle(self.root)
            
            # 检查主题文件是否存在
            theme_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib", "ttkthemes", "themes")
            if not os.path.exists(theme_dir):
                raise FileNotFoundError(f"主题目录不存在: {theme_dir}")
            
            self.available_themes = self.style.get_themes()
            if not self.available_themes:
                raise ValueError("没有可用的主题")
            
            # 尝试设置默认主题，如果失败则尝试其他主题
            try:
                self.style.set_theme("arc")
            except Exception as e:
                self.logger.warning(f"无法设置 arc 主题: {str(e)}")
                # 尝试使用第一个可用的主题
                if self.available_themes:
                    self.style.set_theme(self.available_themes[0])
                else:
                    raise ValueError("无法设置任何主题")
                
        except Exception as e:
            self.logger.warning(f"无法加载自定义主题: {str(e)}")
            # 如果无法加载自定义主题，使用默认ttk主题
            self.style = ttk.Style(self.root)
            self.available_themes = ['default']
            self.style.theme_use('default')
            
            # 设置一些基本的样式
            self.style.configure('TButton', padding=6)
            self.style.configure('TFrame', background='#f5f6fa')
            self.style.configure('TLabel', background='#f5f6fa')
        
    def init_ui(self):
        """初始化用户界面"""
        self.root.title("Cursor Reset Plus")
        self.root.geometry("900x600")
        self.root.configure(bg='#f5f6fa')
        self.root.minsize(900, 600)
        
        # 配置字体
        self.title_font = ('Segoe UI', 24, 'bold')
        self.normal_font = ('Segoe UI', 10)
        self.button_font = ('Segoe UI', 12, 'bold')
        
        # 初始化变量
        self.os_var = tk.StringVar(value=platform.system())
        self.appimage_path_var = tk.StringVar()
        
        # 创建主容器
        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # 配置网格
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)
        
        self.create_header()
        self.create_menu()
        self.create_status_area()
        self.create_control_panel()
        
        # 设置主题色
        self.style.configure('Header.TLabel', font=self.title_font, background='#f5f6fa')
        self.style.configure('Status.TFrame', background='white')
        
        # 初始化状态信息
        self.update_status("欢迎使用 Cursor Reset Plus\n请选择操作系统并点击相应的重置按钮开始重置过程。")

    def create_header(self):
        """创建头部区域"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # 标题和版本
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky="w")
        
        title_label = ttk.Label(
            title_frame,
            text="Cursor Reset Plus",
            style='Header.TLabel'
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        version_label = ttk.Label(
            title_frame,
            text=f"v{self.VERSION.lstrip('v')}",
            font=('Segoe UI', 12),
            foreground='#666666'
        )
        version_label.grid(row=1, column=0, sticky="w")
        
        # 操作系统选择
        os_frame = ttk.Frame(header_frame)
        os_frame.grid(row=0, column=1, padx=(50, 0))
        
        ttk.Label(os_frame, text="选择操作系统：").grid(row=0, column=0)
        os_combo = ttk.Combobox(
            os_frame,
            textvariable=self.os_var,
            values=["Windows", "macOS", "Linux"],
            state="readonly"
        )
        os_combo.grid(row=0, column=1)
        os_combo.bind('<<ComboboxSelected>>', self.on_os_changed)
        
        # AppImage选择（Linux专用）
        self.appimage_label = ttk.Label(os_frame, text="AppImage路径：")
        self.appimage_entry = ttk.Entry(os_frame, textvariable=self.appimage_path_var)
        self.appimage_button = ttk.Button(os_frame, text="浏览", command=self.browse_appimage)
        
        # 根据当前操作系统更新UI
        self.update_appimage_widgets()

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导出日志", command=self.export_logs)
        file_menu.add_command(label="清理备份", command=self.clean_backups)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 操作菜单
        action_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="操作", menu=action_menu)
        action_menu.add_command(label="快速重置", command=self.quick_reset)
        action_menu.add_command(label="恢复备份", command=self.restore_backup)
        action_menu.add_separator()
        action_menu.add_command(label="自动检测系统", command=self.auto_detect_os)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="进程管理器", command=self.show_process_manager)
        tools_menu.add_command(label="备份管理器", command=self.show_backup_manager)
        tools_menu.add_command(label="系统信息", command=self.show_system_info)
        
        # 主题菜单
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="主题", menu=theme_menu)
        for theme in self.available_themes:
            theme_menu.add_radiobutton(
                label=theme,
                value=theme,
                variable=tk.StringVar(value=self.style.theme_use()),
                command=lambda t=theme: self.change_theme(t)
            )
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="查看文档", command=lambda: webbrowser.open("https://github.com/hamflx/cursor-reset"))
        help_menu.add_separator()
        help_menu.add_command(label="关于", command=self.show_about)

    def create_status_area(self):
        """创建状态显示区域"""
        status_frame = ttk.Frame(self.main_container, style='Status.TFrame', padding="20")
        status_frame.grid(row=2, column=0, sticky="nsew")
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_rowconfigure(1, weight=1)
        
        # 状态标题
        status_header = ttk.Label(
            status_frame,
            text="操作状态",
            font=('Segoe UI', 14, 'bold')
        )
        status_header.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # 状态文本框和滚动条
        self.status_text = tk.Text(
            status_frame,
            wrap=tk.WORD,
            font=self.normal_font,
            bg='#f8f9fa',
            relief='flat',
            padx=10,
            pady=10
        )
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # 禁用编辑
        self.status_text.config(state=tk.DISABLED)

    def create_control_panel(self):
        """创建控制面板"""
        control_frame = ttk.Frame(self.main_container)
        control_frame.grid(row=3, column=0, sticky="ew", pady=(20, 0))
        control_frame.grid_columnconfigure(1, weight=1)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            control_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        # 按钮
        self.reset_button = self.create_button(
            control_frame,
            "重置 Cursor",
            self.start_reset,
            'primary'
        )
        self.reset_button.grid(row=1, column=0, padx=5)
        
        self.restore_button = self.create_button(
            control_frame,
            "恢复备份",
            self.restore_backup,
            'secondary'
        )
        self.restore_button.grid(row=1, column=1, padx=5)
        
        self.quit_button = self.create_button(
            control_frame,
            "退出程序",
            self.root.quit,
            'danger'
        )
        self.quit_button.grid(row=1, column=2, padx=5)

    def create_button(self, parent, text, command, style):
        """创建自定义按钮"""
        colors = {
            'primary': ('#007bff', '#0056b3'),
            'secondary': ('#6c757d', '#545b62'),
            'danger': ('#dc3545', '#c82333')
        }
        
        btn = tk.Button(
            parent,
            text=text,
            font=self.button_font,
            command=command,
            bg=colors[style][0],
            fg='white',
            activebackground=colors[style][1],
            activeforeground='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        
        # 鼠标悬停效果
        btn.bind('<Enter>', lambda e: btn.configure(bg=colors[style][1]))
        btn.bind('<Leave>', lambda e: btn.configure(bg=colors[style][0]))
        
        return btn

    def update_status(self, message, level="info"):
        """更新状态信息"""
        try:
            self.status_text.config(state=tk.NORMAL)
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            # 根据消息级别设置颜色
            tag = f"message_{timestamp}"
            color = {
                "info": "#000000",    # 黑色
                "warning": "#FFA500",  # 橙色
                "error": "#FF0000",    # 红色
                "success": "#008000"   # 绿色
            }.get(level, "#000000")
            
            self.status_text.tag_configure(tag, foreground=color)
            self.status_text.insert(tk.END, f"{timestamp} - ", tag)
            self.status_text.insert(tk.END, f"{message}\n", tag)
            self.status_text.see(tk.END)
            self.status_text.config(state=tk.DISABLED)
            self.root.update()
            
            # 记录日志
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(message)
        except Exception as e:
            self.logger.error(f"更新状态时出错: {str(e)}")

    def update_progress(self, value):
        """更新进度条"""
        self.progress_var.set(value)
        self.root.update()

    def browse_appimage(self):
        """浏览选择AppImage文件"""
        filename = filedialog.askopenfilename(
            title="选择Cursor AppImage文件",
            filetypes=[("AppImage文件", "*.AppImage"), ("所有文件", "*.*")]
        )
        if filename:
            self.appimage_path_var.set(filename)

    def on_os_changed(self, event):
        """操作系统选择改变时的处理"""
        self.update_appimage_widgets()

    def update_appimage_widgets(self):
        """更新AppImage相关控件的显示状态"""
        if self.os_var.get() == "Linux":
            self.appimage_label.grid(row=0, column=2, padx=(20, 10))
            self.appimage_entry.grid(row=0, column=3, padx=(0, 10))
            self.appimage_button.grid(row=0, column=4)
        else:
            self.appimage_label.grid_remove()
            self.appimage_entry.grid_remove()
            self.appimage_button.grid_remove()

    def check_cursor_process(self):
        """检查Cursor是否在运行"""
        try:
            if self.os_type == "windows":
                output = subprocess.check_output("tasklist", text=True)
                return "cursor.exe" in output.lower()
            else:
                output = subprocess.check_output(["ps", "aux"], text=True)
                return "cursor" in output.lower()
        except Exception as e:
            self.logger.error(f"检查进程时出错: {str(e)}")
            return False

    def wait_for_cursor_exit(self):
        """等待Cursor进程退出"""
        while self.check_cursor_process():
            self.update_status("正在等待 Cursor 进程退出...", level="warning")
            time.sleep(1)
        self.update_status("Cursor 已关闭，继续执行...", level="success")

    def generate_mac_machine_id(self):
        """生成类似macMachineId的格式"""
        template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
        result = ""
        for char in template:
            if char in ['x', 'y']:
                r = random.randint(0, 15)
                v = r if char == 'x' else (r & 0x3 | 0x8)
                result += hex(v)[2:]
            else:
                result += char
        return result

    def generate_random_id(self):
        """生成64位随机ID"""
        return uuid.uuid4().hex + uuid.uuid4().hex

    def backup_file(self, file_path, backup_dir):
        """备份文件"""
        if not os.path.exists(file_path):
            return None
            
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{os.path.basename(file_path)}_{timestamp}")
        shutil.copy2(file_path, backup_path)
        return backup_path

    def windows_reset(self):
        """Windows系统重置"""
        try:
            import winreg
            self.update_status("开始Windows系统重置...", level="info")
            
            # 备份和更新MachineGuid
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_ALL_ACCESS)
            current_guid = winreg.QueryValueEx(key, "MachineGuid")[0]
            
            backup_dir = Path.home() / "CursorResetPlus" / "backups" / "MachineGuid"
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / f"MachineGuid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(backup_path, 'w') as f:
                f.write(current_guid)
            self.update_status(f"已备份MachineGuid到: {backup_path}", level="success")
            
            new_guid = str(uuid.uuid4())
            winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_guid)
            winreg.CloseKey(key)
            self.update_status(f"已更新MachineGuid: {new_guid}", level="success")
            
        except Exception as e:
            self.logger.error(f"Windows重置出错: {str(e)}")
            raise

    def macos_reset(self):
        """macOS系统重置"""
        try:
            self.update_status("开始macOS系统重置...", level="info")
            
            # 获取硬件UUID
            hw_uuid = subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode()
            current_uuid = None
            for line in hw_uuid.split('\n'):
                if 'Hardware UUID' in line:
                    current_uuid = line.split(':')[1].strip()
                    break
            
            if current_uuid:
                # 备份当前UUID
                backup_dir = Path.home() / "CursorResetPlus" / "backups" / "HardwareUUID"
                backup_dir.mkdir(parents=True, exist_ok=True)
                backup_path = backup_dir / f"HardwareUUID_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                
                with open(backup_path, 'w') as f:
                    f.write(current_uuid)
                self.update_status(f"已备份Hardware UUID到: {backup_path}", level="success")
            
            self.update_status("macOS重置完成", level="success")
            
        except Exception as e:
            self.logger.error(f"macOS重置出错: {str(e)}")
            raise

    def linux_reset(self):
        """Linux系统重置"""
        try:
            self.update_status("开始Linux系统重置...", level="info")
            
            appimage_path = self.appimage_path_var.get()
            if not appimage_path or not os.path.exists(appimage_path):
                raise ValueError("请选择有效的AppImage文件路径")
                
            # 创建临时目录
            temp_dir = Path.home() / "CursorResetPlus" / "temp"
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # 备份原始AppImage
            backup_dir = Path.home() / "CursorResetPlus" / "backups" / "AppImage"
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / f"Cursor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.AppImage"
            shutil.copy2(appimage_path, backup_path)
            
            self.update_status("正在提取AppImage...", level="info")
            subprocess.run([appimage_path, "--appimage-extract"], cwd=temp_dir, check=True)
            
            # 修改相关文件
            files_to_modify = [
                temp_dir / "squashfs-root/resources/app/out/main.js",
                temp_dir / "squashfs-root/resources/app/out/vs/code/node/cliProcessMain.js"
            ]
            
            for file_path in files_to_modify:
                if file_path.exists():
                    self.update_status(f"正在修改: {file_path.name}", level="info")
                    content = file_path.read_text(encoding='utf-8')
                    
                    # 替换machine-id相关代码
                    content = content.replace('"uuidgen"', '"echo \\"$(uuidgen)\\""')
                    
                    file_path.write_text(content, encoding='utf-8')
            
            self.update_status("正在重新打包AppImage...", level="info")
            subprocess.run(["appimagetool", "-n", "./squashfs-root"], cwd=temp_dir, check=True)
            
            # 清理临时文件
            shutil.rmtree(temp_dir / "squashfs-root")
            self.update_status("Linux重置完成", level="success")
            
        except Exception as e:
            self.logger.error(f"Linux重置出错: {str(e)}")
            raise

    def update_storage_json(self):
        """更新storage.json文件"""
        try:
            self.update_status("开始更新storage.json...", level="info")
            
            # 确定storage.json路径
            if self.os_type == "windows":
                storage_path = Path(os.getenv("APPDATA")) / "Cursor" / "User" / "globalStorage" / "storage.json"
            elif self.os_type == "darwin":
                storage_path = Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "storage.json"
            else:
                storage_path = Path.home() / ".config" / "Cursor" / "User" / "globalStorage" / "storage.json"

            if not storage_path.exists():
                raise FileNotFoundError(f"未找到storage.json文件: {storage_path}")

            # 备份原文件
            backup_dir = Path.home() / "CursorResetPlus" / "backups" / "storage"
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / f"storage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            shutil.copy2(storage_path, backup_path)
            self.update_status(f"已备份storage.json到: {backup_path}", level="success")

            # 生成新的ID
            new_ids = {
                "telemetry.machineId": str(uuid.uuid4()) + str(uuid.uuid4()),
                "telemetry.macMachineId": str(uuid.uuid4()),
                "telemetry.devDeviceId": str(uuid.uuid4()),
                "telemetry.sqmId": "{" + str(uuid.uuid4()).upper() + "}"
            }

            # 读取并更新文件
            data = json.loads(storage_path.read_text(encoding='utf-8'))
            data.update(new_ids)

            # 保存更新后的文件
            storage_path.write_text(json.dumps(data, indent=2), encoding='utf-8')

            # 输出新的ID
            for key, value in new_ids.items():
                self.update_status(f"新的 {key}: {value}", level="info")

            self.update_status("storage.json更新完成", level="success")

        except Exception as e:
            self.logger.error(f"更新storage.json出错: {str(e)}")
            raise

    def start_reset(self):
        """开始重置过程"""
        try:
            # 禁用按钮
            self.reset_button.configure(state='disabled')
            self.restore_button.configure(state='disabled')
            
            # 检查Cursor是否运行
            if self.check_cursor_process():
                self.update_status("请先关闭 Cursor 再继续...", level="warning")
                messagebox.showwarning("警告", "请先关闭 Cursor 再继续！")
                self.wait_for_cursor_exit()
            
            self.update_progress(0)
            self.update_status("开始重置过程...", level="info")
            
            # 根据操作系统执行相应的重置
            os_type = self.os_var.get().lower()
            if os_type == "windows":
                self.windows_reset()
            elif os_type == "macos":
                self.macos_reset()
            elif os_type == "linux":
                self.linux_reset()
                
            self.update_progress(50)
            self.update_status("系统特定的重置完成", level="success")
            
            # 更新storage.json
            self.update_storage_json()
            
            self.update_progress(100)
            self.update_status("重置完成！", level="success")
            messagebox.showinfo("成功", "Cursor ID 已成功重置！")
            
        except Exception as e:
            self.handle_error(e, "重置过程")
            
        finally:
            # 恢复按钮状态
            self.reset_button.configure(state='normal')
            self.restore_button.configure(state='normal')
            self.update_progress(0)

    def restore_backup(self):
        """恢复备份"""
        try:
            backup_dir = Path.home() / "CursorResetPlus" / "backups"
            if not backup_dir.exists():
                messagebox.showinfo("提示", "没有找到可用的备份文件")
                return
                
            # 创建备份管理窗口
            backup_window = tk.Toplevel(self.root)
            backup_window.title("选择要恢复的备份")
            backup_window.geometry("800x500")
            
            # 创建备份列表
            columns = ("时间", "类型", "大小", "路径")
            tree = ttk.Treeview(backup_window, columns=columns, show="headings")
            
            for col in columns:
                tree.heading(col, text=col)
            
            tree.column("时间", width=150)
            tree.column("类型", width=100)
            tree.column("大小", width=100)
            tree.column("路径", width=400)
            
            # 添加滚动条
            scrollbar = ttk.Scrollbar(backup_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 添加按钮
            button_frame = ttk.Frame(backup_window)
            button_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(
                button_frame,
                text="恢复选中",
                command=lambda: self.restore_selected_backup(tree, backup_window)
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                button_frame,
                text="取消",
                command=backup_window.destroy
            ).pack(side=tk.LEFT, padx=5)
            
            # 加载备份列表
            self.load_backup_list(tree)
            
        except Exception as e:
            self.handle_error(e, "恢复备份")

    def show_process_manager(self):
        """显示进程管理器"""
        process_window = tk.Toplevel(self.root)
        process_window.title("进程管理器")
        process_window.geometry("600x400")
        
        # 创建进程列表
        columns = ("PID", "名称", "内存使用", "状态")
        tree = ttk.Treeview(process_window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        def update_process_list():
            for item in tree.get_children():
                tree.delete(item)
            
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    tree.insert("", tk.END, values=(
                        info['pid'],
                        info['name'],
                        f"{info['memory_percent']:.1f}%",
                        info['status']
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            process_window.after(1000, update_process_list)
        
        update_process_list()

    def show_backup_manager(self):
        """显示备份管理器"""
        backup_window = tk.Toplevel(self.root)
        backup_window.title("备份管理器")
        backup_window.geometry("800x500")
        
        # 创建备份列表
        columns = ("时间", "类型", "大小", "路径")
        tree = ttk.Treeview(backup_window, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.column("时间", width=150)
        tree.column("类型", width=100)
        tree.column("大小", width=100)
        tree.column("路径", width=400)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # 添加工具栏
        toolbar = ttk.Frame(backup_window)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="恢复选中", command=lambda: self.restore_selected_backup(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="删除选中", command=lambda: self.delete_selected_backup(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="刷新列表", command=lambda: self.refresh_backup_list(tree)).pack(side=tk.LEFT, padx=5)
        
        self.refresh_backup_list(tree)

    def refresh_backup_list(self, tree):
        """刷新备份列表"""
        for item in tree.get_children():
            tree.delete(item)
            
        backup_dir = Path.home() / "CursorResetPlus" / "backups"
        if backup_dir.exists():
            for item in backup_dir.rglob("*"):
                if item.is_file():
                    tree.insert("", tk.END, values=(
                        datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        item.suffix[1:] if item.suffix else "未知",
                        f"{item.stat().st_size / 1024:.1f} KB",
                        str(item)
                    ))

    def load_backup_list(self, tree):
        """加载备份列表"""
        try:
            # 清空现有项目
            for item in tree.get_children():
                tree.delete(item)
            
            backup_dir = Path.home() / "CursorResetPlus" / "backups"
            if backup_dir.exists():
                for item in backup_dir.rglob("*"):
                    if item.is_file():
                        # 获取文件信息
                        mtime = datetime.fromtimestamp(item.stat().st_mtime)
                        size = item.stat().st_size
                        file_type = item.suffix[1:] if item.suffix else "未知"
                        
                        tree.insert("", tk.END, values=(
                            mtime.strftime("%Y-%m-%d %H:%M:%S"),
                            file_type,
                            f"{size / 1024:.1f} KB",
                            str(item)
                        ))
        except Exception as e:
            self.handle_error(e, "加载备份列表")

    def restore_selected_backup(self, tree, backup_window):
        """恢复选中的备份"""
        try:
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("警告", "请先选择要恢复的备份文件")
                return
            
            item = tree.item(selected[0])
            backup_path = Path(item['values'][3])
            
            if not backup_path.exists():
                messagebox.showerror("错误", "备份文件不存在")
                return
            
            if not messagebox.askyesno("确认", "确定要恢复选中的备份吗？\n此操作将覆盖当前配置。"):
                return
            
            # 根据备份文件类型执行不同的恢复操作
            file_type = backup_path.suffix.lower()
            
            if file_type == '.json':
                # 恢复storage.json
                if self.os_type == "windows":
                    target_path = Path(os.getenv("APPDATA")) / "Cursor" / "User" / "globalStorage" / "storage.json"
                elif self.os_type == "darwin":
                    target_path = Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "storage.json"
                else:
                    target_path = Path.home() / ".config" / "Cursor" / "User" / "globalStorage" / "storage.json"
                
                shutil.copy2(backup_path, target_path)
                self.update_status(f"已恢复storage.json: {backup_path}", level="success")
                
            elif file_type == '.txt':
                if 'machineguid' in backup_path.stem.lower():
                    # 恢复Windows MachineGuid
                    with open(backup_path, 'r') as f:
                        guid = f.read().strip()
                    
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, guid)
                    winreg.CloseKey(key)
                    self.update_status(f"已恢复MachineGuid: {guid}", level="success")
                    
                elif 'hardwareuuid' in backup_path.stem.lower():
                    # 恢复macOS Hardware UUID
                    with open(backup_path, 'r') as f:
                        uuid = f.read().strip()
                    self.update_status(f"已恢复Hardware UUID: {uuid}", level="success")
                    
            elif file_type == '.appimage':
                # 恢复Linux AppImage
                target_path = Path(self.appimage_path_var.get())
                if target_path.exists():
                    shutil.copy2(backup_path, target_path)
                    self.update_status(f"已恢复AppImage: {backup_path}", level="success")
                else:
                    messagebox.showerror("错误", "请先选择AppImage目标路径")
                    return
            
            messagebox.showinfo("成功", "备份恢复成功！")
            backup_window.destroy()
            
        except Exception as e:
            self.handle_error(e, "恢复备份")

    def delete_selected_backup(self, tree):
        """删除选中的备份"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的备份文件")
            return
            
        if messagebox.askyesno("确认", "确定要删除选中的备份吗？"):
            for item in selected:
                backup_path = tree.item(item)['values'][3]
                try:
                    os.remove(backup_path)
                    tree.delete(item)
                except Exception as e:
                    messagebox.showerror("错误", f"删除备份文件时出错：{str(e)}")

    def show_system_info(self):
        """显示系统信息"""
        info_window = tk.Toplevel(self.root)
        info_window.title("系统信息")
        info_window.geometry("600x400")
        
        info_text = tk.Text(info_window, wrap=tk.WORD, padx=10, pady=10)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        # 收集系统信息
        info = [
            f"操作系统: {platform.system()} {platform.release()}",
            f"处理器: {platform.processor()}",
            f"Python版本: {platform.python_version()}",
            f"总内存: {psutil.virtual_memory().total / (1024**3):.1f} GB",
            f"可用内存: {psutil.virtual_memory().available / (1024**3):.1f} GB",
            f"CPU使用率: {psutil.cpu_percent()}%",
            f"磁盘使用情况:"
        ]
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info.append(f"  {partition.mountpoint}: 总空间 {usage.total / (1024**3):.1f} GB, "
                          f"已用 {usage.used / (1024**3):.1f} GB ({usage.percent}%)")
            except:
                pass
        
        info_text.insert(tk.END, "\n".join(info))
        info_text.config(state=tk.DISABLED)

    def export_logs(self):
        """导出日志"""
        log_dir = Path.home() / "CursorResetPlus" / "logs"
        if not log_dir.exists():
            messagebox.showinfo("提示", "没有找到日志文件")
            return
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")],
            initialfile=f"cursor_reset_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        )
        
        if save_path:
            try:
                shutil.make_archive(save_path[:-4], 'zip', log_dir)
                messagebox.showinfo("成功", f"日志已导出到：{save_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出日志时出错：{str(e)}")

    def clean_backups(self):
        """清理备份"""
        backup_dir = Path.home() / "CursorResetPlus" / "backups"
        if not backup_dir.exists():
            messagebox.showinfo("提示", "没有找到备份文件")
            return
            
        if messagebox.askyesno("确认", "确定要清理所有备份文件吗？"):
            try:
                shutil.rmtree(backup_dir)
                os.makedirs(backup_dir)
                messagebox.showinfo("成功", "备份文件已清理完成！")
            except Exception as e:
                messagebox.showerror("错误", f"清理备份文件时出错：{str(e)}")

    def show_about(self):
        """显示关于对话框"""
        about_window = tk.Toplevel(self.root)
        about_window.title("关于")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        # 设置关于窗口图标
        if hasattr(self, 'icon_path') and os.path.exists(self.icon_path):
            about_window.iconbitmap(self.icon_path)
            try:
                # 使用PIL处理图标
                icon = Image.open(self.icon_path)
                icon = icon.resize((64, 64), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(icon)
                
                icon_label = tk.Label(about_window, image=photo)
                icon_label.image = photo  # 保持引用
            except Exception as e:
                self.logger.error(f"加载图标出错: {str(e)}")
                icon_label = tk.Label(
                    about_window,
                    text="🔄",
                    font=("Segoe UI", 48),
                    fg='#007bff'
                )
        else:
            icon_label = tk.Label(
                about_window,
                text="🔄",
                font=("Segoe UI", 48),
                fg='#007bff'
            )
        
        icon_label.pack(pady=20)
        
        # 添加标题
        title_label = tk.Label(
            about_window,
            text="Cursor Reset Plus",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack()
        
        # 添加版本信息
        version_label = tk.Label(
            about_window,
            text=f"版本 {self.VERSION.lstrip('v')}",  # 移除v前缀
            font=("Segoe UI", 10)
        )
        version_label.pack()
        
        # 添加描述
        desc_label = tk.Label(
            about_window,
            text="一个用于重置 Cursor IDE 设备标识的跨平台工具",
            font=("Segoe UI", 10),
            wraplength=300
        )
        desc_label.pack(pady=10)
        
        # 添加链接
        link_label = tk.Label(
            about_window,
            text="访问项目主页",
            font=("Segoe UI", 10),
            fg='blue',
            cursor='hand2'
        )
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/hamflx/cursor-reset"))

    def change_theme(self, theme_name):
        """切换主题"""
        self.style.set_theme(theme_name)

    def auto_detect_os(self):
        """自动检测操作系统"""
        detected_os = platform.system()
        self.os_var.set(detected_os)
        self.update_appimage_widgets()
        self.update_status(f"已自动检测操作系统：{detected_os}")

    def quick_reset(self):
        """快速重置（跳过确认）"""
        if not messagebox.askyesno("确认", "快速重置将跳过部分确认步骤，是否继续？"):
            return
        
        self.run_in_thread(self.start_reset)

    def cleanup_threads(self):
        """清理已完成的线程"""
        self.running_threads = [t for t in self.running_threads if t.is_alive()]
        
    def run_in_thread(self, target, daemon=True):
        """在新线程中运行函数"""
        self.cleanup_threads()  # 清理已完成的线程
        thread = threading.Thread(target=target, daemon=daemon)
        self.running_threads.append(thread)
        thread.start()
        return thread

    def handle_error(self, error, operation="操作"):
        """统一错误处理"""
        error_msg = str(error)
        self.logger.error(f"{operation}时出错: {error_msg}")
        self.update_status(f"{operation}失败: {error_msg}", level="error")
        
        # 显示错误对话框
        messagebox.showerror("错误", f"{operation}时出现错误：\n{error_msg}")
        
        # 尝试恢复
        try:
            self.cleanup_threads()  # 清理所有线程
            self.progress_var.set(0)  # 重置进度条
            self.reset_button.configure(state='normal')  # 重置按钮状态
            self.restore_button.configure(state='normal')
        except:
            pass  # 忽略恢复过程中的错误

    def __del__(self):
        """析构函数，确保清理所有线程"""
        for thread in self.running_threads:
            if thread.is_alive():
                thread.join(timeout=1.0)

def main():
    # 在Windows系统上检查管理员权限
    if sys.platform == 'win32' and not is_admin():
        if run_as_admin():
            sys.exit(0)
        else:
            messagebox.showerror("错误", "此程序需要管理员权限才能运行。")
            sys.exit(1)
    
    root = tk.Tk()
    app = CursorResetPlus(root)
    root.mainloop()

if __name__ == "__main__":
    main() 