import subprocess
import sys
import json
import datetime
import socket
import os

# File to store logs
LOG_FILE = "vastai_logs.json"

def log_command(command, output):
    """Logs the command, timestamp, computer name, and output to a JSON file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    computer_name = socket.gethostname()

    # Create log entry
    log_entry = {
        "timestamp": timestamp,
        "computer_name": computer_name,
        "command": command,
        "output": output
    }

    # Load existing logs (if file exists)
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as file:
                logs = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []  # Reset if the file is corrupted or unreadable
    else:
        logs = []

    # Append new log entry
    logs.append(log_entry)

    # Write back to JSON file
    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)

def run_vastai_command(args):
    """Executes the Vast.ai command, logs the command unless it contains certain keywords, and prints the result."""
    command = ["vastai"] + args  # Auto-prepend "vastai"
    command_str = " ".join(command)

    try:
        # Check if the command requires confirmation (e.g., destroy, stop)
        confirm_required = any(cmd in ["destroy", "stop"] for cmd in args)

        if confirm_required:
            # For commands that require confirmation, use Popen and send "yes"
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate(input="yes\n")
        else:
            # Use subprocess.run for everything else (avoids hanging)
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output, error = result.stdout, result.stderr

        # Always print the output
        print(output.strip())

        # Ignore logging if the command contains specific keywords
        if any(ignored in command_str for ignored in ["--help", "-h", "search offers", "show instances", "show connections", "show endpoints", "set api-key", "show", "search"]):
            return
        
        # Replace "Command failed with error:" messages with just "Error" in the log
        sanitized_output = "Error" if "Command failed with error:" in output else output

        # Log the command and computer name along with the sanitized output
        log_command(command_str, sanitized_output)

    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        log_command(command_str, "Error")

    except Exception as e:
        print(f"An error occurred: {e}")
        log_command(command_str, "Error")

def main():
    if len(sys.argv) < 2:
        print("Usage: python vast.py [vastai commands...]")
        sys.exit(1)

    # Extract Vast.ai command arguments (since "vastai" is already prepended)
    vastai_args = sys.argv[1:]
    run_vastai_command(vastai_args)

if __name__ == "__main__":
    main()
