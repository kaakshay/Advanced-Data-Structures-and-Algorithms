# -*- coding: utf-8 -*-
'''
Created on Sep 14, 2014

@author: Akshay Ashwathanarayana
'''
from numpy import asarray, zeros  # analysis:ignore

# STOCK_PRICES  = [100,113,110,85,105,102,86,63,81,101,94,106,101,79,94,90,97]
STOCK_PRICE_CHANGES = [
    13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]


# Implement pseudocode from the book
def find_maximum_subarray_brute(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Implement the brute force method from chapter 4
    time complexity = O(n^2)

    >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES)
    (7, 10)
    >>> find_maximum_subarray_brute([1, 2, 3, 4, 5, 6])
    (0, 5)
    >>> find_maximum_subarray_brute([1, -1, -2, -3, -4, -5])
    (0, 0)
    """
    n = len(A)
    maximumSubArray = -float("inf")
    iIndex = jIndex = 0
    for i in range(n):
        currentSum = 0
        for j in range(i, n):
            currentSum += A[j]
            if(currentSum > maximumSubArray):
                maximumSubArray = currentSum
                iIndex = i
                jIndex = j
    return (iIndex, jIndex)


# Implement pseudocode from the book
def find_maximum_crossing_subarray(A, low, mid,  high):
    """
    Find the maximum subarray that crosses mid
    Return a tuple (i,j) where A[i:j] is the maximum subarray.

    >>> find_maximum_subarray_brute(STOCK_PRICE_CHANGES)
    (7, 10)
    """
    leftSum = -float("inf")
    currentSum = 0
    iIndex = jIndex = mid
    for i in range(mid, low - 1, -1):
        currentSum += A[i]
        if(currentSum > leftSum):
            leftSum = currentSum
            iIndex = i
    rightSum = -float("inf")
    currentSum = 0
    for i in range(mid + 1, high + 1):
        currentSum += A[i]
        if(currentSum > rightSum):
            rightSum = currentSum
            jIndex = i
    return (iIndex, jIndex)


def find_maximum_subarray_recursive(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Recursive method from chapter 4
    >>> find_maximum_subarray_recursive(STOCK_PRICE_CHANGES)
    (7, 10)
    >>> find_maximum_subarray_recursive([1, 2, 3, 4, 5, 6])
    (0, 5)
    >>> find_maximum_subarray_recursive([1, -1, -2, -3, -4, -5])
    (0, 0)
    """
    if(high == -1):
        high = len(A) - 1
    if (high == low):
        return (low, high)
    mid = (int)(high + low) / 2
    (leftIIndex, leftJIndex) = find_maximum_subarray_recursive(A, low, mid)
    (rightIIndex, rightJIndex) = find_maximum_subarray_recursive(
        A, mid + 1, high)
    (crossIIndex, crossJIndex) = find_maximum_crossing_subarray(
        A, low, mid, high)
    leftSum = sum(A[leftIIndex:leftJIndex + 1])
    rightSum = sum(A[rightIIndex:rightJIndex + 1])
    crossSum = sum(A[crossIIndex:crossJIndex + 1])
    if(leftSum >= rightSum and leftSum >= crossSum):
        return (leftIIndex, leftJIndex)
    elif(rightSum >= leftSum and rightSum >= crossSum):
        return (rightIIndex, rightJIndex)
    else:
        return (crossIIndex, crossJIndex)


def find_maximum_subarray_iterative(A, low=0, high=-1):
    """
    Return a tuple (i,j) where A[i:j] is the maximum subarray.
    Do problem 4.1-5 from the book.
    >>> find_maximum_subarray_iterative(STOCK_PRICE_CHANGES)
    (7, 10)
    >>> find_maximum_subarray_iterative([1, 2, 3, 4, 5, 6])
    (0, 5)
    >>> find_maximum_subarray_iterative([1, -1, -2, -3, -4, -5])
    (0, 0)
    """
    maximumSubArraySum = currentMaximum = currentMaxIIndex = 0
    maxIIndex = maxJIndex = 0
    for i in range(len(A)):
        currentMaximum += A[i]
        if(currentMaximum < 0):
            currentMaximum = 0
            currentMaxIIndex = i+1
        if(maximumSubArraySum < currentMaximum):
            maximumSubArraySum = currentMaximum
            maxJIndex = i
            maxIIndex = currentMaxIIndex
    return (maxIIndex, maxJIndex)


def square_matrix_multiply(A, B):
    """
    Return the product AB of matrix multiplication.
    >>> A = ([1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16])
    >>> B = ([1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16])
    >>> print square_matrix_multiply(A, B)
    [[  90.  100.  110.  120.]
     [ 202.  228.  254.  280.]
     [ 314.  356.  398.  440.]
     [ 426.  484.  542.  600.]]

    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    n = A.shape[0]
    outputMatrix = zeros((n, n))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                outputMatrix[i, j] += A[i, k] * B[k, j]
    # print dot(A,B)
    return outputMatrix


def square_matrix_multiply_strassens(A, B):
    """
    Return the product AB of matrix multiplication.
    Assume len(A) is a power of 2
    Return the product AB of matrix multiplication.
    >>> A = ([1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16])
    >>> B = ([1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16])
    >>> print square_matrix_multiply_strassens(A, B)
    [[  90.  100.  110.  120.]
     [ 202.  228.  254.  280.]
     [ 314.  356.  398.  440.]
     [ 426.  484.  542.  600.]]
    """
    A = asarray(A)
    B = asarray(B)
    assert A.shape == B.shape
    assert A.shape == A.T.shape
    assert (len(A) & (len(A) - 1)) == 0, "A is not a power of 2"

    n = A.shape[0]
    outputMatrix = zeros((n, n))
    if(n == 1):
        outputMatrix[0, 0] = A[0, 0] * B[0, 0]
    else:
        splitA = splitMatrixIntoNby2(A)
        splitB = splitMatrixIntoNby2(B)
        splitOutputMatrix = splitMatrixIntoNby2(outputMatrix)
        s1 = splitB[0, 1] - splitB[1, 1]
        s2 = splitA[0, 0] + splitA[0, 1]
        s3 = splitA[1, 0] + splitA[1, 1]
        s4 = splitB[1, 0] - splitB[0, 0]
        s5 = splitA[0, 0] + splitA[1, 1]
        s6 = splitB[0, 0] + splitB[1, 1]
        s7 = splitA[0, 1] - splitA[1, 1]
        s8 = splitB[1, 0] + splitB[1, 1]
        s9 = splitA[0, 0] - splitA[1, 0]
        s10 = splitB[0, 0] + splitB[0, 1]
        p1 = square_matrix_multiply_strassens(splitA[0, 0], s1)
        p2 = square_matrix_multiply_strassens(s2, splitB[1, 1])
        p3 = square_matrix_multiply_strassens(s3, splitB[0, 0])
        p4 = square_matrix_multiply_strassens(splitA[1, 1], s4)
        p5 = square_matrix_multiply_strassens(s5, s6)
        p6 = square_matrix_multiply_strassens(s7, s8)
        p7 = square_matrix_multiply_strassens(s9, s10)
        splitOutputMatrix[0, 0] = p5 + p4 - p2 + p6
        splitOutputMatrix[0, 1] = p1 + p2
        splitOutputMatrix[1, 0] = p3 + p4
        splitOutputMatrix[1, 1] = p5 + p1 - p3 - p7
        outputMatrix = combineSplitMatrix(splitOutputMatrix, outputMatrix)
    return outputMatrix


def splitMatrixIntoNby2(matrix):
    n = matrix.shape[0]
    a11 = matrix[0:n / 2, 0:n / 2]
    a12 = matrix[0:n / 2, n / 2:n]
    a21 = matrix[n / 2:n, 0:n / 2]
    a22 = matrix[n / 2:n, n / 2:n]
    return asarray(([a11, a12], [a21, a22]))


def combineSplitMatrix(inputMatrix, combinedMatrix):
    n = combinedMatrix.shape[0]
    combinedMatrix[0:n / 2, 0:n / 2] = inputMatrix[0, 0]
    combinedMatrix[0:n / 2, n / 2:n] = inputMatrix[0, 1]
    combinedMatrix[n / 2:n, 0:n / 2] = inputMatrix[1, 0]
    combinedMatrix[n / 2:n, n / 2:n] = inputMatrix[1, 1]
    return combinedMatrix


def test():
    maxSubArray = find_maximum_subarray_brute(STOCK_PRICE_CHANGES)
    print "Maximum sub array for the input ", STOCK_PRICE_CHANGES
    print "1)Using brute force algorithm :\
        ,\ni : ", maxSubArray[0], "\nj : ", maxSubArray[1], "\
        sum : ", sum(STOCK_PRICE_CHANGES[maxSubArray[0]:(maxSubArray[1] + 1)])

    maxSubArray = find_maximum_subarray_recursive(STOCK_PRICE_CHANGES)
    print "2)Using recursive algorithm :\
        ,\ni : ", maxSubArray[0], "\nj : ", maxSubArray[1], "\
        sum : ", sum(STOCK_PRICE_CHANGES[maxSubArray[0]:(maxSubArray[1] + 1)])

    maxSubArray = find_maximum_subarray_iterative(STOCK_PRICE_CHANGES)
    print "3)Using iterative algorithm :\
        ,\ni : ", maxSubArray[0], "\nj : ", maxSubArray[1], "\
        sum : ", sum(STOCK_PRICE_CHANGES[maxSubArray[0]:(maxSubArray[1] + 1)])

    maxSubArray = find_maximum_crossing_subarray(
        STOCK_PRICE_CHANGES, 0, 7, 15)
    print "4)Maximum crossing subarray :\
        ,\ni : ", maxSubArray[0], "\nj : ", maxSubArray[1], "\
        sum : ", sum(STOCK_PRICE_CHANGES[maxSubArray[0]:(maxSubArray[1] + 1)])

    a = ([1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16])
    b = ([1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16])
    print "Multiplication of \nA :", asarray(a), " and \nB : ", asarray(b)
    c = square_matrix_multiply(a, b)
    print "1)Normal multiplication ", c
    c = square_matrix_multiply_strassens(a, b)
    print "2)Strassens multiplication ", c
    pass


if __name__ == '__main__':
    test()
