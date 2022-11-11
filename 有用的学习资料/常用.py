import queue
import sys

# a=sys.argv[1]
# sys.exit()

q = queue.Queue()
file = open('url.txt')
for x in file.readlines():
    q.put(x.split(',')[0])

while not q.empty():
    url = q.get()

with open('api.txt', 'a') as f:
    f.write(url + '\n')

f1 = open("ip.txt", "r", encoding='utf-8')
for line in f1:
    print(line)
