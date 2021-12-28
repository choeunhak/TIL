#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'solution' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY stockPrices
#  2. INTEGER k
#

def solution(stockPrices, k):
    ans=0
    for i in range(len(stockPrices)-k+1):
        flag=True
        for j in range(k-1):
            if(stockPrices[i+j+1]<=stockPrices[i+j]):
                flag=False
                break
        if(flag==True):
            ans=ans+1
        
    return ans
    # Write your code here

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    stockPrices_count = int(input().strip())

    stockPrices = []

    for _ in range(stockPrices_count):
        stockPrices_item = int(input().strip())
        stockPrices.append(stockPrices_item)

    k = int(input().strip())

    result = solution(stockPrices, k)

    fptr.write(str(result) + '\n')

    fptr.close()
