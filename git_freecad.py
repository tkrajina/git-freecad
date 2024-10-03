#!/usr/bin/env python3

import sys
import os
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
	for file in os.listdir():
		print(file.lower())
		if file.lower().endswith(".fcstd"):
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
	files_list = subprocess.check_output(["unzip", "-Z1", file]).decode('utf-8')
	print("Saving files list")
	with open(f"{dir}/{fn}/files.txt", "w") as f:
		f.write(files_list)
	print("Unzipping")
	print(subprocess.check_output(["unzip", file, "-d", f"{dir}/{fn}"]).decode('utf-8'))

if args[0] == "unzip":
	for file in get_fcsd_files():
		unzip(file)
elif args[0] == "stage":
	for file in get_fcsd_files():
		unzip(file)
	print("Staging")
	print(subprocess.check_output(["git", "add", dir]).decode('utf-8'))
elif args[0] == "restore":
	for file in get_fcsd_files():
		with open(f"{dir}/{file}/files.txt") as f:
			files = f.read().decode('utf-8')
		print(subprocess.check_output(["zip", "-r", f"../../{file}.FCStd", files], cwd=f"{dir}/{file}").decode('utf-8'))
	pass
else:
	help()