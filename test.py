def find():
    L = str(input())
    L = L.split(' ')
    n = int(len(L)/2)
    for j in range(n):
        if L[j] != L[len(L)-j-1]:
            return 'no'
    return 'yes'

        
count = int(input())
ans = list()
for i in range(count):
    ans.append(find())

for i, n in enumerate(ans):
    print(f'# case{i}:{n}')


