from filter001 import *
import pandas as ps

#約32分(200~2000)
tick_list = filter1()

def tick_get(tick):
        tick_negative = []
        print(len(tick))
        for i in range(0,len(tick),1):
                tick_negative.append(tick[i][0])
        print(tick_negative)
        print(type(tick_negative))
        return tick_negative
        

#filter2()


with open('tick_list.txt', 'w') as f:
        f.write(str(tick_list))
       
#sa38%222tick_list =filter2()