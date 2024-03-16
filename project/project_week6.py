import sys

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def count(bill_list, bill, total_money):
    for i in bill_list:
            if len(i) != 2:
                print(f"{bcolors.FAIL}The format of a record should be like this: breakfast -50. \nFail to add a record.{bcolors.FAIL}")
                return bill, total_money
            try:
                amount = int(i[1])
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
    if item in cate:
        [print(f"{x[0]} {x[1]}") for x in bill if x[0]==item]
    else:
        print(f"{bcolors.FAIL}There's no record with {item}. Fail to delete a record.{bcolors.RESET}")
        return total_money

    try:
        amount = int(input("Which amount you want to delete: "))
    except:
        print(f"{bcolors.FAIL}{bcolors.RESET}")
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




# input initial money
bill_list = list()
bill = list()
total_money = 0

try:
    total_money = int(input(f'{bcolors.WARNING}How much money do you have?{bcolors.RESET}'))
except:
    print(f"{bcolors.FAIL}Invalid value for money. Set to 0 by default.{bcolors.RESET}\n")

while True:
    command_line = str(input(f"{bcolors.WARNING}(What do you want to do (add / view / delete / exit)?{bcolors.RESET} "))
    if command_line == "exit" :
        break

    elif command_line == "add" :
        print("Add some expense or income records with description and amount:")
        print("desc1 amt1, desc2 amt2, desc3 amt3, ...")
        try:
            bill_list = [ i.split(" ",2) for i in input().split(", ")]
        except:
            print(f"{bcolors.FAIL}The format of a record should be like this: breakfast -50. \nFail to add a record.{bcolors.FAIL}")
        bill, total_money = count(bill_list, bill, total_money)

    elif command_line == "view":
        print("Here's your expense and income records:")
        view(bill)
        if total_money >=0 :
            print(f"Now you have {bcolors.OK}{total_money}{bcolors.RESET} dollars.")
        else: print(f"Now you have {bcolors.FAIL}{total_money}{bcolors.RESET} dollars.")

    elif command_line == "delete":
        total_money = delete(bill,total_money)

    else :
        print(f"{bcolors.FAIL}Invalid command. Try again.{bcolors.RESET}")

    print()

