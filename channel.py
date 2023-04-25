import random

p = 0.1          #prawodpodobieństwo przejścia ze stanu Good do Bad
q = 0.2          # z Bad do Good
alpha = 0.01     # prawdopodobieństwo błędu w G
beta = 0.1       #prawdopodobieństwo błędu w B

def gilbert_eliot_channel(message, p, q, alpha, beta):
    state = 'G'
    out = []
    mesLen = len(message)

    for i in range(mesLen):
        if state == 'G':
            if(random.uniform(0,1)<p):
                state = 'B'
        else:
            if (random.uniform(0, 1) < q):
                state = 'G'
        if state == 'G':
            if(random.uniform(0,1)<alpha):
                out.append(int(not message[i]))
            else:
                out.append((message[i]))
        else:
            if (random.uniform(0, 1) < beta):
                out.append(int(not message[i]))
            else:
                out.append((message[i]))
    return out