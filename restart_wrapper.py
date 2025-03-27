import os
import sys
import time
import subprocess

def restart_bot():
    while True:
        try:
            print("[INFO] Starting bot...")
            # Run the bot script
            process = subprocess.run([sys.executable, "vcbs.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Bot crashed with exit code {e.returncode}. Restarting in 5 seconds...")
            time.sleep(5)  # Wait for 5 seconds before restarting
        except FileNotFoundError:
            print("[ERROR] vcbs.py not found. Ensure the script is in the same directory.")
            os.system("taskkill")
            restart_bot()
        except KeyboardInterrupt:
            print("[INFO] Restart wrapper interrupted. Exiting...")
            break
        except AttributeError:
            print("[ERROR] A Command has failed, restarting")
            break
        else:
            print("[INFO] Bot exited normally. Restarting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    print("[INFO] Starting bot with restart wrapper...")
    restart_bot()