# cl_auto
 Pulls Craigslist auto listings

## Setup
### python
```bash
brew install pyenv
# pyenv install 3.9.0
# pyenv local 3.9.0
# ln -s ~/.pyenv/versions/3.9.0/bin/python3.9 /usr/local/bin/python3.9
```
### pipenv
```bash
# new install (automatically installs python version via pyenv)
pipenv install

# playwright
# See sources for WSL setup
pipenv run playwright install

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

## TODO
* Loop through `url` column and open each page in Playwright
    * Keep Playwright open until each tab is closed
    * Headless option (i.e., don't open Playwright window, just capture results)
* [argparse](https://realpython.com/command-line-interfaces-python-argparse/)
* [Dockerize script](https://github.com/pythoninthegrass/docker-python)
* Add SMTP
    * Google API account for mail server
    * Email csv
* Cron job to mail results weekly
* Convert to k8s pod
* Deploy to web host (e.g., AWS, Digital Ocean)

## SOURCES
[Enable GUIs on Windows Subsystem Linux (WSL) · Scott Spence](https://scottspence.com/2020/12/09/gui-with-wsl/#video-detailing-the-process)

[Using Graphical User Interfaces like Cypress' in WSL2](https://nickymeuleman.netlify.app/blog/gui-on-wsl2-cypress)

[Protecting X410 Public Access for WSL2 via Windows Defender Firewall - X410.dev](https://x410.dev/cookbook/wsl/protecting-x410-public-access-for-wsl2-via-windows-defender-firewall/)

