#   
#   Created by Trevor Sears <trevorsears.main@gmail.com>.
#   4:32 PM -- October 07th, 2019.
#   Project: up2date
#   

from distutils.core import setup
from up2date.packageinfo import NAME, VERSION, DESCRIPTION

setup(
	name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	author="Trevor Sears",
	author_email="trevorsears.main@gmail.com",
	url="https://github.com/T99/up2date",
	scripts=["bin/up2date"]
)
