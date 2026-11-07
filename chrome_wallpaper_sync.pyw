import os
import json
import urllib.request
import ctypes
import time
from pathlib import Path

def get_chrome_background_url(profile_name="Default"):
    """从 Chrome 配置文件中获取当前新标签页背景的 URL"""
    local_app_data = os.environ.get('LOCALAPPDATA')
    prefs_path = Path(local_app_data) / "Google" / "Chrome" / "User Data" / profile_name / "Preferences"
    
    if not prefs_path.exists():
        return None

    try:
        # Chrome 运行时可能在写入，偶尔会有读冲突，所以包在 try-except 中
        with open(prefs_path, 'r', encoding='utf-8') as f:
            prefs = json.load(f)
            
        custom_background = prefs.get('ntp', {}).get('custom_background_dict', {})
        return custom_background.get('background_url')
    except Exception:
        return None

def set_windows_wallpaper(image_path):
    """调用 Windows API 设置桌面壁纸"""
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDWININICHANGE = 2
    abs_path = os.path.abspath(image_path)
    
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 
        0, 
        abs_path, 
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
    )

def main():
    pictures_dir = Path(os.environ.get('USERPROFILE')) / "Pictures"
    save_path = pictures_dir / "chrome_sync_wallpaper.jpg"
    
    try:
        # 只获取一次，不加循环
        current_url = get_chrome_background_url(profile_name="Default")
        
        if current_url:
            urllib.request.urlretrieve(current_url, save_path)
            set_windows_wallpaper(save_path)
            
    except Exception:
        pass

if __name__ == "__main__":
    main()