Team 12 Bomberman
=================

##########
Authors & Copyright notice

All rights reserved ©

Gabriel Gibeault-Girard, gabriel.gibeault-girard@mail.mcgill.ca
Mathieu Wang, mathieu.wang@mail.mcgill.ca
Stefan Tihanyi, stefan.tihanyi@mail.mcgill.ca
Michael Ho, micheal.ho@mail.mcgill.ca

##########
URLs

github's url: https://github.com/mcgill-ecse321/Team-12
git clone's url: git@github.com:mcgill-ecse321/Team-12.git

##########
Dependencies

Programming language: Python

Python package dependencies:
	- SIP
	- Qt4
    - PyQt4
	- dataset

Installation instruction given below.

##########
Platforms

This program was developed and tested on the following platforms:

    -Ubuntu, Sublime Text 2
    -Ubuntu, PyCharm
    -Mac OS X, PyCharm

##########
How to run the game

Just type: "python game.py" in the command line without the quote (INSIDE the src/ directory)

##########
Installation

Mac OS X:
=========

1)  Install the [brew package manager](http://brew.sh/) if not already present

2)  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

3)  Install Python 2.7 using brew if not already present (the native Apple Python is not compatible)

        brew install python

5)  Add the brew PYTHONPATH to your environment variables by adding the following line to .bash_profile

        export PATH=/usr/local/bin:$PATH

6)  Install the pip package manager if not already present

        sudo easy_install pip

7)  Install qt

        brew install Qt

8)  Install SIP

        brew install sip

9)  Install PyQt

        brew install pyqt

10) Install Dataset

        pip install dataset


Ubuntu:
=======

1)  Install SIP and PyQt using aptitude

        sudo apt-get install python-sip python-qt4

2)  Install the pip package manager if not already present

        sudo apt-get install python-pip

        install Dataset

        pip install dataset

##########
Unit tests

1)  Inside the root directory run:

        python -m unittest discover

