import sys
import Obtainer
import Calculator
import json
import pyodbc
import glob, os
import re
import requests
from bs4 import BeautifulSoup
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
        Calculator.calculator()
    if usercmd2 == 'calc':
        Calculator.calculator()