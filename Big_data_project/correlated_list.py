import json
from pprint import pprint

with open('fullAttrU.json') as f:#reading the full attribute file
    data = json.load(f)
count =15;
with open("correlation.txt", "r") as filestream:# reading correlation file
        for line in filestream:#  reading each line of the correlation.txt file
                currentline = line.split(",")# spliting each line with comma
                third =currentline[2].split("\n")
                out = open("correlated"+str(count)+".csv", 'a')# storing the correlated value in .csv file
                out.write('%s,%s,%s\n' %(json.dumps(currentline[0]),json.dumps(currentline[1]),third[0]))
                for item in data:# iterating through the json data
                        print(item[third[0]])
                        out = open("correlated"+str(count)+".csv", 'a')#creating correlation file for each correlation attribute
                        out.write('%s,%s,%s' %(json.dumps(item[currentline[0]]),json.dumps(item[currentline[1]]),item[third[0]]))# writing it to a file
                        out.write('\n')
                count-=1;
                out.close

