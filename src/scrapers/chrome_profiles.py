import json
import os


def get_chrome_profile_path():
    """Get the default Chrome user profile path on Windows."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        return None
    return os.path.join(local_app_data, "Google", "Chrome", "User Data")


def print_chrome_profiles_info():
    """Print username and email for each Chrome profile."""
    chrome_profile_path = get_chrome_profile_path()
    if not chrome_profile_path or not os.path.exists(chrome_profile_path):
        print("Chrome profile path not found.")
        return

    profiles = [
        name
        for name in os.listdir(chrome_profile_path)
        if os.path.isdir(os.path.join(chrome_profile_path, name))
        and (name.startswith("Profile") or name == "Default")
    ]

    for profile in profiles:
        profile_dir = os.path.join(chrome_profile_path, profile)
        preferences_path = os.path.join(profile_dir, "Preferences")
        if not os.path.exists(preferences_path):
            continue
        try:
            with open(preferences_path, "r", encoding="utf-8") as f:
                prefs = json.load(f)
            email = None
            name = None
            account_info = prefs.get("account_info", [])
            if account_info and isinstance(account_info, list):
                email = account_info[0].get("email")
                name = account_info[0].get("full_name")
            if not email:
                email = prefs.get("profile", {}).get("user_name")
            if not name:
                name = prefs.get("profile", {}).get("name")
            print(f"Profile: {profile}")
            print(f"  Name: {name}")
            print(f"  Email: {email}")
        except Exception as e:
            print(f"Could not read profile {profile}: {e}")


def get_chrome_profiles_info():
    """Return a list of dicts with info for each Chrome profile."""
    chrome_profile_path = get_chrome_profile_path()
    if not chrome_profile_path or not os.path.exists(chrome_profile_path):
        return []

    profiles = [
        name
        for name in os.listdir(chrome_profile_path)
        if os.path.isdir(os.path.join(chrome_profile_path, name))
        and (name.startswith("Profile") or name == "Default")
    ]

    result = []
    for profile in profiles:
        profile_dir = os.path.join(chrome_profile_path, profile)
        preferences_path = os.path.join(profile_dir, "Preferences")
        if not os.path.exists(preferences_path):
            continue
        try:
            with open(preferences_path, "r", encoding="utf-8") as f:
                prefs = json.load(f)
            info = {
                "profile": profile,
                "name": None,
                "email": None,
                "raw": prefs,
            }
            account_info = prefs.get("account_info", [])
            if account_info and isinstance(account_info, list):
                info["email"] = account_info[0].get("email")
                info["name"] = account_info[0].get("full_name")
            if not info["email"]:
                info["email"] = prefs.get("profile", {}).get("user_name")
            if not info["name"]:
                info["name"] = prefs.get("profile", {}).get("name")
            result.append(info)
        except Exception:
            continue
    return result
