Team 12 Bomberman
=================

Python package dependencies:
- SIP
- Qt4
- PyQt4
- dataset

# How to run
```
python game.py
```

# Installation

## Mac OS X

Install the [brew package manager](http://brew.sh/) if not already present
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Install the pip package manage if not already present
```
sudo easy_install pip
```
Install qt
```
brew install Qt
```
Install SIP
```
brew install sip
```
Install PyQt
```
brew install pyqt
```
Install Dataset
```
pip install dataset
```

## Ubuntu

Install SIP and PyQt using aptitude
```
sudo apt-get install python-sip python-qt4
```
Install the pip package manager if not already present
```
sudo apt-get install python-pip
```
Install Dataset
```
pip install dataset
```

### Run directly in Ubuntu 12.04 without installation using the virtualenv

Inside the root directory, activate the python virtual environment:
```
source venv/bin/activate
```

Now `(venv)` should appear in front of your prompt. To start the game, run:
```
python game.py
```

### Unit tests
Inside the root directory run:
```
python -m unittest discover
```
