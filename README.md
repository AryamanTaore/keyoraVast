# 🚀 Vast.ai Setup and Usage Guide

## 1️⃣ Generating a Public Key for Admin (Aryaman)

### If using macOS:
```bash
ssh-keygen -t rsa
ssh-add
ssh-add -l
cat ~/.ssh/id_rsa.pub
```
Example key:
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAZBAQDdxWwxwN5Lz7ubkMrxM57CHhVzOnZuLt5FHi7J8zFXCJHfr96w+ccBOBo2rtBBTTRDLnJjIsKLgBcC3+jGyZhpUNMFRVIJ7MeqdEHgHFvUUV/uBkb7RjbyyFcb4BCSYNggUZkMNNoNgEa3aqtBSzt47bnuGqKszs9bfACaPFtr9Wo0b8p4IYil/gfOY5kuSVwkqrBCWrg53/+T2rAk/02mWNHXyBktJAu1q9qTWcyO68JTDd0sa+4apSu+CsJMBJs3FcDDRAl3bcpiKwRbCkQ+N63ol4xDV3zQRebUc98CJPh04Gnc41W02lmdqFL2XG5U/rV8/JM7CawKiIz3dbkv bob@velocity
```

### If using Windows:
Open PowerShell and run:
```powershell
ssh-keygen -t rsa
Get-Content $env:USERPROFILE/.ssh/id_rsa.pub | Set-Clipboard
```
Send the generated public key back to the administrator.

---
## 2️⃣ 🔧 Installing `vastai`
To install Vast.ai CLI:
```bash
pip install vastai
```

---
## 3️⃣ 🔑 Setting Up API Key
Before using Vast.ai, set up your API key:
```bash
vastai set api-key [API_KEY]
```
Replace `[API_KEY]` with your actual API key.

---
## 4️⃣ 📂 Checking Available Resources
### 📖 General Help
To get a list of available commands:
```bash
python vast.py --help
```
For detailed help on specific commands:
```bash
python vast.py show instances --help
```

### 🖥️ Show Running or Stopped Instances
To list all instances:
```bash
python vast.py show instances
```

### 🔗 Show Active Connections (Dropbox, S3, etc.)
To check all configured connections:
```bash
python vast.py show connections
```

---
## 5️⃣ 🎯 Searching for GPU Offers
To search for available instances with specific hardware requirements:
```bash
python vast.py search offers 'num_gpus=2 gpu_name=A100_SXM4 gpu_ram>=80 disk_space>=100 datacenter=True inet_up>500 inet_down>500 duration>3' --on-demand
```
#### 📋 Explanation of Search Filters:
- `num_gpus=2` → Request at least 2 GPUs.
- `gpu_name=A100_SXM4` → Specify GPU model.
- `gpu_ram>=80` → Require at least 80GB per GPU.
- `disk_space>=100` → Ensure at least 100GB of disk space.
- `datacenter=True` → Use a datacenter instance for security.
- `inet_up>500` and `inet_down>500` → Require internet speeds > 500 Mbps.
- `duration>3` → Instance available for at least 3 days.
- `--on-demand` → Use on-demand instances.

---
## 6️⃣ ⚙️ Creating and Managing Instances
### 🛠️ Creating an Instance
To create an instance with a specific configuration:
```bash
vastai create instance [INSTANCE_ID] --template_hash c93fcc3479bdc59f8f906a17882e57c0 --disk [DISK_SIZE] --label [YOUR_NAME] --jupyter --direct
```
Replace:
- `[INSTANCE_ID]` with the instance ID.
- `[DISK_SIZE]` with the required disk space (recommended 100-200GB).
- `[YOUR_NAME]` with a custom label for your instance.
- `--jupyter` enables Jupyter Notebook.
- `--direct` ensures a faster direct connection.

### 🛠️ Stopping & Starting an Instance
To stop an instance:
```bash
vastai stop instance [INSTANCE_ID]
```
To start an instance:
```bash
vastai start instance [INSTANCE_ID]
```

---
## 7️⃣ 🔐 Connecting to an Instance
### 1️⃣ Retrieve SSH URL
To get the SSH URL:
```bash
vastai ssh-url [INSTANCE_ID]
```
Example output:
```
ssh://root@79.117.112.218:27638
```
### 2️⃣ Establish SSH Connection with Port Forwarding
```bash
ssh -p 27638 root@79.117.112.218 -L 8080:localhost:8080
```
This command:
- Connects via SSH (`root@79.117.112.218 -p 27638`).
- Forwards port `8080` from the instance to localhost.

### 3️⃣ Open Jupyter Notebook
In your browser, go to:
```
https://localhost:8080
```
### 4️⃣ Retrieve Jupyter Token
Inside the SSH terminal, run:
```bash
jupyter notebook list
```
Example output:
```
Currently running servers:
https://be3771f8591b:8080/?token=a3e33a7d6d2fde7b494985d260b3c188367e1f494b618e6d4d0bf446b0770ff5 :: /
```
Copy the token and use it to log into Jupyter Notebook.

### 5️⃣ Exiting the SSH Session
```bash
exit
```

---
## 8️⃣ ☁️ Cloud Copy & File Transfer
To copy files between an instance and a cloud provider:
```bash
vastai cloud copy --src [SOURCE_PATH] --dst [DEST_PATH] --instance [INSTANCE_ID] --connection [CONNECTION_ID] --transfer [TRANSFER_TYPE]
```
Example:
```bash
vastai cloud copy --src /folder --dst /workspace --instance 6003036 --connection 1001 --transfer "Instance To Cloud"
```
Replace:
- `[SOURCE_PATH]` → Source folder path.
- `[DEST_PATH]` → Target location.
- `[INSTANCE_ID]` → Instance ID (use `vastai show instances`).
- `[CONNECTION_ID]` → Cloud connection ID (use `vastai show connections`).
- `[TRANSFER_TYPE]` → `Instance To Cloud` or `Cloud To Instance`.

---
## 9️⃣ ❌ Destroying an Instance
To destroy an unused instance:
```bash
vastai destroy instance [INSTANCE_ID]
```

---
## 🔔 Additional Notes
- **Security Considerations:**
  - Use `datacenter=True` for security.
  - Ensure internet speed >500 Mbps (`inet_up/down>500`).
- **Optimizing Cost:**
  - Use `--on-demand` to avoid preemptible instances.
- **Storage Options:**
  - Run `python vast.py show connections` to check Dropbox/S3 connections.

---
This guide provides a complete workflow for setting up and managing Vast.ai instances, from installation to GPU searches, file transfers, and cloud storage. 🚀

