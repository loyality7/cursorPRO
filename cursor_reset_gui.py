import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
import json
import uuid
import random
import shutil
import winreg
import time
from datetime import datetime
from tkinter import font as tkfont

class CursorResetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cursor Reset Tool")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 设置窗口最小尺寸
        self.root.minsize(800, 600)
        
        # 配置字体
        self.title_font = tkfont.Font(family="Segoe UI", size=24, weight="bold")
        self.status_font = tkfont.Font(family="Segoe UI", size=10)
        self.button_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")  # 增大字体并加粗
        
        # 设置样式
        style = ttk.Style()
        style.configure("Main.TFrame", background='#f0f0f0')
        style.configure("Card.TFrame", background='white', relief='flat')
        
        # 使用自定义按钮替代ttk按钮
        class CustomButton(tk.Button):
            def __init__(self, master=None, **kwargs):
                self.button_type = kwargs.pop('button_type', 'action')
                super().__init__(master, **kwargs)
                self.configure(relief='flat', borderwidth=0)
                self.bind('<Enter>', self.on_enter)
                self.bind('<Leave>', self.on_leave)

            def on_enter(self, e):
                if self.button_type == 'danger':
                    self['background'] = '#c82333'
                else:
                    self['background'] = '#0056b3'

            def on_leave(self, e):
                if self.button_type == 'danger':
                    self['background'] = '#dc3545'
                else:
                    self['background'] = '#007bff'

        # 创建主框架
        main_frame = ttk.Frame(root, style="Main.TFrame", padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        
        # 标题区域（带图标）
        title_frame = ttk.Frame(main_frame, style="Main.TFrame")
        title_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        title_frame.grid_columnconfigure(1, weight=1)
        
        # 图标（用文字代替图标）
        icon_label = tk.Label(title_frame, 
                            text="🔄",  # Unicode 图标
                            font=("Segoe UI", 32),
                            bg='#f0f0f0',
                            fg='#007bff')
        icon_label.grid(row=0, column=0, padx=(0, 15))
        
        # 标题和副标题
        title_label = tk.Label(title_frame,
                             text="Cursor Reset Tool",
                             font=self.title_font,
                             bg='#f0f0f0',
                             fg='#2c3e50')
        title_label.grid(row=0, column=1, sticky=tk.W)
        
        subtitle_label = tk.Label(title_frame,
                                text="重置 Cursor ID 和系统标识符",
                                font=("Segoe UI", 12),
                                bg='#f0f0f0',
                                fg='#666666')
        subtitle_label.grid(row=1, column=1, sticky=tk.W)
        
        # 状态卡片
        status_frame = ttk.Frame(main_frame, style="Card.TFrame", padding="20")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_rowconfigure(1, weight=1)
        
        # 状态标题
        status_title = tk.Label(status_frame,
                              text="操作状态",
                              font=("Segoe UI", 14, "bold"),
                              bg='white',
                              fg='#2c3e50')
        status_title.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # 状态文本框
        self.status_text = tk.Text(status_frame,
                                 height=15,
                                 width=70,
                                 wrap=tk.WORD,
                                 font=self.status_font,
                                 bg='#f8f9fa',
                                 fg='#212529',
                                 relief='flat',
                                 padx=10,
                                 pady=10)
        self.status_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # 禁用文本框编辑
        self.status_text.config(state=tk.DISABLED)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame, style="Main.TFrame")
        button_frame.grid(row=3, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # 重置按钮
        reset_button = CustomButton(button_frame,
                                  text="重置 Cursor ID",
                                  font=self.button_font,
                                  foreground='white',
                                  background='#007bff',
                                  activebackground='#0056b3',
                                  activeforeground='white',
                                  padx=30,
                                  pady=10,
                                  cursor='hand2',
                                  button_type='action',
                                  command=self.reset_cursor)
        reset_button.grid(row=0, column=0, padx=5, sticky=tk.E)
        
        # 退出按钮
        quit_button = CustomButton(button_frame,
                                 text="退出程序",
                                 font=self.button_font,
                                 foreground='white',
                                 background='#dc3545',
                                 activebackground='#c82333',
                                 activeforeground='white',
                                 padx=30,
                                 pady=10,
                                 cursor='hand2',
                                 button_type='danger',
                                 command=root.quit)
        quit_button.grid(row=0, column=1, padx=5, sticky=tk.W)
        
        # 配置根窗口的网格权重
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
        # 设置初始状态消息
        self.update_status('欢迎使用 Cursor Reset Tool\n请点击"重置 Cursor ID"按钮开始重置过程。')

    def update_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()

    def new_mac_machine_id(self):
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

    def new_random_id(self):
        return uuid.uuid4().hex + uuid.uuid4().hex

    def wait_for_cursor_exit(self):
        while True:
            try:
                if sys.platform == "win32":
                    cursor_running = "cursor.exe" in subprocess.check_output(["tasklist"]).decode()
                else:
                    cursor_running = "cursor" in subprocess.check_output(["ps", "aux"]).decode()
                
                if not cursor_running:
                    self.update_status("Cursor 已关闭，继续执行...")
                    break
                
                self.update_status("正在等待 Cursor 进程退出...")
                time.sleep(1)
            except:
                break

    def backup_machine_guid(self):
        try:
            # 创建备份目录
            backup_dir = os.path.join(os.path.expanduser("~"), "MachineGuid_Backups")
            os.makedirs(backup_dir, exist_ok=True)

            # 读取当前的 MachineGuid
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_READ)
            current_guid = winreg.QueryValueEx(key, "MachineGuid")[0]
            winreg.CloseKey(key)

            # 创建备份文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"MachineGuid_{timestamp}.txt")
            counter = 0

            while os.path.exists(backup_file):
                counter += 1
                backup_file = os.path.join(backup_dir, f"MachineGuid_{timestamp}_{counter}.txt")

            with open(backup_file, 'w') as f:
                f.write(current_guid)

            return backup_file
        except Exception as e:
            self.update_status(f"备份 MachineGuid 时出错: {str(e)}")
            return None

    def update_machine_guid(self):
        try:
            new_guid = str(uuid.uuid4())
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_guid)
            winreg.CloseKey(key)
            return new_guid
        except Exception as e:
            self.update_status(f"更新 MachineGuid 时出错: {str(e)}")
            return None

    def reset_cursor(self):
        try:
            # 检查 Cursor 是否在运行
            cursor_running = False
            try:
                if sys.platform == "win32":
                    cursor_running = "cursor.exe" in subprocess.check_output(["tasklist"]).decode()
                else:
                    cursor_running = "cursor" in subprocess.check_output(["ps", "aux"]).decode()
            except:
                pass

            if cursor_running:
                self.update_status("请先关闭 Cursor 再继续...")
                messagebox.showwarning("警告", "请先关闭 Cursor 再继续！")
                self.wait_for_cursor_exit()

            # 备份 MachineGuid
            machine_guid_backup = None
            if sys.platform == "win32":
                machine_guid_backup = self.backup_machine_guid()
                if machine_guid_backup:
                    self.update_status(f"MachineGuid 已备份到: {machine_guid_backup}")

            # 生成新的ID
            new_machine_id = self.new_random_id()
            new_mac_machine_id = self.new_mac_machine_id()
            new_dev_device_id = str(uuid.uuid4())
            new_sqm_id = "{" + str(uuid.uuid4()).upper() + "}"

            # 更新 storage.json
            if sys.platform == "win32":
                storage_path = os.path.join(os.getenv("APPDATA"), "Cursor", "User", "globalStorage", "storage.json")
            else:
                storage_path = os.path.expanduser("~/.config/Cursor/User/globalStorage/storage.json")

            if os.path.exists(storage_path):
                # 备份原文件
                backup_dir = os.path.join(os.path.expanduser("~"), "cursor_backups")
                os.makedirs(backup_dir, exist_ok=True)
                backup_file = os.path.join(backup_dir, f"storage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                shutil.copy2(storage_path, backup_file)

                # 保存原始文件属性
                original_attributes = os.stat(storage_path)
                
                # 如果文件是只读的，移除只读属性
                if sys.platform == "win32":
                    subprocess.run(['attrib', '-R', storage_path], check=False)

                # 更新文件
                with open(storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                data.update({
                    "telemetry.machineId": new_machine_id,
                    "telemetry.macMachineId": new_mac_machine_id,
                    "telemetry.devDeviceId": new_dev_device_id,
                    "telemetry.sqmId": new_sqm_id
                })

                # 使用 UTF-8 无 BOM 编码保存文件
                json_str = json.dumps(data, indent=2)
                if sys.platform == "win32":
                    json_str = json_str.replace('\n', '\r\n')
                
                with open(storage_path, 'wb') as f:
                    f.write(json_str.encode('utf-8-sig').replace(b'\xef\xbb\xbf', b''))

                # 恢复原始文件属性
                os.chmod(storage_path, original_attributes.st_mode)

                self.update_status("已成功更新 storage.json")
                self.update_status(f"备份文件保存在: {backup_file}")
                self.update_status(f"新的 machineId: {new_machine_id}")
                self.update_status(f"新的 macMachineId: {new_mac_machine_id}")
                self.update_status(f"新的 devDeviceId: {new_dev_device_id}")
                self.update_status(f"新的 sqmId: {new_sqm_id}")

                # 更新 Windows 注册表中的 MachineGuid
                if sys.platform == "win32":
                    new_machine_guid = self.update_machine_guid()
                    if new_machine_guid:
                        self.update_status(f"新的 MachineGuid: {new_machine_guid}")

                messagebox.showinfo("成功", "Cursor ID 已成功重置！")
            else:
                self.update_status("错误：未找到 storage.json 文件")
                messagebox.showerror("错误", "未找到 storage.json 文件！")

        except Exception as e:
            self.update_status(f"错误：{str(e)}")
            messagebox.showerror("错误", f"发生错误：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CursorResetGUI(root)
    root.mainloop() 