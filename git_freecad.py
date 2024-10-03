#!/usr/bin/env python3

import sys
import os
import os.path
import subprocess
import shutil

from typing import *

dir = "fcstd"
os.makedirs(dir, exist_ok=True)

args = sys.argv[1:]

def help():
	print("Usage: git-freecad <command> [<args>]")
	sys.exit(1)

#only_directories = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
def get_fcsd_files():
	res = []
	for file in os.listdir("."):
		if file.lower().endswith(".fcstd"):
			res.append(file)
	return res

def get_fcsd_directories():
	res = []
	for file in os.listdir(dir):
		if os.path.isdir(f"{dir}/{file}"):
			res.append(file)
	return res

if len(args) == 0:
	help()

def remove_fcsd_extension(file: str) -> str:
	return file[:-len(".fcstd")]

def unzip(file: str) -> None:
	fn = remove_fcsd_extension(file)
	if "." in fn:
		raise Exception(f"Invalid filename {file}")
	print(f"Unzipping {file} to {fn}")
	shutil.rmtree(f"{dir}/{fn}", ignore_errors=True)
	os.makedirs(f"{dir}/{fn}", exist_ok=True)
	files_list = exec(["unzip", "-Z1", file])
	print("Saving files list")
	with open(f"{dir}/{fn}/files.txt", "w") as f:
		f.write(files_list)
	print("Unzipping")
	exec(["unzip", file, "-d", f"{dir}/{fn}"])

def exec(command: List[str], dir: Optional[str] = ".") -> None:
	print(f"Executing {command}")
	res = subprocess.check_output(command, cwd=dir).decode('utf-8')
	return res

def restore() -> None:
	for fn in get_fcsd_directories():
		print(f"Restoring {fn}")
		with open(f"{dir}/{fn}/files.txt") as f:
			files = f.read().split("\n")
		target = f"{fn}.FCStd"
		if os.path.exists(target):
			if input(f"{target} already exists, overwrite? [y/n]") != "y":
				sys.exit(0)
		exec(["zip", "-r", f"../../{target}", *files], dir=f"{dir}/{fn}")

if args[0] == "unzip":
	for file in get_fcsd_files():
		unzip(file)
elif args[0] == "stage":
	for file in get_fcsd_files():
		unzip(file)
	print("Staging")
	exec(["git", "add", dir])
elif args[0] == "checkout":
	if len(args) == 0:
		help()
	exec(["git", "checkout", args[1]])
	restore()
elif args[0] == "restore":
	restore()
else:
	help()