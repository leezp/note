import IPy

# c段转成独立ip
f = open('aa', 'r')
lines = f.readlines()
f.close()

with open('bb', 'w') as fopen:
    for line in lines:
        ip = IPy.IP(line)
        for x in ip:
            x1 = str(x)
            fopen.write(x1 + "\n")
print("ok!")
