# CSCI468Project
Compiler project for CSCI 468

## Prerequisites

### ANTLR v4
The ANTLR v4 jar file must be downloaded and included in the java classpath. An example for doing so on Linux/MacOS is provided below.
```
cd /usr/local/lib
sudo curl -O https://www.antlr.org/download/antlr-4.8-complete.jar
sudo vi ~/.bash_profile
```
Add the following line to your bash profile.
```
export CLASSPATH="/usr/local/lib/antlr-4.8-complete.jar:{$CLASSPATH}"
```
Then reload your bash profile.
```
source ~/.bash_profile
```

### Python 3.4.10 or newer
The grading machines have Python 3.4.10 installed, so all of our code is compatible with this version. Instructions for downloading Python can be found [here](https://www.python.org/downloads/).

### Additional Notes
The venv package used in the micro scripts requires that there be no spaces in the path to the project folder.

## Micro Files
The micro files check for the presence of an env directory. If it does not exist, a new virtual environment is created using venv, the antlr4-python3-runtime package is installed in the environment, and the ANTLR code is generated for the grammar. This is why you must delete the env folder if you wish to regenerate the ANTLR code. Then, the script runs our Main.py file. To run the Micro file, use the command below.
```
./Micro <args>
```
If you want ANTLR to regenerate the python files, you will need to delete the env folder before running the Micro file again.
```
rm -rf env
```

