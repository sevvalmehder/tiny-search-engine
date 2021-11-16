"""
Contains two base classes that are important:

BaseDataAccess -> Read and write functions to access data
BaseTextProcessor -> Abstract class which has common functions for text processor
"""
import os
import string
from abc import abstractmethod
from typing import List


"""
Here are some global variables
"""
stopword_path = "stopwords.txt"

class BaseDataAccess:
    """
    Base class for manage data read/write operations 
    for common use.
    """

    def read(self, read_path, encoding='utf-8', mode='r'):
        """
        Read data from given read_path with default utf-8 encoding and read('r') mode.
        """
        with open(os.path.join(os.getcwd(), read_path), encoding=encoding, mode=mode) as f:
            data = f.read()
            f.close()

        return data

    def write(self, data, write_path, mode='w'):
        """
        Write given data to given write_path with default mode write('w).
        """
        with open(os.path.join(os.getcwd(), write_path), mode=mode) as f:
            f.write(data)
            f.close()

class BaseTextProcessor():
    """
    Base text preprocessing class for impelements necessary preprocessing
    operations such as tokenization and elimination stop words

    self.data -> for i/o operations
    self.text -> the text that wanted to be processed
    """

    def __init__(self) -> None:
        self.data = BaseDataAccess()
        self._text = None
    
    def tokenize(self, text=None) -> List[str]:
        """
        Tokenization operation for covnerting strings to tokens i.e words
        """
        if text:
            return text.split()
        else:
            return self.text.split()
    
    def punctuation_remove(self):
        """
        Punctuation remove operation with using string maketrans

        Info: 
        - maketrans creates a mapping table.
        - In this example it will map the characters in third arg with None
        - src: https://docs.python.org/3.3/library/stdtypes.html?highlight=maketrans#str.maketrans
        """
        to_remove = string.punctuation + "\n"
        mapper = str.maketrans('', '', to_remove)
        self._text = self._text.translate(mapper)

    @property
    def stopwords(self) -> str:
        
        if stopword_path:
            return self.data.read(stopword_path)
        else:
            print("The module for finding stopword is not implemented yet.")
            return None

    def case_folding(self):
        """
        Case-folding operation for string.
        Lower also can be used for case-folding.

        Detailed information about casefold() function in Python:
        https://docs.python.org/3/howto/unicode.html?highlight=casefold#comparing-strings
        """
        self._text = self._text.casefold()
        #self._text = self._text.lower()

    @abstractmethod
    def split(self):
        pass
    
    @abstractmethod
    def normalize(self):
        pass
    
    @abstractmethod
    def stem(self):
        pass

class BaseInvertedIndex:
    """
    Base class for inverted index basic operations.
    Tokens and posting list will be kept in map and names as dictionary.
    
    Dict data structure used for this purpose. Because it represents 
    Hashmap in Python.
    src: https://docs.python.org/3/library/stdtypes.html#typesmapping
    For map keys represent the tokens(words) and values represent the 
    posting lists that keep document ids.
    keys: string
    values: list of integer

    Key points:
    - Posting lists are sorted in ascending order.
    - Binary search is used for insert a new id to posting list -> O(logn)
    
    Functions:
    - get: Returns the posting list(value) of given token -> O(1)
    - add: Add the token belongs to given id to the dictionary
    - update: It updates the dictionary with giving key-value pair -> O(1)
    - insert: It insert the given document id to the posting list of given key
    """
    
    def __init__(self) -> None:
        self.dictionary = {}

    def get(self, token) -> List:
        """
        Returns the posting list of given token.
        """
        value = self.dictionary.get(token)
        return value if value else []

    def add(self, token, id) -> None:
        """
        Add the given token which belongs to given id to the dictionary
        """
        if token in self.dictionary.keys():
            self._insert(token, id)
        else:
            self._update(token, [id])


    def _update(self, key, value=[]) -> None:
        """
        This function updates the dictionary with given key-value pair

        Params:
        - key: the token(word) that wanted to be added.
        - value: the posting list that includes document ids. If there is no value given
                 it initialized with an empty list.
        """
        self.dictionary.update({key: value})
    
    def _insert(self, key, id) -> None:
        """
        This function insert the given document id to the sorted posting list of given token.
        Insertion implemented as like adding to the binary tree.

        Params:
        - key -> the token(word) that occured in given document id
        - id -> the document id
        """
        
        posting = self.dictionary.get(key)
        
        # Dind the index that showing where this id should be added
        start = 0
        end = len(posting) - 1

        while start <= end:
            middle = int((start+end)/2)

            if posting[middle] > id:
                end = middle - 1
            else:
                start = middle + 1

        posting.insert(start, id)






















