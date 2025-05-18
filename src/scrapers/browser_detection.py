def get_default_windows_browser():
    """Detect the default browser on Windows system"""
    import winreg

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice",
        ) as key:
            browser_name = winreg.QueryValueEx(key, "ProgId")[0]

        if "Chrome" in browser_name:
            return "chrome"
        elif "Firefox" in browser_name:
            return "firefox"
        elif "MSEdge" in browser_name:
            return "edge"
        else:
            return "chrome"  # Default to Chrome if detection fails
    except Exception:
        return "chrome"  # Default to Chrome on error
