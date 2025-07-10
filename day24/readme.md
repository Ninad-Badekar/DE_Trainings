#  Linux Fundamentals & File System Architecture

This guide covers the core concepts of Linux architecture, basic commands, file system hierarchy, and user management including sudo privileges. It is designed for beginners and system administrators getting started with Linux.

---

##  Contents

1. [Windows vs Linux](#1-windows-vs-linux)
2. [Linux Architecture](#2-understand-linux-architecture)
3. [Basic Linux Commands](#3-basic-linux-commands)
4. [Linux Command Line](#4-linux-command-line)
5. [File System Architecture](#5-file-system-architecture)
6. [User Management & Sudo Users](#6-user-management--sudo-users)

---

## 1 Windows vs Linux

| Feature              | Linux                                  | Windows                                |
|----------------------|-----------------------------------------|----------------------------------------|
| Open Source          | ✅ Yes                                 | ❌ No (Proprietary)                    |
| Command Line Focus   | 🖥️ Strong (Bash, Shell)                | ⚠️ Limited (CMD, PowerShell)           |
| File System          | ext4, xfs, btrfs                       | NTFS, FAT32                            |
| Security             | 🔒 Strong (permissions, sudo)          | Moderate (UAC, Defender)               |
| Package Management   | `apt`, `yum`, `dnf`, etc.              | Manual installers or `winget`          |
| Community Support    | ✅ Large, global                        | Official + limited open communities    |

---

## 2 Understand Linux Architecture

+----------------------------+
| User Applications |
+----------------------------+
| Shell (Bash, Zsh, etc.) |
+----------------------------+
| Kernel (core of the OS) |
| - Process mgmt |
| - Memory mgmt |
| - Device drivers |
+----------------------------+
| Hardware (CPU, Disk, RAM) |
+----------------------------+

bash


- **Monolithic kernel**: Linux kernel has all core components in one piece.
- Supports modular loading of device drivers and file systems.

---

## 3 Basic Linux Commands

```bash
pwd         # Show current directory
ls -l       # List files in long format
cd /path    # Change directory
touch file  # Create a file
mkdir dir   # Create a directory
rm file     # Delete a file
cp a b      # Copy file a to b
mv a b      # Move/rename file a to b
cat file    # Show file content
man ls      # Manual/help for 'ls'
```
## 4 Linux Command Line
Shell: Command interpreter (e.g., Bash, Zsh)

Prompt: $ for regular users, # for root

Use TAB for autocompletion and ↑/↓ to scroll command history

Use Ctrl + C to cancel running process

## 5 File System Architecture
🔹 Key Folders in / (root):
Directory	Purpose
/bin	Essential user commands (ls, cp, etc.)
/boot	Boot loader files (kernel)
/dev	Device files
/etc	Configuration files
/home	User home directories
/lib	Shared libraries
/media	Mounted removable media
/mnt	Temporary mount points
/proc	Kernel & process info (virtual)
/root	Root user’s home directory
/sbin	System binaries
/tmp	Temporary files
/usr	User apps, libraries
/var	Logs, cache, spool files

## 6 User Management & Sudo Users
- List Existing Users
```bash
cat /etc/passwd
```
- Create User (with home directory) using adduser
```bash
sudo adduser ninad
# Then login:
su - ninad
```
- Create User using useradd
```bash
sudo useradd -m -s /bin/bash john
sudo passwd john
# Then login:
su - john
```
- Provide Sudo Access with Password Prompt
```bash
sudo usermod -aG sudo john
# Or edit /etc/sudoers:
sudo visudo
# Add:
john ALL=(ALL:ALL) ALL
```
- Provide Sudo Access WITHOUT Password Prompt
```bash
sudo visudo
# Add:
john ALL=(ALL) NOPASSWD:ALL
```
- Provide Sudo Using usermod
```bash
sudo usermod -aG sudo username
```
- Delete User with Home Directory
```bash
sudo deluser --remove-home john
```
- Delete User but Keep Home Directory
```bash
sudo deluser john
```