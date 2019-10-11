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
	
	previous_working_directory = os.getcwd()
	
	if is_git_repo(repo_path):
		os.chdir(repo_path)
		result = subprocess.run(["git", "log", "-1", "--format=%ct"], stdout=subprocess.PIPE).stdout.decode('utf-8')
		os.chdir(previous_working_directory)
		return int(result)
	
	else:
		raise ValueError("Provided path was not a git repository directory.")

def find_and_replace_in_file(file_path: str, content: str, replacement: str) -> int:
	
	if path.exists(file_path) and path.isfile(file_path):

		lines: List[str] = []

		with open(file_path) as f:

			lines = f.readlines()
			
		modified_lines = []
		modifications = 0
		
		for line in lines:
			while content in line:
				line = line.replace(content, replacement, 1)
				modifications += 1
			modified_lines.append(line)

		with open(file_path, "w") as f:

			f.writelines(modified_lines)
			
		return modifications

	else:

		print("Could not find file in order to replace text: '" + file_path + "'")
		return 0
	
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
	
	if not is_git_repo(git_repo):
		print(path.abspath(git_repo))
		invalid_git_repo(git_repo)
		exit(1)
		
	if should_fail_silently:
		files = [file for file in files if path.exists(file) and path.isfile(file)]
		
	modifications = run(git_repo, files, orig_text, new_text)
	
	num_of_files = len(files)
	print("Successfully performed " + str(modifications) + " modification" + ("s" if modifications != 1 else "") +
			" over " + str(num_of_files) + " file" + ("s" if num_of_files != 1 else "") + ".")

def run(repo_path: str, files: List[str], orig_text: str, new_text: str) -> int:
	
	"""
	Finds and replaces all occurrences of the 'orig_text' string with the 'new_text' string in each of the file paths
	specified if the file has been updated since the last commit to the specified repository.
	
	:param repo_path: A path to a valid Git repository.
	:param files: A list of files to conditionally find-and-replace in.
	:param orig_text: The text to replace.
	:param new_text: The text with which to replace.
	:return: The total number of find-and-replace operations that occurred.
	"""
	
	if not is_git_repo(repo_path):
		
		raise ValueError("The provided path did not resolve to a valid Git repository.")
	
	last_commit_timestamp = get_timestamp_from_git_repo(repo_path)
	
	if not any([(path.exists(file) and path.isfile(file)) for file in files]):
		
		raise ValueError("Some provided input file was invalid/did not exist.")
	
	modifications = 0
	
	for file in files:
		
		last_modification_timestamp = path.getmtime(file)
		
		if last_modification_timestamp > last_commit_timestamp:
			
			modifications += find_and_replace_in_file(file, orig_text, new_text)
			
	return modifications