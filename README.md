# cl_auto
 Pulls Craigslist auto listings

## Setup
### python
```bash
brew install pyenv
# pyenv install 3.8.9
# pyenv local 3.8.9
# ln -s ~/.pyenv/versions/3.7.3/bin/python3.7 /usr/local/bin/python3.7
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
(meraki_portcylcle_cronjob) $ python main.py

# deactivate virtualenv
(meraki_portcylcle_cronjob) $ exit

## SOURCES
