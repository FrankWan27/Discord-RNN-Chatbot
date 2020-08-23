import re

traindata = open("traindata.txt", "w", encoding="utf-8")
inputdata = open("input.txt", "r", encoding="utf-8")

for line in inputdata:
    if len(line) > 1:
        if line[0] is not '[':
            line = re.sub(r'^https?:\/\/.*[\r\n]*', '', line)
            line = re.sub(r'^{.*}$', '', line)
            traindata.write(str(line))

traindata.close()
inputdata.close()