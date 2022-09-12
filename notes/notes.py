#!/usr/bin/env python3
""" ****************************************************************************
 * @file        notes.py
 * @project     Personal

 * @author      Jonathan Hendriks
 * @date        Wed Aug 31 18:46:04 2022
 * @brief       Note taking for General Todo, Project (Meeting, Notebook, todo) following the todo.txt 

**************************************************************************** """
import sys
import subprocess
import os
import argparse

from pyfzf.pyfzf import FzfPrompt
from datetime import date

from jinja2 import Template

def notebook(path,project=''):
    tit = input('Enter Title of Notebook :\n')
    filename = tit.replace(" ","_") + '.md'
    filepath = os.path.join(path,filename)
    if not os.path.exists(filepath):
        txt ="""
---
title: {{ title }}
project: {{ prj }}
author: {{ user }}
date: {{ date }}
...

# {{ title }}
"""
        tm = Template(txt)
        data = tm.render(prj=project,user=os.environ['USER'],date=date.today().strftime('%Y-%m-%d'),title=tit)
        os.makedirs(os.path.join(os.path.dirname(filepath)),exist_ok=True)
        with open(filepath,'w') as fd:
           fd.write(data)
    return filepath

def meeting(path,project=''):
    filename = project + '_' + date.today().strftime('%Y-%m-%d') + '.md'
    filepath = os.path.join(path,filename)
    if not os.path.exists(filepath):
        txt = """
---
title: Meeting_{{ date }}_{{ prj }}
project: {{ prj }}
author: {{ user }}
date: {{ date }}
...

# Meeting : {{ date }}
"""
        tm = Template(txt)
        data = tm.render(prj=project,user=os.environ['USER'],date=date.today().strftime('%Y-%m-%d'))
        os.makedirs(os.path.join(os.path.dirname(filepath)),exist_ok=True)
        with open(filepath,'w') as fd:
            fd.write(data)
    return filepath

def QandA(path,project=''):
    filename = 'QA_' + date.today().strftime('%Y-%m-%d') + '.md'
    filepath = os.path.join(path,filename)
    if not os.path.exists(filepath):
        txt = """
---
title: QA_{{ date }}_{{ prj }}
project: {{ prj }}
author: {{ user }}
date: {{ date }}
...

"""
        tm = Template(txt)
        data = tm.render(prj=project,user=os.environ['USER'],date=date.today().strftime('%Y-%m-%d'))
        os.makedirs(os.path.join(os.path.dirname(filepath)),exist_ok=True)
        with open(filepath,'w') as fd:
            fd.write(data)
    return filepath
            
def todo(filepath,project=''):
    if not os.path.exists(filepath):
        txt = """
████████╗ ██████╗ ██████╗  ██████╗   |
╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗  |
   ██║   ██║   ██║██║  ██║██║   ██║  |
   ██║   ██║   ██║██║  ██║██║   ██║  |
   ██║   ╚██████╔╝██████╔╝╚██████╔╝  |
   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝   |    {{ prj }}
________________________________________________________________
 
"""
                                   
        tm = Template(txt)
        data = tm.render(prj=project)
        os.makedirs(os.path.join(os.path.dirname(filepath)),exist_ok=True)
        with open(filepath,'w') as fd:
            fd.write(data)
    return filepath


def main() -> int:
    """Echo the input arguments to standard output"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    
    if args.t == True: 
        # TodoPath = "/home/hej/perso/stowfiles/notes/.notes/test.txt"
        TodoPath = os.path.join(os.environ["HOMENOTES"], "todo.md")

        todo(TodoPath)
        subprocess.run(["nvim",'+','-c "norm 0"','-c "startinsert"', TodoPath])
        # vim.command('FloatermNew nvim /home/hej/perso/stowfiles/notes/test.txt')
        # nvim = attach('child',argv=["/bin/env", "nvim", "/home/hej/perso/stowfiles/notes/test.txt"])
        # vim.command('echo "hello world"')
    else :
        # TEST
        # os.environ['HOMENOTES'] = '/home/hej/perso/stowfiles/notes/testprojet'
        # os.environ['HOMENOTES'] = '/home/hej/perso/stowfiles/notes/.notes'
        # ----
        # print(os.environ['HOMENOTES'])
        # print(os.environ['HOMENOTES'])

        # Selection Project, fuzzy finder pop up
        # projects = os.listdir(os.environ['HOMENOTES'])
        lprojects = [d for d in os.listdir(os.environ['HOMENOTES']) if os.path.isdir(os.path.join(os.environ['HOMENOTES'],d))]
        projects = [d for d in lprojects if ".obsidian" not in d]
        
        fzf = FzfPrompt()
        project = fzf.prompt(projects,'--height=40% --layout=reverse --info=inline --border --margin=1 --padding=1 --header-first --header=\'Project Selection:\'')
        project = project[0]

        # Selection Notebook, Todo or Meeting
        l = ['Notebook','Q&A', 'Meeting', 'Todo']
        choice = fzf.prompt(l,'--height=40% --layout=reverse --info=inline --border --margin=1 --padding=1 --header-first --header=\'Document Selection:\'')
        choice = choice[0]

        if choice == 'Notebook':

            ## Notebook N or list
            NotebookPath = os.path.join(os.environ['HOMENOTES'],project,'notebook')
            notebooks = ['New']
            try:
                notebooks.extend([f for f in os.listdir(NotebookPath) if os.path.isfile(os.path.join(NotebookPath, f))])
            except FileNotFoundError:
                os.makedirs(NotebookPath)
            except :
                raise ValueError('A very specific bad thing happened.')
            file = fzf.prompt(notebooks,'--height=40% --layout=reverse --info=inline --border --margin=1 --padding=1 --header-first --header=\'Notebook Selection:\'')
            filename = file[0] 
            if filename == 'New':
                filepath = notebook(NotebookPath,project)
            else:
                filepath = os.path.join(NotebookPath,filename)
            
            subprocess.run(["nvim",'+','-c "norm 0"','-c "startinsert"', filepath])

        elif choice == 'Meeting': 
            ## Meeting N or list (saved by date)
            MeetingPath = os.path.join(os.environ['HOMENOTES'],project,'meeting')
            meetings = ['New']
            try:
                meetings.extend([f for f in os.listdir(MeetingPath) if os.path.isfile(os.path.join(MeetingPath, f))])
            except FileNotFoundError:
                os.makedirs(MeetingPath)
            except :
                raise ValueError('A very specific bad thing happened.')

            file = fzf.prompt(meetings,'--height=40% --layout=reverse --info=inline --border --margin=1 --padding=1 --header-first --header=\'Meeting Selection:\'')
            filename = file[0] 
            if filename == 'New':
                filepath = meeting(MeetingPath,project)
            else:
                filepath = os.path.join(MeetingPath,filename)

            ## NVIM the file
            subprocess.run(["nvim",'+','-c "norm 0"','-c "startinsert"', filepath])

        elif choice == 'Q&A': 
            ## QA N or list (saved by date)
            QAPath = os.path.join(os.environ['HOMENOTES'],project,'QA')
            qa = ['New']
            try:
                qa.extend([f for f in os.listdir(QAPath) if os.path.isfile(os.path.join(QAPath, f))])
            except FileNotFoundError:
                os.makedirs(QAPath)
            except :
                raise ValueError('A very specific bad thing happened.')

            file = fzf.prompt(qa,'--height=40% --layout=reverse --info=inline --border --margin=1 --padding=1 --header-first --header=\'Q&A Selection:\'')
            filename = file[0] 
            if filename == 'New':
                filepath = QandA(QAPath,project)
            else:
                filepath = os.path.join(QAPath,filename)

            ## NVIM the file
            subprocess.run(["nvim",'+','-c "norm 0"','-c "startinsert"', filepath])
        elif choice == 'Todo':
            ## Todo for the project
            TodoPath = os.path.join(os.environ['HOMENOTES'],project,'todo.txt')
            todo(TodoPath,project)
            subprocess.run(["nvim",'+','-c "norm 0"','-c "startinsert"', TodoPath])
            ## NVIM the file
        else :
            print('Oups')


    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit

