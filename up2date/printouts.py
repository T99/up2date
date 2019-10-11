#   
#   Created by Trevor Sears <trevorsears.main@gmail.com>.
#   12:59 AM -- October 11th, 2019.
#   Project: up2date
#   

from up2date.packageinfo import NAME, VERSION, DESCRIPTION
from os import path

def help_text() -> None:
	
	print(NAME + " " + VERSION)
	print(DESCRIPTION)
	print("Usage: " + NAME + " <git_repo> <files...> <orig_text> <new_text>")
	print("       " + NAME + " -c <files...> <orig_text> <new_text>")
	print("  <git_repo>  specifies the location of the repository to check for the most recent commit.")
	print("  <files...>  is a space-separate list of files to find-and-replace inside of.")
	print("  <orig_text> is the text that should be replaced from the files specified.")
	print("  <new_text>  is the text with which to replace <orig_text>.")
	print("  -c          specifies that the current working directory should be used as the Git repository.")
	print("  -s          specifies that this tool should silently exclude non-applicable paths.")

def not_enough_args(expected: str, actual: str) -> None:
	
	print("Not enough arguments. Expected " + expected + " but got " + actual + ".\n")
	help_text()
	
def invalid_git_repo(repo_path: str) -> None:
	
	print("The provided Git repository at '" + path.abspath(repo_path) + "' was invalid.")