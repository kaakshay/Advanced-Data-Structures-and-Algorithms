'''
Created on Nov 15, 2014

@author: Akshay Ashwathanarayana
'''
import sys
from numpy import zeros, array, int
INFINITY = sys.maxint

def print_neatly(words, M):
    """ Print text neatly.
    
    Parameters
    ----------
    words: list of str
        Each string in the list is a word from the file. 
    M: int
        The max number of characters per line including spaces
        
    Returns
    -------
    cost: number
        The optimal value as described in the textbook.
    text: str
        The entire text as one string with newline characters. 
        It should not end with a blank line. 
        
    Details
    -------
        Look at print_neatly_test for some code to test the solution.
    """
    
    n = len(words)
    wordCost = zeros((n, n))
    for i in range(n):
        infinityFlag = False
        for j in range(n):
            if not infinityFlag:
                if( i <= j):
                    currentLength = j - i
                    for k in range(i, j+1):
                        currentLength = currentLength + len(words[k])
                    if currentLength > M:
                        wordCost[i, j] = INFINITY
                        infinityFlag = True
                    else:    
                        if j != n-1:    #To remove cost for last line.
                            wordCost[i, j] = (M-currentLength) **3
            else:
                wordCost[i, j] = INFINITY
    
    line = zeros((n+1), dtype=int)
    lineCost = zeros((n+1), dtype=int)
    
    for i in range(1, n+1):
        currentMinimum = INFINITY
        minimumPosition = i
        for j in range(1, i+1):
            if (lineCost[j-1]+ wordCost[j-1, i-1]) < currentMinimum :
                minimumPosition = j-1
                currentMinimum = lineCost[j-1]+ wordCost[j-1, i-1]
        line[i] = minimumPosition
        lineCost[i] = currentMinimum
    
    text = "";
    currentIndex = line[n]
    for i in range(currentIndex, n):
            text = text + words[i];
            if(i != n-1):
                text = text + " "  
    while(currentIndex != 0):
        prevIndex = currentIndex
        currentIndex = line[currentIndex]
        currentLine = ""
        for i in range(currentIndex, prevIndex):
            currentLine = currentLine + words[i];
            if(i != prevIndex-1):
                currentLine = currentLine + " "  
        text = currentLine + str("\n") + text
    print lineCost[n], lineCost[n-1]    
    return lineCost[n], text


def main():
#     arr = array(["Put", "out", "the", "fire", "with", "gasoline"])
    arr = array(["I", "am", "the", "king", "of", "the", "jungle"])
    cost, text = print_neatly(arr, 8)
    print cost
    print text
    
if __name__ == '__main__':
    main()
