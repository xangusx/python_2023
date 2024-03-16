import sys
import os
import time

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def count(bill, total_money):
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
                return bill, total_money
            try:
                amount = int(i[1])
                try:
                    if amount == 0:
                        raise ValueError(f"{bcolors.FAIL}Amount cannot be zero.{bcolors.RESET}")
                except ValueError as error:
                    print(error)
                    return bill, total_money
            except:
                print(f"{bcolors.FAIL}Invalid value for money.\nFail to add a record.{bcolors.RESET}")
                return bill, total_money
            bill.append((str(i[0]),amount))
            total_money += int(i[1])           
    return bill, total_money

def view(bill):
    print("Description          Amount")
    print("==================== ======")
    for i in bill:
        if i[1] >= 0:
            print(f"{i[0]:20s} {bcolors.OK}{i[1]}{bcolors.RESET}")
        else: print(f"{i[0]:20s} {bcolors.FAIL}{i[1]}{bcolors.RESET}")
    print("==================== ======")


def delete(bill,total_money):
    cate = {x[0] for x in bill}
    if len(cate)==0 :
        print(f"{bcolors.FAIL}Bill is empty! Please add some records.{bcolors.RESET}")
        return total_money

    print("These are the full items of the bill:")
    print("--> ",end="")
    for x in cate:
        print(f"{bcolors.WARNING}{x}{bcolors.RESET} ",end=" ")

    item = input("\nWhich items you want to delete: ")
    try:
        if item not in cate:
            raise ValueError(f"{bcolors.FAIL}There's no record with {item}. Fail to delete a record.{bcolors.RESET}")
        [print(f"{x[0]} {x[1]}") for x in bill if x[0]==item]
    except ValueError as error:
        print(error)
        return total_money

    try:
        amount = int(input("Which amount you want to delete: "))       
    except (ValueError, TypeError):
        print(f"{bcolors.FAIL}Please input the integer{bcolors.RESET}")
        return total_money
    
    status = False
    for index,x in enumerate(bill):
        if x[0]==item and x[1]==amount:
            bill.pop(index)
            total_money -= amount
            status = True
            break
    if status:
        print(f"{bcolors.OK}removed ({item}, {amount}) successfully!{bcolors.RESET}")
    else:
        print(f"{bcolors.FAIL}invaild delete!{bcolors.RESET}")
    return total_money




#initial param
bill = list()
total_money = 0
filename = 'records.txt'

# read the bill file
try:
    with open(filename, 'r') as f:
        try:
            total_money = int(f.readline().strip())
        except:
            print(f"{bcolors.FAIL}initial money is lost!{bcolors.RESET}")
            total_money = int(input(f'{bcolors.WARNING}How much money do you have?{bcolors.RESET}'))
        try:
            bill_list = f.readlines()
            if len(bill_list) == 0 or bill_list[0] == '\n':
                raise ImportError(f"{bcolors.FAIL}file is empty!{bcolors.RESET}")
            for line in bill_list:
                try:
                    val = line.split(",")
                    if int(val[1]) == 0:
                        raise ValueError()
                    bill.append((str(val[0]), int(val[1])))
                except (ValueError,IndexError) :
                    print(f"{bcolors.FAIL}file damage, some accounts may be lost!{bcolors.RESET}")
        except ImportError as error:
            print(error)
        finally:
            f.close()
            print(f"{bcolors.OK}Welcome back!{bcolors.RESET}")
except FileNotFoundError:
    try:
        total_money = int(input(f'{bcolors.WARNING}How much money do you have?{bcolors.RESET}'))
    except:
        print(f"{bcolors.FAIL}Invalid value for money. Set to 0 by default.{bcolors.RESET}\n")

# main function
while True:
    # selete the bill's function
    command_line = str(input(f"{bcolors.WARNING}(What do you want to do (add / view / delete / exit)?{bcolors.RESET} "))
    
    # save the bill
    if command_line == "exit" :
        with open('records.txt','w') as f:
            f.write(str(total_money) + '\n')
            record_str = []
            for record in bill:
                records = ','.join([str(x) for x in record])
                record_str.append(records + '\n')
            f.writelines(record_str)
            f.close()
        print(f"{bcolors.OK}save the bill file{bcolors.RESET}")
        break

    # add
    elif command_line == "add" :
        bill, total_money = count(bill, total_money)

    # view the bill
    elif command_line == "view":
        print("Here's your expense and income records:")
        view(bill)
        if total_money >=0 :
            print(f"Now you have {bcolors.OK}{total_money}{bcolors.RESET} dollars.")
        else: print(f"Now you have {bcolors.FAIL}{total_money}{bcolors.RESET} dollars.")

    # delete the account
    elif command_line == "delete":
        total_money = delete(bill,total_money)

    # deal with the error command
    else :
        print(f"{bcolors.FAIL}Invalid command. Try again.{bcolors.RESET}")

    print()

