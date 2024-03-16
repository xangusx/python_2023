def trans_char(code):
    table = list()
    while code>26:
        table.append(code%26)
        code = int(code/26)
    table.append(code)
    ans = [chr(64+i) for i in table]
    return ans
        


count = int(input())
ans = list()
for i in range(count):
    ans.append(trans_char(int(input())))

for i,n in enumerate(ans):
    if i!=0:
        print(f'\nCase #{i+1}: ',end='')
    else:
        print(f'Case #{i+1}: ',end='')
    for j in n:
        print(j,end='')
    

