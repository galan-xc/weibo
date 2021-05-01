rows = ""
with open("c.txt", "r")as fp:
    rows = fp.readlines()

for row in rows:
    tmp = row.partition(":")
    print('"{}": "{}",'.format(tmp[0].strip(), tmp[2].strip()))


