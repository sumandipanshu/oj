import re
import checker
def filterit(fileName):
    a=open(fileName,"r")
    pattern=re.compile(r"(import os|subprocess|socket)|(open)|(#include<sys/)|(#include<socket)|(#include<netinet/)|(fstream)")

    code =" ".join(a.readlines())

    print(pattern.findall(code))
    if pattern.search(code)!=None:
        return "unsafe"
    else:
        return "safe"


def check(fileName,timeOut=1):
    if filterit(fileName)=="safe":
        status = checker.codechecker(
            filename=fileName,              # Source code file
            inputfile='input.txt',                  # Input file
            expectedoutput='expected.txt',     # Expected output
            timeout=timeOut,                              # Time limit
            check=True                              # Set to true to check actual output against expected output
        )
        print(status)
        if status[1]==201:
            return "correct",status[1]
        else:
            return "wrong",status[1]
    else:
        return "wrong",403
