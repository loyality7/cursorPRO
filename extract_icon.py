import os
import sys
import shutil

def extract_icon(exe_path, output_path):
    """从exe文件中提取图标并保存为ico文件"""
    try:
        # 直接复制图标文件
        icon_path = os.path.join(os.path.dirname(exe_path), "resources", "app", "resources", "icons", "cursor.ico")
        if os.path.exists(icon_path):
            shutil.copy2(icon_path, output_path)
            return True
            
        return False
    except Exception as e:
        print(f"提取图标时出错: {str(e)}")
        return False

if __name__ == "__main__":
    cursor_exe = os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\cursor\Cursor.exe")
    cursor_dir = os.path.dirname(cursor_exe)
    
    if not os.path.exists(cursor_exe):
        print(f"未找到Cursor.exe: {cursor_exe}")
        sys.exit(1)

    output_path = os.path.abspath("icon.ico")
    if extract_icon(cursor_exe, output_path):
        print(f"图标已保存到: {output_path}")
    else:
        print("提取图标失败") 