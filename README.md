# cl_auto
 Pulls Craigslist auto listings

## Setup
### python
```bash
# macOS
brew install pyenv

# *nix
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc

# python3.9
pyenv install 3.9.0
pyenv local 3.9.0
ln -s ~/.pyenv/versions/3.9.0/bin/python3.9 /usr/local/bin/python3.9
```
### pipenv
```bash
# new install (automatically installs python version via pyenv)
pip install --user pipenv
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

## Development
* Install `asdf`
```bash
# install asdf
git clone https://github.com/asdf-vm/asdf.git ~/.asdf
cd ~/.asdf
git checkout "$(git describe --abbrev=0 --tags)"

# ~/.bashrc
. $HOME/.asdf/asdf.sh
. $HOME/.asdf/completions/asdf.bash
```
* Install `node`
```bash
# install npm and node
curl -L https://git.io/n-install | N_PREFIX=~/.n bash -s -- -y

# ~/.bashrc (added automatically via `n-install`)
# export N_PREFIX="$HOME/.n"; [[ :$PATH: == *":$N_PREFIX/bin:"* ]] || PATH+=":$N_PREFIX/bin"

# rm -rf
npm install rimraf --global


```
* Install terraform
```bash
asdf plugin add terraform
asdf plugin list
```
* Install Docker Desktop for Windows[<sup>1</sup>](#1)
* Generate dependencies list: `pipenv lock --requirements > requirements.txt`

## TODO
* Update instructions
    * Mix and match from `jss_migrator` README.md
* Loop through `url` column and open each page in Playwright
    * ~~Keep Playwright open until each tab is closed~~ (timeout or ctrl-c workaround)
    * Headless option (i.e., don't open Playwright window, just capture results)
* [Dockerize script](https://github.com/pythoninthegrass/docker-python)
    * Test new `Dockerfile` (requirements.txt, `COPY /ms-playwright ...`) 
* [argparse](https://realpython.com/command-line-interfaces-python-argparse/)
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

[Playwright for Python](https://playwright.dev/python/)

[web scraping - How do you open multiple pages asynchronously with Playwright Python? - Stack Overflow](https://stackoverflow.com/questions/64664437/how-do-you-open-multiple-pages-asynchronously-with-playwright-python)

[asdf](https://asdf-vm.com/#/core-manage-asdf)

[n](https://github.com/tj/n#third-party-installers)

[How to Set Up Docker in WSL [Step-by-Step]](https://adamtheautomator.com/how-to-set-up-docker-in-wsl-step-by-step/)<a class="anchor" id="1"></a>
