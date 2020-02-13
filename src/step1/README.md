### Setup

- The ANTLR v4 jar file must be downloaded to /usr/local/lib
```
cd /usr/local/lib
sudo curl -O https://www.antlr.org/download/antlr-4.8-complete.jar
```
- Python3 and the ANTLR v4 runtime package must be installed
```
pip3 install antlr4-python3-runtime
```

### Bash Script

Our bash script, Micro, starts by generating the lexer class from the .g4 file if it hasn't been generated yet. It then runs our main Python3 file and passes the first argument from the bash script. Our Python3 file creates an instance of the generated lexer class given the source file, and prints all the token types and values.