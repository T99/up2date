# up2date
Simple find-and-replace over project files since the last Git commit.

## Table of Contents

 - [Installation](#installation)
 - [Basic Usage](#basic-usage)
 - [License](#license)

## Installation
Install from PyPi with
```
$ pip install up2date
```

**Note** _At time of pushing this code, this package is not yet live on PyPi._

You can also download this source and install it locally:

```
$ git clone https://github.com/T99/up2date.git your/desired/path
$ pip install your/desired/path
```

This project does use Python 3+, so if you're having trouble installing using plain `pip`, you can also try:

```
$ python3 -m pip install your/desired/path
```

...and you should be good to go!

## Basic Usage

Running the `up2date` command for a given set of files will perform an en-mass find-and-replace that ONLY acts on files that have been modified since the most recent Git commit in the specified repository.

```
up2date v0.1.0
Simple find-and-replace over files since the last Git commit.
Usage: up2date <git_repo> <files...> <orig_text> <new_text>
       up2date -c <files...> <orig_text> <new_text>
  <git_repo>  specifies the location of the repository to check for the most recent commit.
  <files...>  is a space-separate list of files to find-and-replace inside of.
  <orig_text> is the text that should be replaced from the files specified.
  <new_text>  is the text with which to replace <orig_text>.
  -c          specifies that the current working directory should be used as the Git repository.
  -s          specifies that this tool should silently exclude non-applicable paths.
```

## License
up2date is made available under the GNU General Public License v3.

Copyright (C) 2019 Trevor Sears
