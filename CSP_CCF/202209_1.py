n,m=[int(i) for i in input().split()]
a_arr=[10086]+[int(a_str) for a_str in input().split()]
c=[1 for _ in range(n+1)]
b=[-1 for _ in range(n+1)]
for i in range(1,n+1):
    c[i]=c[i-1]*a_arr[i]
print(c,a_arr)
sum_=0
for i in range(1,n+1):
    cb=m%c[i]
    cb-=sum_
    b[i]=cb//c[i-1]
    sum_+=cb
print(" ".join(str(b[1:])))
# print(n,m,type(n),a_arr)
