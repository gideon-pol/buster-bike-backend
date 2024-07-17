import subprocess
import time
import threading

def git_pull():
    """Pulls the latest changes from the Git repository."""
    result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
    return result.stdout

server_process = None

def server_is_running():
    """Checks if the server is running."""
    global server_process
    return server_process is not None and server_process.poll() is None

def restart_server():
    """Restarts the server."""
    global server_process
    if server_is_running():
        server_process.terminate()  # Terminate the existing server process
        server_process.wait()  # Wait for the process to terminate
    # Start the server in a new subprocess
    server_process = subprocess.Popen(['python3', 'manage.py', 'runserver', '0.0.0.0:8000'])

def main():
    restart_server()

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