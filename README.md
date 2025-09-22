This is a simple production calculator for Satisfactory. It requires python to be installed on your computer as well as MySQL. MySQL database must be setup before using the calculator.
In order to connect it to your MySQL database you must modify the login.txt to match your server, database, uid and password.

DRIVER={MySQL ODBC 9.0 ANSI Driver};SERVER=(yourserverhere);DATABASE=(yourDBhere);UID=(yourUIDhere);PWD=(yourpasswordhere)

The main commands are: update, calculator, help, exit, calc
When you launch it, you must first run the updater to fill out the recipe list.
The calculator commands are: list (lists all recipes available), new, delete, listdb (lists recipes in the database), modify, view (shows you your recipe's production values)
I've added help commands in most areas of it, but it's pretty straight forward. You can either use the calculator to see the results, or go into MySQL and see them there.

I've included a bat file that will launch the calculator.
This is my first project, so if there's any bugs please let me know.
