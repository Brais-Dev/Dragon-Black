import os
import subprocess
import sys
from core.configuration_language import Translator

app = Translator()

def check_git():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except Exception:
        return False

def has_internet():
    """Check if there is an internet connection"""
    try:
        subprocess.run(["ping", "-c", "1", "github.com"], check=True, capture_output=True)
        return True
    except Exception:
        return False

def update_repo(repo_dir=None):
    """
    Check for updates and ask the user if they want to update.

    Args:
        repo_dir (str): Path to the repository. If None, uses the script's directory.
    """
    if repo_dir is None:
        repo_dir = os.path.dirname(os.path.abspath(__file__))

    if not check_git():
        print(app.t("enter_not_git"))
        return

    if not has_internet():
        print(app.t("enter_not_connection"))
        return

    try:
        os.chdir(repo_dir)
        print(app.t("checking_updates"))
        subprocess.run(["git", "fetch"], check=True)

        status = subprocess.run(
            ["git", "status", "-uno"],
            capture_output=True,
            text=True
        )

        if "behind" in status.stdout:
            print(app.t("updater_available"))
            choice = input("Do you want to update now? (y/n): ").strip().lower()
            if choice == "y":
                pull = subprocess.run(
                    ["git", "pull"],
                    capture_output=True,
                    text=True
                )
                print(pull.stdout)
                print("[*] Repository updated. Restarting script...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print("[*] Continuing without updating...")
        else:
            print("[*] Already up to date.")

    except subprocess.CalledProcessError as e:
        print("[-] Error running git:", e)
    except Exception as e:
        print("[-] Unexpected error:", e)
        
def update_change():
    print("🎉🎉 new packages")
    
    