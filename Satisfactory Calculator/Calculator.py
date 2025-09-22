import sys
import json
import pyodbc
import glob, os
def calculator():
    print('Logging into MySQL Server. . . .')
    cnxn = pyodbc.connect(
        'DRIVER={MySQL ODBC 9.0 ANSI Driver};SERVER=localhost;DATABASE=satisfactory;UID=root;PWD=jDRDsH3j8YB3R8@')
    cursor = cnxn.cursor()
    print('Connection Established.')
    while True:
        while True:
            modding = 0
            clear = 0
            d = dict()
            while True:
                usercmd = input('Input Command:  ')
                usercmd.lower()
                if usercmd == 'help':
                    print('Commands:\nexit\nlist\nhelp\nlistdb\nview\nnew\ndelete\nmodify')
                if usercmd == 'delete':
                    while True:
                        listdb = cursor.tables(tableType='TABLE').fetchall()
                        try:
                            listchecker = listdb[0]
                            counter = 0
                            cleanlist = []
                            for entry in listdb:
                                clean = listdb[counter]
                                cleanlist.append(clean[2])
                                counter = counter + 1
                            print(cleanlist)
                            table_check = input('Input Table to Delete: ').lower()
                            if table_check == 'back':
                                break
                            if table_check == 'exit':
                                sys.exit()
                            if table_check in cleanlist:
                                delcmd = 'DROP TABLE '+ table_check
                                cursor.execute(delcmd)
                                cnxn.commit()
                            if table_check not in cleanlist:
                                print('Enter a Valid Table.')
                        except IndexError:
                            print('Database is Empty.')
                            break
                if usercmd == 'listdb':
                    listdb = cursor.tables(tableType='TABLE').fetchall()
                    try:
                        listchecker = listdb[0]
                        counter = 0
                        for entry in listdb:
                            clean = listdb[counter]
                            print(clean[2])
                            counter = counter + 1
                    except IndexError:
                        print('Database is Empty.')
                if usercmd == 'view':
                    while True:
                        listdb = cursor.tables(tableType='TABLE').fetchall()
                        try:
                            listchecker = listdb[0]
                            counter = 0
                            cleanlist = []
                            for entry in listdb:
                                clean = listdb[counter]
                                cleanlist.append(clean[2])
                                counter = counter + 1
                            print(cleanlist)
                            table_check = input('Input Table to View: ')
                            if table_check == 'back':
                                break
                            if table_check == 'exit':
                                sys.exit()
                            if table_check in cleanlist:
                                getcmd = "SELECT ID, Product, SUM(Machines) AS Machines, SUM(Wattage) AS Wattage,SUM(Output) AS Output FROM "+table_check+" GROUP BY ID, Product HAVING COUNT(*) = 1;"
                                getdict = dict()
                                cursor.execute(getcmd)
                                for row in cursor.fetchall():
                                    getdict['ID'] = row[0]
                                    getdict['Product'] = row[1]
                                    getdict['Machines'] = row[2]
                                    getdict['Wattage'] = row[3]
                                    getdict['Output'] = row[4]
                                    print(getdict)
                                cnxn.commit()
                                break
                            if table_check not in cleanlist:
                                print('Please enter valid table.')
                        except IndexError:
                            print('Database is Empty.')
                            break
                if usercmd == 'exit':
                    sys.exit()
                if usercmd == 'list':
                    for file in glob.glob('*.json'):  # Grabbing File
                        with open(os.path.join(os.getcwd(), file), 'r') as f:
                            print(file.replace('.json', ''))
                if usercmd == 'new':
                    while True:
                        cmds = ('exit.json', 'back.json', 'list.json')
                        product = input('Enter Recipe: ') + '.json'
                        if product == 'exit.json':
                            sys.exit()
                        if product == 'back.json':
                            break
                        if product == 'list.json':
                            for file in glob.glob('*.json'):  # Grabbing File
                                with open(os.path.join(os.getcwd(), file), 'r') as f:
                                    print(file.replace('.json', ''))
                        if product not in cmds:
                            try:
                                with open(product) as read:
                                    d = json.load(read)
                                clear = 1
                                break
                            except FileNotFoundError:
                                print('Try Again.')
                    if clear == 1:
                        break
                if usercmd == 'modify':
                    while True:
                        listdb = cursor.tables(tableType='TABLE').fetchall()
                        modding = 1
                        try:
                            listchecker = listdb[0]
                            counter = 0
                            cleanlist = []
                            for entry in listdb:
                                clean = listdb[counter]
                                cleanlist.append(clean[2])
                                counter = counter + 1
                            print(cleanlist)
                            product = input('Enter Table to Modify: ')
                            if product == 'exit':
                                sys.exit()
                            if product == 'back':
                                break
                            if product == 'list':
                                for file in glob.glob('*.json'):  # Grabbing File
                                    with open(os.path.join(os.getcwd(), file), 'r') as f:
                                        print(file.replace('.json', ''))
                            if product in cleanlist:
                                try:
                                    moddb_var = "SELECT * FROM "+product+" WHERE `key` = 1;"
                                    moddb=cursor.execute(moddb_var).fetchone()
                                    product = moddb[2] + '.json'
                                    with open(product) as read:
                                        d = json.load(read)
                                    clear = 1
                                    break
                                except FileNotFoundError:
                                    print('Try Again.')
                            if product not in cleanlist:
                                print('Enter a Valid Table')
                        except IndexError:
                            print('Database is Empty.')
                            break
                if clear == 1:
                    break
            if 'Raw' in d:
                print("Raw recipes don't need calculation!")
            if 'Raw' not in d:
                break
        while True:
            try:
                out = input("Enter Desired Output: ")
                if out == 'exit':
                    sys.exit()
                out = float(out)
                outmult = out / d['Output']
                if 'Raw' not in d:
                    d['Machines'] = outmult
                    d['Wattage'] = d['Wattage'] * outmult
                break
            except ValueError:
                print("Invalid Input. Please enter a number")
        table = product.replace('.json', '')
        table = table.lower()
        table = table.replace(' ', '')
        table = table.replace('(', '')
        table = table.replace(')', '')
        tcount = 1
        while True:                             #CREATING RECIPE ENTRY IN SQL DB
            if cursor.tables(table=table + 'dirty', tableType='Table').fetchone():  # Makes sure intermediate table is gone
                dirtcmd = 'DROP TABLE ' + table + 'dirty'
                cursor.execute(dirtcmd)
                cnxn.commit()
            if modding == 1:
                drop_table = "DROP TABLE IF EXISTS " + table + ";"
                cursor.execute(drop_table)
                cnxn.commit()
                create_table = 'CREATE TABLE ' + table + "dirty (`key` INT NOT NULL AUTO_INCREMENT, `ID` VARCHAR(255) NULL, `Product` VARCHAR(255) NULL, `Output` FLOAT NULL, `Machines` FLOAT NULL, `Wattage` FLOAT NULL, PRIMARY KEY (`key`));"
                cursor.execute(create_table)
                cnxn.commit()
                break
            if modding != 1:
                if cursor.tables(table=table, tableType='TABLE').fetchone():
                    resp = input('Table already exists. Overwrite? (Y/N)')
                    resp.upper()
                    if resp == 'Y':
                        drop_table = "DROP TABLE IF EXISTS "+table+";"
                        cursor.execute(drop_table)
                        cnxn.commit()
                        create_table = 'CREATE TABLE ' + table + "dirty (`key` INT NOT NULL AUTO_INCREMENT, `ID` VARCHAR(255) NULL, `Product` VARCHAR(255) NULL, `Output` FLOAT NULL, `Machines` FLOAT NULL, `Wattage` FLOAT NULL, PRIMARY KEY (`key`));"
                        cursor.execute(create_table)
                        cnxn.commit()
                        break
                    if resp == 'N':
                        while True:
                            table = table + str(tcount)
                            if cursor.tables(table=table, tableType='TABLE').fetchone():
                                table = table.replace(str(tcount), '')
                                tcount = int(tcount) + 1
                            else:
                                create_table = 'CREATE TABLE ' + table + "dirty (`key` INT NOT NULL AUTO_INCREMENT, `ID` VARCHAR(255) NULL, `Product` VARCHAR(255) NULL, `Output` FLOAT NULL, `Machines` FLOAT NULL, `Wattage` FLOAT NULL, PRIMARY KEY (`key`));"
                                cursor.execute(create_table)
                                cnxn.commit()
                                break
                        break
                    if resp not in ('Y', 'N'):
                        print('Y OR N')
                else:
                    create_table = 'CREATE TABLE '+table+"dirty (`key` INT NOT NULL AUTO_INCREMENT, `ID` VARCHAR(255) NULL, `Product` VARCHAR(255) NULL, `Output` FLOAT NULL, `Machines` FLOAT NULL, `Wattage` FLOAT NULL, PRIMARY KEY (`key`));"
                    cursor.execute(create_table)
                    cnxn.commit()
                    break

        if 'Raw' not in d:  #BASE LAYER
            bld = dict()  #BASE LAYER DICTIONARY
            bld2 = dict() #BASE LAYER SECOND PRODUCT DICTIONARY
            fld = dict()  #FIRST LAYER DICTIONARY
            fld2 = dict() #FIRST LAYER SECOND PRODUCT DICTIONARY
            sld = dict()  #SECOND LAYER DICTIONARY
            sld2 = dict() #SECOND LAYER SECOND PRODUCT DICTIONARY
            tld = dict()  #THIRD LAYER DICTIONARY
            tld2 = dict() #THIRD LAYER SECOND PRODUCT DICTIONARY
            ffld = dict() #FOURTH LAYER DICTIONARY
            ffld2 = dict()#FOURTH LAYER SECOND PRODUCT DICTIONARY
            fffld = dict()#FIFTH LAYER DICTIONARY
            fffld2= dict()#FIFTH LAYER SECOND PRODUCT DICTIONARY
            ssld = dict() #SIXTH LAYER DICTIONARY
            ssld2 = dict()#SIXTH LAYER SECOND PRODUCT DICTIONARY
            count = 1
            sub1 = None
            sub2 = None
            sub3 = None
            sub4 = None
            sub5 = None
            bld['Product'] = d['Product']
            bld['ID'] = d['ID']
            bld['Output'] = out
            bld['Machines'] = bld['Output'] / d['Output']
            bld['Wattage'] = d['Wattage'] * bld['Machines']
            bld['key'] = None
            if 'Product2' in d:
                bld2['Product'] = d['Product2']
                bld2['ID'] = 'BYPRODUCT'
                bld2['Output'] = d['Output2'] * outmult
                bld2['Machines'] = outmult
                bld2['Wattage'] = d['Wattage'] * bld2['Machines']
                bld2['key'] = None
                keys = ['key', 'ID', 'Product', 'Output', 'Machines', 'Wattage']
                values = [bld2.get(ke, None) for ke in keys]
                insertcmd = 'INSERT INTO ' + table + "dirty VALUES (?, ?, ?, ?, ?, ?);"
                cursor.execute(insertcmd, values)
                cnxn.commit()
            keys = ['key', 'ID', 'Product', 'Output', 'Machines', 'Wattage']
            values = [bld.get(ke, None) for ke in keys]
            insertcmd = 'INSERT INTO ' + table + "dirty VALUES (?, ?, ?, ?, ?, ?);"
            cursor.execute(insertcmd, values)
            cnxn.commit()
            print(bld['Product'], ' Entered into DB.')
            while True:         #FIRST LAYER
                first_layer = "Ingredient" + str(count)
                first_input = 'Input' + str(count)
                try:
                    ing1 = d[first_layer] +'.json'
                except KeyError:
                    break
                with open(ing1) as read:
                    ing1 = json.load(read)
                if 'Raw' not in ing1:
                    fld['Product'] = ing1['Product']
                    fld['ID'] = ing1['ID']
                    fld['Output'] = d[first_input] * outmult
                    fld['Machines'] = fld['Output'] / ing1['Output']
                    fld['Wattage'] = ing1['Wattage'] * fld['Machines']
                    fld['key'] = None
                    keys = ['key', 'ID', 'Product', 'Output', 'Machines', 'Wattage']
                    values = [fld.get(ke, None) for ke in keys]
                    insertcmd = 'INSERT INTO ' + table + "dirty VALUES (?, ?, ?, ?, ?, ?);"
                    cursor.execute(insertcmd, values)
                    cnxn.commit()
                    print(fld['Product'], ' Entered into DB.')
                if 'Product2' in ing1:
                    fld2['Product'] = ing1['Product2']
                    fld2['ID'] = 'BYPRODUCT'
                    fld2['Output'] =  ing1['Output2'] * outmult
                    fld2['Machines'] = fld2['Output'] / ing1['Output2']
                    fld2['Wattage'] = ing1['Wattage'] * fld2['Machines']
                    fld2['key'] = None
                    keys = ['key', 'ID', 'Product', 'Output', 'Machines', 'Wattage']
                    values = [fld2.get(ke, None) for ke in keys]
                    insertcmd = 'INSERT INTO ' + table + "dirty VALUES (?, ?, ?, ?, ?, ?);"
                    cursor.execute(insertcmd, values)
                    cnxn.commit()
                count = count + 1
                count2 = 1
                if 'Raw' not in ing1:
                    while True:         #SECOND LAYER
                        second_layer = 'Ingredient' +str(count2)
                        second_input = 'Input' + str(count2)
                        try:
                            sub1 = ing1[second_layer] + '.json'
                        except KeyError:
                            break
                        with open(sub1) as read:
                            sub1 = json.load(read)
                        if 'Product2' in sub1:
                            sld2['Product'] = sub1['Product2']
                            sld2['ID'] = 'BYPRODUCT'
                            sld2['Output'] = sub1['Output2'] * fld['Machines']
                            sld2['Machines'] = 1
                            sld2['Wattage'] = 1
                            sld2['key'] = None
                            values = [sld2.get(ke, None) for ke in keys]
                            cursor.execute(insertcmd, values)
                            cnxn.commit()
                            print(sld['Product'], ' Entered into DB.')
                        if 'Raw' in sub1:
                            sld['Product'] = sub1['Product']
                            sld['ID'] = sub1['ID']
                            sld['Output'] = ing1[second_input] * fld['Machines']
                            sld['Machines'] = 1
                            sld['Wattage'] = 5
                            sld['key'] = None
                            values = [sld.get(ke, None) for ke in keys]
                            cursor.execute(insertcmd, values)
                            cnxn.commit()
                            print(sld['Product'], ' Entered into DB.')
                        if 'Raw' not in sub1:
                            sld['Product'] = sub1['Product']
                            sld['ID'] = sub1['ID']
                            sld['Output'] = ing1[second_input] * fld['Machines']
                            sld['Machines'] = sld['Output'] / sub1['Output']
                            sld['Wattage'] = sub1['Wattage'] * sld['Machines']
                            sld['key'] = None
                            values = [sld.get(ke, None) for ke in keys]
                            cursor.execute(insertcmd, values)
                            cnxn.commit()
                            print(sld['Product'], ' Entered into DB.')
                        count2 = count2 + 1
                        count3 = 1
                        if 'Raw' not in sub1:
                            while True:         #THIRD LAYER
                                third_layer = 'Ingredient' + str(count3)
                                third_input = 'Input' + str(count3)
                                try:
                                    sub2 = sub1[third_layer] + '.json'
                                except KeyError:
                                    break
                                with open(sub2) as read:
                                    sub2 = json.load(read)
                                if 'Product2' in sub2:
                                    tld2['Product'] = sub2['Product2']
                                    tld2['ID'] = 'BYPRODUCT'
                                    tld2['Output'] = sub2['Output2'] * sld['Machines']
                                    tld2['Machines'] = 1
                                    tld2['Wattage'] = 1
                                    tld2['key'] = None
                                    values = [tld2.get(ke, None) for ke in keys]
                                    cursor.execute(insertcmd, values)
                                    cnxn.commit()
                                    print(tld2['Product'], ' Entered into DB.')
                                if 'Raw' in sub2:
                                    tld['Product'] = sub2['Product']
                                    tld['ID'] = sub2['ID']
                                    tld['Output'] = sub1[third_input] * sld['Machines']
                                    tld['Machines'] = 1
                                    tld['Wattage'] = 5
                                    tld['key'] = None
                                    values = [tld.get(ke, None) for ke in keys]
                                    cursor.execute(insertcmd, values)
                                    cnxn.commit()
                                    print(tld['Product'], ' Entered into DB.')
                                if 'Raw' not in sub2:
                                    tld['Product'] = sub2['Product']
                                    tld['ID'] = sub2['ID']
                                    tld['Output'] = sub1[third_input] * sld['Machines']
                                    tld['Machines'] = tld['Output'] / sub2['Output']
                                    tld['Wattage'] = sub2['Wattage'] * tld['Machines']
                                    tld['key'] = None
                                    values = [tld.get(ke, None) for ke in keys]
                                    cursor.execute(insertcmd, values)
                                    cnxn.commit()
                                    print(tld['Product'], ' Entered into DB.')
                                count3 = count3 + 1
                                count4 = 1
                                if 'Raw' not in sub2:
                                    while True:  #FOURTH LAYER
                                        fourth_layer = 'Ingredient' + str(count4)
                                        fourth_input = 'Input' + str(count4)
                                        try:
                                            sub3 = sub2[fourth_layer] + '.json'
                                        except KeyError:
                                            break
                                        with open(sub3) as read:
                                            sub3 = json.load(read)
                                        if 'Product2' in sub3:
                                            ffld2['Product'] = sub3['Product2']
                                            ffld2['ID'] = 'BYPRODUCT'
                                            ffld2['Output'] = sub3['Output2'] * tld['Machines']
                                            ffld2['Machines'] = 1
                                            ffld2['Wattage'] = 1
                                            ffld2['key'] = None
                                            values = [ffld2.get(ke, None) for ke in keys]
                                            cursor.execute(insertcmd, values)
                                            cnxn.commit()
                                            print(ffld2['Product'], ' Entered into DB.')
                                        if 'Raw' in sub3:
                                            ffld['Product'] = sub3['Product']
                                            ffld['ID'] = sub3['ID']
                                            ffld['Output'] = sub2[fourth_input] * tld['Machines']
                                            ffld['Machines'] = 1
                                            ffld['Wattage'] = 5
                                            ffld['key'] = None
                                            values = [ffld.get(ke, None) for ke in keys]
                                            cursor.execute(insertcmd, values)
                                            cnxn.commit()
                                            print(ffld['Product'], ' Entered into DB.')
                                        if 'Raw' not in sub3:
                                            ffld['Product'] = sub3['Product']
                                            ffld['ID'] = sub3['ID']
                                            ffld['Output'] = sub2[fourth_input] * tld['Machines']
                                            ffld['Machines'] = ffld['Output'] / sub3['Output']
                                            ffld['Wattage'] = sub3['Wattage'] * ffld['Machines']
                                            ffld['key'] = None
                                            values = [ffld.get(ke, None) for ke in keys]
                                            cursor.execute(insertcmd, values)
                                            cnxn.commit()
                                            print(ffld['Product'], ' Entered into DB.')
                                        count4 = count4 + 1
                                        count5 = 1
                                        if 'Raw' not in sub3:
                                            while True:     #FIFTH LAYER
                                                fifth_layer = 'Ingredient' + str(count5)
                                                fifth_input = 'Input' + str(count5)
                                                try:
                                                    sub4 = sub3[fifth_layer] + '.json'
                                                except KeyError:
                                                    break
                                                with open(sub4) as read:
                                                    sub4 = json.load(read)
                                                if 'Product2' in sub4:
                                                    fffld2['Product'] = sub4['Product2']
                                                    fffld2['ID'] = 'BYPRODUCT'
                                                    fffld2['Output'] = sub4['Output2'] * ffld['Machines']
                                                    fffld2['Machines'] = 1
                                                    fffld2['Wattage'] = 1
                                                    fffld2['key'] = None
                                                    values = [fffld2.get(ke, None) for ke in keys]
                                                    cursor.execute(insertcmd, values)
                                                    cnxn.commit()
                                                    print(fffld2['Product'], ' Entered into DB.')
                                                if 'Raw' in sub4:
                                                    fffld['Product'] = sub4['Product']
                                                    fffld['ID'] = sub4['ID']
                                                    fffld['Output'] = sub3[fifth_input] * ffld['Machines']
                                                    fffld['Machines'] = 1
                                                    fffld['Wattage'] = 5
                                                    fffld['key'] = None
                                                    values = [fffld.get(ke, None) for ke in keys]
                                                    cursor.execute(insertcmd, values)
                                                    cnxn.commit()
                                                    print(fffld['Product'], ' Entered into DB.')
                                                if 'Raw' not in sub4:
                                                    fffld['Product'] = sub4['Product']
                                                    fffld['ID'] = sub4['ID']
                                                    fffld['Output'] = sub3[fifth_input] * ffld['Machines']
                                                    fffld['Machines'] = fffld['Output'] / sub4['Output']
                                                    fffld['Wattage'] = sub4['Wattage'] * fffld['Machines']
                                                    fffld['key'] = None
                                                    values = [fffld.get(ke, None) for ke in keys]
                                                    cursor.execute(insertcmd, values)
                                                    cnxn.commit()
                                                    print(fffld['Product'], ' Entered into DB.')
                                                count5 = count5 + 1
                                                count6 = 1
                                                if 'Raw' not in sub4:
                                                    while True:     #SIXTH LAYER
                                                        sixth_layer = 'Ingredient' + str(count6)
                                                        sixth_input = 'Input' + str(count6)
                                                        try:
                                                            sub5 = sub4[sixth_layer] + '.json'
                                                        except KeyError:
                                                            break
                                                        with open(sub5) as read:
                                                            sub5 = json.load(read)
                                                        if 'Product2' in sub5:
                                                            ssld2['Product'] = sub5['Product2']
                                                            ssld2['ID'] = 'BYPRODUCT'
                                                            ssld2['Output'] = sub5['Output2'] * fffld['Machines']
                                                            ssld2['Machines'] = 1
                                                            ssld2['Wattage'] = 1
                                                            ssld2['key'] = None
                                                            values = [ssld2.get(ke, None) for ke in keys]
                                                            cursor.execute(insertcmd, values)
                                                            cnxn.commit()
                                                            print(ssld2['Product'], ' Entered into DB.')
                                                        if 'Raw' in sub5:
                                                            ssld['Product'] = sub5['Product']
                                                            ssld['ID'] = sub5['ID']
                                                            ssld['Output'] = sub4[sixth_input] * fffld['Machines']
                                                            ssld['Machines'] = 1
                                                            ssld['Wattage'] = 5
                                                            ssld['key'] = None
                                                            values = [ssld.get(ke, None) for ke in keys]
                                                            cursor.execute(insertcmd, values)
                                                            cnxn.commit()
                                                            print(ssld['Product'], ' Entered into DB.')
                                                        if 'Raw' not in sub5:
                                                            ssld['Product'] = sub5['Product']
                                                            ssld['ID'] = sub5['ID']
                                                            ssld['Output'] = sub4[sixth_input] * fffld['Machines']
                                                            ssld['Machines'] = ssld['Output'] / sub5['Output']
                                                            ssld['Wattage'] = sub5['Wattage'] * ssld['Machines']
                                                            ssld['key'] = None
                                                            values = [ssld.get(ke, None) for ke in keys]
                                                            cursor.execute(insertcmd, values)
                                                            cnxn.commit()
                                                            print(ssld['Product'], ' Entered into DB.')
                                                        count6 = count6 + 1
            #CleanUp
            newcmd = "SELECT ID, Product, SUM(Machines) AS Machines, SUM(Wattage) AS Wattage,SUM(Output) AS Output FROM "+table+"dirty GROUP BY ID, Product HAVING COUNT(*) = 1;"
            newcmd2 = "SELECT ID, Product, SUM(Machines) AS Machines, SUM(Wattage) AS Wattage,SUM(Output) AS Output FROM "+table+"dirty GROUP BY ID, Product HAVING COUNT(*) > 1;"
            neatdict = dict()
            neatdict['key'] = None
            neatdict['ID'] = None
            neatdict['Product'] = None
            neatdict['Machines'] = None
            neatdict['Wattage'] = None
            neatdict['Output'] = None
            create_table = 'CREATE TABLE '+table+"(`key` INT NOT NULL AUTO_INCREMENT, `ID` VARCHAR(255) NULL, `Product` VARCHAR(255) NULL, `Output` FLOAT NULL, `Machines` FLOAT NULL, `Wattage` FLOAT NULL, PRIMARY KEY (`key`));"
            cursor.execute(create_table)
            cnxn.commit()
            cursor.execute(newcmd)
            for row in cursor.fetchall():
                neatdict['ID'] = row[0]
                neatdict['Product'] = row[1]
                neatdict['Machines'] = row[2]
                neatdict['Wattage'] = row[3]
                neatdict['Output'] = row[4]
                keys = ['key', 'ID', 'Product', 'Output', 'Machines', 'Wattage']
                values = [neatdict.get(ke, None) for ke in keys]
                insertcmd = 'INSERT INTO '+table+" VALUES (?, ?, ?, ?, ?, ?);"
                cursor.execute(insertcmd, values)
                cnxn.commit()
            cursor.execute(newcmd2)
            for row in cursor.fetchall():
                neatdict['ID'] = row[0]
                neatdict['Product'] = row[1]
                neatdict['Machines'] = row[2]
                neatdict['Wattage'] = row[3]
                neatdict['Output'] = row[4]
                keys = ['key', 'ID', 'Product', 'Output', 'Machines', 'Wattage']
                values = [neatdict.get(ke, None) for ke in keys]
                insertcmd = 'INSERT INTO '+table+" VALUES (?, ?, ?, ?, ?, ?);"
                cursor.execute(insertcmd, values)
                cnxn.commit()
            cursor.execute('DROP TABLE '+table+'dirty')