import random
from math import sin, pi

def rand_sample(data_len):
    data = []

    afreq = (random.random() * 9) + 1
    aphase = random.random() * pi
    aamp = (random.random() * 9) + 1
    bfreq = afreq * ((random.random() * 7) + 3)
    bphase = random.random() * pi
    bamp = (random.random() * 9) + 1

    n1sum = 0
    n2sum = 0
    n3sum = 0
    N1 = 10
    N2 = 50
    N3 = 100

    time = 0

    for i in range(data_len):
        n = (aamp * sin((i * afreq) + aphase)) + (bamp * sin((i * bfreq) + bphase))
        tar = 0

        n1sum += n
        n2sum += n
        n3sum += n

        if i >= N1:
            n1sum -= data[i - N1][1]

        if i >= N2:
            n2sum -= data[i - N2][1]

        if i >= N3:
            n3sum -= data[i - N3][1]

        ave1 = (n1sum / N1)
        ave2 = (n2sum / N2)
        ave3 = (n3sum / N3)

        if sin((i * bfreq) + bphase) < -0.8:
            tar = 1
        else:
            tar = 0

        data.append((time, n, tar, ave1, ave2, ave3))

        time += 1

    return data
