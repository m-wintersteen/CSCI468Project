# CSCI468Project
Compiler project for CSCI 468

### Step 0: ANTLR Setup

We followed the guide at https://github.com/antlr/antlr4/blob/master/doc/getting-started.md to install ANTLR v4 and test the provided example. We are chosing to use Python3 for this project so the commands to generate the scanner and parser are slightly different:  `antlr4 -Dlanguage=Python3 Hello.g4`. To run the Driver code in the example, you must also install the Antlr v4 runtime from https://pypi.org/project/antlr4-python3-runtime. This can be done by running `pip3 install -r requirements.txt`. Example python driver code is taken from http://blog.anvard.org/articles/2016/03/15/antlr-python.html.

### Step 1: Scanner

In step 1, we define the tokens for the language in a grammar file and use ANTLR v4 to generate the Python3 code for the scanner. We then use the scanner code to output the type and value of each token for a given source file. To run the scanner program, run the following command from the src directory `python3 Part1.py <sourcefile>`, and replace \<sourcefile> with the path to the source code to tokenize. To diff the expected outputs against the actual output of the program for the different input files, run `./step1` from the tests directory.

