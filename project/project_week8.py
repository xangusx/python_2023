#/usr/bin/python
import sys
import os
import time

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def add(initial_money, records):
    bill_list = list()
    print("Add some expense or income records with description and amount:")
    print("desc1 amt1, desc2 amt2, desc3 amt3, ...")
    try:
        bill_list = [ i.split(" ") for i in input().split(", ")]
    except:
        print(f"{bcolors.FAIL}The format of a record should be like this: breakfast -50. \nFail to add a record.{bcolors.FAIL}")

    for i in bill_list:
            if len(i) != 2:
                print(f"{bcolors.FAIL}The format of a record should be like this: breakfast -50. \nFail to add a record.{bcolors.RESET}")
                return initial_money, records
            try:
                amount = int(i[1])
                try:
                    if amount == 0:
                        raise ValueError(f"{bcolors.FAIL}Amount cannot be zero.{bcolors.RESET}")
                except ValueError as error:
                    print(error)
                    return initial_money, records
            except:
                print(f"{bcolors.FAIL}Invalid value for money.\nFail to add a record.{bcolors.RESET}")
                return initial_money, records
            records.append((str(i[0]),amount))
            initial_money += int(i[1])           
    return initial_money, records
def view(initial_money, records):
    print("Here's your expense and income records:")
    print("Description          Amount")
    print("==================== ======")
    for i in records:
        if i[1] >= 0:
            print(f"{i[0]:20s} {bcolors.OK}{i[1]}{bcolors.RESET}")
        else: print(f"{i[0]:20s} {bcolors.FAIL}{i[1]}{bcolors.RESET}")
    print("==================== ======")
    if initial_money >=0 :
        print(f"Now you have {bcolors.OK}{initial_money}{bcolors.RESET} dollars.")
    else: 
        print(f"Now you have {bcolors.FAIL}{initial_money}{bcolors.RESET} dollars.")
    return initial_money, records
def delete(initial_money, records):
    cate = {x[0] for x in records}
    if len(cate)==0 :
        print(f"{bcolors.FAIL}Bill is empty! Please add some records.{bcolors.RESET}")
        return initial_money, records

    print("These are the full items of the records:")
    print("--> ",end="")
    for x in cate:
        print(f"{bcolors.WARNING}{x}{bcolors.RESET} ",end=" ")

    item = input("\nWhich items you want to delete: ")
    try:
        if item not in cate:
            raise ValueError(f"{bcolors.FAIL}There's no record with {item}. Fail to delete a record.{bcolors.RESET}")
        [print(f"{x[0]} {x[1]}") for x in records if x[0]==item]
    except ValueError as error:
        print(error)
        return initial_money, records

    try:
        amount = int(input("Which amount you want to delete: "))       
    except (ValueError, TypeError):
        print(f"{bcolors.FAIL}Please input the integer{bcolors.RESET}")
        return initial_money, records
    
    status = False
    for index,x in enumerate(records):
        if x[0]==item and x[1]==amount:
            records.pop(index)
            initial_money -= amount
            status = True
            break
    if status:
        print(f"{bcolors.OK}removed ({item}, {amount}) successfully!{bcolors.RESET}")
    else:
        print(f"{bcolors.FAIL}invaild delete!{bcolors.RESET}")
    return initial_money, records
#initial param
def initialize():
    records = list()
    initial_money = 0
    filename = 'records.txt'
    # read the records file
    try:
        with open(filename, 'r') as f:
            try:
                initial_money = int(f.readline().strip())
            except:
                print(f"{bcolors.FAIL}initial money is lost!{bcolors.RESET}")
                initial_money = int(input(f'{bcolors.WARNING}How much money do you have?{bcolors.RESET}'))
                return initial_money, records
            try:
                bill_list = f.readlines()
                if len(bill_list) == 0 or bill_list[0] == '\n':
                    raise ImportError(f"{bcolors.FAIL}file is empty!{bcolors.RESET}")
                for line in bill_list:
                    try:
                        val = line.split(",")
                        if int(val[1]) == 0:
                            raise ValueError()
                        records.append((str(val[0]), int(val[1])))
                    except (ValueError,IndexError) :
                        print(f"{bcolors.FAIL}file damage, some accounts may be lost!{bcolors.RESET}")
                        return initial_money, records
            except ImportError as error:
                print(error)
            finally:
                f.close()
                print(f"{bcolors.OK}Welcome back!{bcolors.RESET}")
                return initial_money, records
    except FileNotFoundError:
        try:
            initial_money = int(input(f'{bcolors.WARNING}How much money do you have?{bcolors.RESET}'))
        except:
            print(f"{bcolors.FAIL}Invalid value for money. Set to 0 by default.{bcolors.RESET}\n")
            return initial_money, records
    return initial_money, records
def save(initial_money, records):
    with open('records.txt','w') as f:
        f.write(str(initial_money) + '\n')
        record_str = []
        for record in records:
            record_single = ','.join([str(x) for x in record])
            record_str.append(record_single + '\n')
        f.writelines(record_str)
        f.close()
    print(f"{bcolors.OK}save the records file{bcolors.RESET}")

# main function
initial_money, records = initialize()
while True:
    # selete the records's function
    command_line = str(input(f"{bcolors.WARNING}(What do you want to do (add / view / delete / exit)?{bcolors.RESET} "))
    
    # save the records
    if command_line == "exit" :
        save(initial_money, records)
        break

    # add
    elif command_line == "add" :
        initial_money, records = add(initial_money, records)

    # view the records
    elif command_line == "view":
        initial_money, records = view(initial_money, records)

    # delete the account
    elif command_line == "delete":
        initial_money, records = delete(initial_money, records)

    # deal with the error command
    else :
        print(f"{bcolors.FAIL}Invalid command. Try again.{bcolors.RESET}")

    print()

