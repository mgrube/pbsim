pbsim
=====

This is a simulator written in Python that simulates the effects of the Pitch Black attack against Freenet's 
Darknet location swapping algorithm. The main body of functions can be found in pynetsim.py

It's important to note that these files assume you are running them in iPython, as the pylab hist() function 
is used without importing any libraries.

Requirements
------------

- networkx: https://networkx.github.io/
- pylab: http://scipy.org/install.html

Usage
-----

    ./testfixpitchblack.py
