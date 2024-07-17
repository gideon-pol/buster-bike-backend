import subprocess
import time

def git_pull():
    """Pulls the latest changes from the Git repository."""
    result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
    return result.stdout

def server_is_running():
    """Checks if the server is running."""
    result = subprocess.run(['pgrep', '-f', 'python3 manage.py runserver'], capture_output=True, text=True)
    return result.stdout != ''

def restart_server():
    """Restarts the server."""
    if server_is_running():
        subprocess.run(['pkill', '-f', 'python3 manage.py runserver'])
    subprocess.run(['python3', 'manage.py', 'runserver', '0.0.0.0:8000'])

def main():
    while True:
        print("Checking for changes...")
        output = git_pull()
        if 'Already up to date.' not in output:
            print("Changes detected, restarting server...")
            restart_server()
        else:
            print("No changes detected.")
        time.sleep(10)  # Wait for 5 minutes

if __name__ == "__main__":
    main()