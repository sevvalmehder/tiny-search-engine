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
    
    def tokenize(self) -> List[str]:
        """
        Tokenization operation for covnerting strings to tokens i.e words
        """

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