# cl_auto
 Pulls Craigslist auto listings

## Setup
### python
```bash
brew install pyenv
# pyenv install 3.8.9
# pyenv local 3.8.9
# ln -s ~/.pyenv/versions/3.8.9/bin/python3.8 /usr/local/bin/python3.8
```
### pipenv
```bash
# new install (automatically installs python version via pyenv)
pipenv install

# updated dependencies (under virtual environment)
pipenv sync

# switched python versions, debugging (e.g., Pipfile.lock `Locking Failed!`)
# pipenv lock --clear
# pipenv install --skip-lock
pipenv --rm
pipenv install
```

## Usage
```bash
# activate virtualenv
$ pipenv shell

# run python script
(cl_auto) $ python cl_auto.py

# deactivate virtualenv
(cl_auto) $ exit
```

## SOURCES
TODO
