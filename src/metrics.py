"""
This is a library that includes some helper functions 
to use some metrics such as tf if, cosine, etc..
"""
import operator
import math

def dot_product(v1, v2):
    return sum(map(operator.mul, v1, v2))

def cosine(v1, v2):
    prod = dot_product(v1, v2)
    len1 = math.sqrt(dot_product(v1, v1))
    len2 = math.sqrt(dot_product(v2, v2))
    cosine = prod / (len1 * len2)
    return f"{cosine:.3f}"

def calculate_idf(N, df):
    """
    N is the total number of documents in the collection
    df is the document frequency of t
    """
    if df == 0:
        return 0
    return math.log(N/df)

def calculate_tf(freq):
    """
    freq is the actual term frequency.
    This function returns log scaled term frequency
    """
    return 1 + math.log(freq)
