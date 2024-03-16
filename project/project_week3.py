def count(total_money):
    cost_str = input('Add an expense or income record with description and amount:\n')
    cost = cost_str.split(" ",1)
    total_money += int(cost[1])
    # print result
    print('Now you have {} dollars.'.format(total_money))
    return total_money

# input initial money
total_money = int(input('How much money do you have?'))
status = True
while status:
    total_money = count(total_money)  
    if bool(int(input('continue : 0, close the app : 1\n'))):   
        status = False
