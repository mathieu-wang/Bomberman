Team 12 Bomberman
=================

Python package dependencies:
- SIP
- Qt4
- PyQt4
- dataset

# Installation

## Mac OS X

1. Install brew if not already present, follow instruction from http://brew.sh/
2. Install qt
```
brew install Qt
```
3. Install SIP
```
brew install sip
```
4. Install PyQt
```
brew install pyqt
```

## Ubuntu


### How to run directly in Ubuntu 12.04

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
