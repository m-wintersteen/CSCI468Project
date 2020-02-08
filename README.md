# CSCI468Project
Compiler project for CSCI 468

Step 1: Scanner

We are chosing to use python for this project so the first step was to install antlr4 for python3 using pip

https://pypi.org/project/antlr4-python3-runtime/

Compilation of .g4 files is done like this:

java -Xmx500M -cp /usr/local/lib/antlr-4.8-complete.jar org.antlr.v4.Tool -Dlanguage=Python3 Hello.g4

Example python driver code is from http://blog.anvard.org/articles/2016/03/15/antlr-python.html