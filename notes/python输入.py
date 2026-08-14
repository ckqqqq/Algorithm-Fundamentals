# 这种智能在.py文件中跑
import sys 
for line in sys.stdin:
    a = line.split()
    if len(a)<2:
        print("退出",len(a))
        break
    print(int(a[0]) + int(a[1]))