import sys
import Obtainer
import Calculator
import glob, os
ready = 0
cmdlist = ('help', 'calculator', 'calc', 'update', 'exit')
while True:
    usercmd2 = input('Please enter a Command:  ')
    usercmd2.lower()
    usercmd2.replace(' ', '')
    if usercmd2 not in cmdlist:
        print('Please enter a valid Command. Enter help to view Commands.')
    if usercmd2 == 'help':
        print(cmdlist)
    if usercmd2 == 'exit':
        sys.exit()
    if usercmd2 == 'update':
        Obtainer.update()
    if usercmd2 == 'calculator':
        while True:
            try:
                with open('done.json') as r:
                    ready = 1
            except FileNotFoundError:
                print('Please run updater before using the calculator.')
                break
            Calculator.calculator()
    if usercmd2 == 'calc':
        while True:
            try:
                with open('done.json') as r:
                    ready = 1
            except FileNotFoundError:
                print('Please run updater before using the calculator.')
                break
            Calculator.calculator()