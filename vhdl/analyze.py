#!/usr/bin/env python3
vhdl
""" ****************************************************************************
 * @file        analyze.py
 * @project     Personal

 * @author      Jonathan Hendriks
 * @date        Wed Aug 31 18:46:04 2022
 * @brief       Analyze the VHDL Code to retrieve the entity 

**************************************************************************** """
import sys
import subprocess
import os
import argparse

from pyfzf.pyfzf import FzfPrompt
from datetime import date

from jinja2 import Template

import pyperclip

import re

def test(a,b):
    return a+b

def main() -> int:
    """Echo the input arguments to standard output"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--component', action='store_true')
    parser.add_argument('--map', action='store_true')
    args = parser.parse_args()
    
    folder = os.getcwd() 
    results = [each for each in os.listdir(folder) if each.endswith('.vhd')]
    fzf = FzfPrompt()

    choice = fzf.prompt(results,'--height=40% --layout=reverse --info=inline --border --margin=1 --padding=1 --header-first --header=\'Document Selection:\'')
    choice = choice[0]

    filepath = os.path.join(folder,choice)
    with open(filepath,'r') as fd:
        data = fd.read()
        # print(data)
        # x = re.findall(r"entity (.*?) end.*;",data, flags=re.S)
        x = re.search(r"entity [a-zA-z0-9_-]+ (.*?)end [a-zA-Z0-9_-]+;",data, flags=re.S)
    
    if args.component == True: 
        component = 'component ' + x.group() + 'end component;\n' 
        pyperclip.copy(component)
        print(component)

    if args.map == True: 
        
        # re.findall(r"(?s)(?<=[gG]eneric \()(.*?)(?=\); --End Generic)",x[0], flags=re.S) 

        lines = x.group().split('\n')

        # Firs line
        namepattern = 'entity (.*?) is'
        name = re.findall(namepattern, lines[0])
        name = name[0]

        linepattern = '[a-z]* [a-zA-Z0-9_\-, ]+ : .*;*'
        genpattern='[A-Z0-9_]+ :'

        ppat = '[Pp]ort.+\('
        portpattern='[a-zA-Z0-9_\-, ]+ :'
        
        generics = []
        ports = []
        flg = True
        
        for line in lines:
            # Check which Block section
            if re.findall(ppat,line):
               flg = False; 

            l = re.findall(linepattern, line)
            if l and flg:
                g = re.findall(genpattern,line)
                generics.append(g[0].replace(' :',''))
            elif l and not flg: 
                p = re.findall(portpattern,line)
                replace = [' ',':']
                str1 = p[0]
                for value in replace:
                    str1 = str1.replace(value,'')
                ports.extend(str1.split(','))
        
        ## Create the Map
        genmap = '\n\tgeneric map (\n'
        for g in generics[:-1]:
            genmap = genmap + '\t\t' + g + ' =>  ,\n'
        genmap = genmap + '\t\t' + generics[-1] + ' =>  );\n'


        portmap = '\n\tport map (\n'
        for p in ports[:-1]:
            portmap = portmap + '\t\t' + p + ' =>  ,\n'
        portmap = portmap + '\t\t' + ports[-1] + ' =>  );\n'

        mapping = 'u1 : ' + name + genmap + portmap 
        pyperclip.copy(mapping)
        print(mapping)
               
    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit

