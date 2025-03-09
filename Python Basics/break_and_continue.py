lst = [1,2,3,4,5,6,7,8,9,10]
n = len(lst)
# print the first 5 elements of list
count = 0
while(count < n):
    if(count >= 5):
        break
    print(lst[count])
    count += 1

# skip the 6th element of list
cnt = 0
while(cnt < n):
    if(cnt == 5):
        cnt += 1
        continue
    print(lst[cnt])
    cnt += 1