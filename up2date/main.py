#   
#   Created by Trevor Sears <trevorsears.main@gmail.com>.
#   12:29 AM -- October 11th, 2019.
#   Project: up2date
#   

import os
from os import path
import subprocess
from typing import List
from sys import argv
from up2date.printouts import help_text, not_enough_args, invalid_git_repo

def is_git_repo(repo_path: str) -> bool:
	
	git_path = path.join(repo_path, ".git")
	
	return path.exists(repo_path) and path.isdir(repo_path) and path.exists(git_path) and path.isdir(git_path) 

def get_timestamp_from_git_repo(repo_path: str) -> int:
	
	if is_git_repo(repo_path):
		os.chdir(repo_path)
		result = subprocess.run(["git", "log", "-1", "--format=%ct"], stdout=subprocess.PIPE).stdout.decode('utf-8')
		return int(result)
	
	else:
		raise ValueError("Provided path was not a git repository directory.")

def find_and_replace_in_file(file_path: str, content: str, replacement: str) -> None:
	
	if path.exists(file_path) and path.isfile(file_path):

		lines: List[str] = []

		with open(file_path) as f:

			lines = f.readlines()

		lines = [line.replace(content, replacement) for line in lines]

		with open(file_path, "w") as f:

			f.writelines(lines)

	else:

		print("Could not find file in order to replace text: '" + file_path + "'")
	
def run_cli() -> None:
	
	arguments = argv[1:]
	num_of_args = len(arguments)
	using_cwd = "-c" in arguments
	should_fail_silently = "-s" in arguments
	
	if num_of_args == 0:
		help_text()
		exit(0)
	
	elif using_cwd and num_of_args < 3:
		not_enough_args("3+", str(num_of_args))
		exit(1)
		
	elif num_of_args < 4:
		not_enough_args("4+", str(num_of_args))
		exit(1)
		
	git_repo = os.getcwd() if using_cwd else arguments[0]
	orig_text, new_text = arguments[-2:]
	files = arguments[1:-2]
	
	print("Git repo: " + git_repo)
	print("Last modified: " + str(get_timestamp_from_git_repo(git_repo)))
	print("Orig text: " + orig_text)
	print("New text: " + new_text)
	print("Files: " + str(files))
	
	if not is_git_repo(git_repo):
		invalid_git_repo(git_repo)
		exit(1)
		
	if should_fail_silently:
		files = [file for file in files if path.exists(file) and path.isfile(file)]
		
	run(git_repo, files, orig_text, new_text)

def run(repo_path: str, files: List[str], orig_text: str, new_text: str) -> None:
	
	if not is_git_repo(repo_path):
		
		raise ValueError("The provided path did not resolve to a valid Git repository.")
	
	last_commit_timestamp = get_timestamp_from_git_repo(repo_path)
	
	if not any([(path.exists(file) and path.isfile(file)) for file in files]):
		
		raise ValueError("Some provided input file was invalid/did not exist.")
	
	for file in files:
		
		last_modification_timestamp = path.getmtime(file)
		
		if last_modification_timestamp > last_commit_timestamp:
			
			find_and_replace_in_file(file, orig_text, new_text)