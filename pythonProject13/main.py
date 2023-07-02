number_of_tabun = int(input())
f = []
temp = []
for i in range(number_of_tabun):
    m = list(input())
    temp.append(m)
    f.append([999, m])

for i in range(number_of_tabun):
    for j in range(number_of_tabun):
        if temp[i] not in f[j]:
            yrodstvo = max(f[j][1].count('a') + temp[i][1].count('a'), f[j][1].count('b') + temp[i][1].count('b'),
                           f[j][1].count('c') + temp[i][1].count('c')) - min(f[j][1].count('a') + temp[i][1].count('a'), f[j][1].count('b') + temp[i][1].count('b'),
                           f[j][1].count('c') + temp[i][1].count('c'))
            if yrodstvo < f[j][0]:
                f[j][0] = yrodstvo
                f[j].append(temp[i])

print(f)

