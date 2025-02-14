import os
import sys
import shutil
from cx_Freeze import setup, Executable
import ttkthemes
import site
import pkgutil
import tkinter
import _tkinter

# 获取tkinter库路径
tcl_path = os.path.dirname(_tkinter.__file__)
tcl_lib = os.path.join(tcl_path, 'tcl8.6')
tk_lib = os.path.join(tcl_path, 'tk8.6')

# 获取ttkthemes的主题文件路径
themes_path = os.path.join(os.path.dirname(ttkthemes.__file__), "themes")

# 获取所有主题文件
theme_files = []
for root, dirs, files in os.walk(themes_path):
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, os.path.dirname(ttkthemes.__file__))
        theme_files.append((full_path, os.path.join("lib", "ttkthemes", rel_path)))

# 获取所有PIL插件
pil_plugins = []
plugin_dir = os.path.join(os.path.dirname(pkgutil.get_loader("PIL").get_filename()), "plugins")
if os.path.exists(plugin_dir):
    for file in os.listdir(plugin_dir):
        if file.endswith('.py'):
            pil_plugins.append(f"PIL.{os.path.splitext(file)[0]}")

# 添加TCL/TK库文件
tcl_tk_files = []
if os.path.exists(tcl_lib):
    for root, dirs, files in os.walk(tcl_lib):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, tcl_lib)
            tcl_tk_files.append((full_path, os.path.join("lib", "tcl8.6", rel_path)))

if os.path.exists(tk_lib):
    for root, dirs, files in os.walk(tk_lib):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, tk_lib)
            tcl_tk_files.append((full_path, os.path.join("lib", "tk8.6", rel_path)))

# 依赖项
build_exe_options = {
    "packages": [
        "tkinter", 
        "ttkthemes", 
        "psutil", 
        "requests", 
        "PIL",
        "json",
        "uuid",
        "logging",
        "webbrowser",
        "threading",
        "datetime",
        "platform",
        "shutil",
        "ctypes",
        "urllib3",
        "idna",
        "certifi",
        "chardet",
        "win32api",
        "win32con",
        "win32gui",
    ] + pil_plugins,
    "includes": [
        "tkinter.ttk",
        "PIL._tkinter_finder",
        "ttkthemes.themed_tk",
        "pkg_resources",
        "appdirs",
    ],
    "include_files": [
        ("cursor_reset_plus.manifest", "cursor_reset_plus.manifest"),
        ("LICENSE", "LICENSE"),
        ("README.md", "README.md"),
        ("requirements.txt", "requirements.txt"),
        ("icon.ico", "icon.ico"),
    ] + theme_files + tcl_tk_files,
    "include_msvcr": True,
    "zip_include_packages": "*",
    "zip_exclude_packages": [],
    "excludes": ["test", "unittest", "pdb", "pydev", "pydevd"],
    "optimize": 2,
    "build_exe": "dist/CursorResetPlus"
}

# 目标文件
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # 使用Windows GUI

# 创建可执行文件
setup(
    name="Cursor Reset Plus",
    version="2.0.0",
    description="Cursor Reset Plus - 重置 Cursor IDE 设备标识的跨平台工具",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "cursor_reset_plus.py",
            base=base,
            target_name="CursorResetPlus.exe",
            icon="icon.ico" if os.path.exists("icon.ico") else None,
            manifest="cursor_reset_plus.manifest",
            shortcut_name="Cursor Reset Plus",
            shortcut_dir="DesktopFolder",
            copyright="Copyright © 2024",
            uac_admin=True  # 请求管理员权限
        )
    ]
) 