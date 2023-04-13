import queue
import threading
import time
from datetime import datetime

import requests

LINE_CLEAR = '\x1b[2K'

count = 0
valid = 0
invalid = 0
result = []

with open('proxies.txt', 'r') as f:
    proxies = f.read().split()


def clock():
    c_time = datetime.now()
    time_readable = c_time.strftime('%H:%M:%S')

    return time_readable


def check(q, res):
    global count, valid, invalid

    while True:
        try:
            proxy = q.get(timeout=1)
        except queue.Empty:
            break

        try:
            session = requests.Session()
            response = session.get(
                'https://www.twitch.tv/',
                proxies={'https': proxy},
                timeout=5
            )

            if response.status_code == 200:
                count += 1
                valid += 1
                time.sleep(1)
                with open("valid_proxies.txt", 'a') as p:
                    p.write(f'{proxy}\n')
            else:
                pass

        except:
            count += 1
            invalid += 1

        res.append(
            f'{clock()} Proxy ativo! | Acertos {valid} Erros {invalid} | Quantidade: {count}')


q = queue.Queue()
for proxy in proxies:
    q.put(proxy)

for _ in range(len(proxies)):
    t = threading.Thread(target=check, args=(q, result))
    t.daemon = True
    t.start()

while threading.active_count() > 1:
    print(LINE_CLEAR, end='\r')
    for r in result:
        print(r, end='\r')
    time.sleep(1)

print(LINE_CLEAR, end='\r')
print(f'{clock()} Verificação concluída! | Acertos {valid} Erros {invalid} | Quantidade: {count}')
