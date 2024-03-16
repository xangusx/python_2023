def count(total_money):
    print("Add some expense or income records with description and amount:")
    print("desc1 amt1, desc2 amt2, desc3 amt3, ...")
    bill_list = list()
    bill = list()
    temp = tuple()
    bill_list = [ i.split(" ") for i in input().split(", ")]
    for i in bill_list:
        bill.append((str(i[0]),int(i[1])))
    print("Here's your expense and income records:")
    for i in bill:
        print(*i, sep=" ")
        total_money += i[1]
    return total_money

# input initial money
total_money = int(input('How much money do you have?'))
status = True
while status:
    total_money = count(total_money)  
    print(f"Now you have {total_money} dollars.")
    if bool(int(input('continue : 0, close the app : 1\n'))):   
        status = False
