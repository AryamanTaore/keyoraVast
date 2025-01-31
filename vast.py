import subprocess
import sys
import json
import datetime
import socket
import os
from azure.storage.blob import BlobServiceClient

# File to store logs locally
LOG_FILE = "vastai_logs.json"

# Azure Blob Storage connection details
AZURE_BLOB_URL = "https://eyetrackingdata.blob.core.windows.net/public?"
CONTAINER_NAME = "keyora"
BLOB_NAME = "vastai_logs.json"
SAS_TOKEN = "sp=r&st=2025-01-31T23:18:02Z&se=2028-02-01T07:18:02Z&spr=https&sv=2022-11-02&sr=c&sig=f%2Bs0rsj6P333D66M9zeHdiw8xjs8N5I9GG6omvLUaEE%3D"


def download_data():
    """Downloads JSON log file from Azure Blob Storage."""
    try:
        # Initialize BlobServiceClient
        blob_service_client = BlobServiceClient(account_url="https://eyetrackingdata.blob.core.windows.net/public?sp=rw&st=2025-01-31T23:37:17Z&se=2028-02-01T07:37:17Z&spr=https&sv=2022-11-02&sr=c&sig=u1ceUkJ8by8LThl1E%2BEg%2B1wiq%2Bu6F89vjYzcdAYl8yo%3D")
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

        # Download JSON data
        blob_data = blob_client.download_blob().readall()
        json_data = json.loads(blob_data)

        # Save the latest logs locally
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4)

        # print("✅ JSON file downloaded and saved locally.")
        return json_data

    except Exception as e:
        # print(f" An error occurred during download: {e}")
        return []  # Return empty list if download fails


def upload_data():
    """Uploads the updated JSON log file to Azure Blob Storage."""
    try:
        # Read local JSON file
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            json_data = json.load(file)

        # Initialize BlobServiceClient
        blob_service_client = BlobServiceClient(account_url="https://eyetrackingdata.blob.core.windows.net/public?sp=rw&st=2025-01-31T23:37:17Z&se=2028-02-01T07:37:17Z&spr=https&sv=2022-11-02&sr=c&sig=u1ceUkJ8by8LThl1E%2BEg%2B1wiq%2Bu6F89vjYzcdAYl8yo%3D")
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

        # Upload JSON data to Azure
        blob_client.upload_blob(json.dumps(json_data, indent=4), overwrite=True)

        # print("✅ JSON file uploaded successfully.")

    except FileNotFoundError:
        pass
        # print(f" Error: Local file '{LOG_FILE}' not found.")
    except Exception as e:
        pass
        # print(f" An error occurred during upload: {e}")


def log_command(command, output):
    """Logs the command, timestamp, computer name, and output to the JSON file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    computer_name = socket.gethostname()

    # Create a new log entry
    log_entry = {
        "timestamp": timestamp,
        "computer_name": computer_name,
        "command": command,
        "output": output
    }

    # Load the latest logs from the downloaded JSON file
    logs = download_data()

    # Append new log entry
    logs.append(log_entry)

    # Write back to local file
    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)

    print("✅ Command logged successfully.")

    # Upload the updated logs back to Azure
    upload_data()


def run_vastai_command(args):
    """Executes the Vast.ai command, logs it, and prints the result."""
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
            output, error = result.stdout.strip(), result.stderr.strip()

        # Always print the output
        print(output)

        # Ignore logging for certain commands
        ignored_cmds = ["--help", "-h", "search offers", "show instances", "show connections", "show endpoints", "set api-key", "show", "search"]
        if any(ignored in command_str for ignored in ignored_cmds):
            return
        
        # Replace "Command failed with error:" messages with just "Error" in the log
        sanitized_output = "Error" if "Command failed with error:" in output else output

        # Log the command
        log_command(command_str, sanitized_output)

    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with error: {e.stderr}")
        log_command(command_str, "Error")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        log_command(command_str, "Error")


def main():
    if len(sys.argv) < 2:
        print("Usage: python vast.py [vastai commands...]")
        sys.exit(1)

    # Extract Vast.ai command arguments
    vastai_args = sys.argv[1:]

    # Ensure logs are downloaded first
    download_data()

    # Run Vast.ai command
    run_vastai_command(vastai_args)


if __name__ == "__main__":
    main()
