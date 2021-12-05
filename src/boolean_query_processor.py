from typing import List
from src.inverted_intex import InvertedIndex
from src.base import BaseTextProcessor

class BooleanQueryProcessor:
    def __init__(self) -> None:

        # First creat the inverted index and load the dictionary
        self._index = InvertedIndex()
        
        # If dictionary cannot load, then build
        if not self._index.load():
            self._index.build()
        
        # Creat text processor for process the query
        self._preprocessor = BaseTextProcessor()

        # Define operands
        self._operands = ["AND", "OR", "NOT"]

    def process(self, q) -> List:
        """
        Process function for parse and run the query

        It takes as input a query
        It returns the IDs of the matching documents sorted in ascending order.
        """

        q_tokens = self._preprocess(q)

        bag = []      
        operand = None

        for token in q_tokens:
            if token in self._operands:
                if not bag:
                    print("Please correct your query!")
                    exit()
                operand = token
            else:
                bag.append(self._index.get(token.casefold()))
                if len(bag) > 1 and operand != None:
                    sub_result = self._operation(bag, operand)
                    if sub_result == None:
                        exit()
                    bag.append(sub_result)
                elif len(bag) > 2 and operand == None:
                    print("Please correct your query, there is no operand!")
                    exit()


        return bag.pop()

    def _preprocess(self, q) -> str:
        """
        Function for preprocess the query before process
        """
        self._preprocessor._text = q
        self._preprocessor.punctuation_remove()
        text = self._preprocessor.stopword_remove()
        return self._preprocessor.tokenize(text)

    def _operation(self, bag, operand) -> List:
        """
        This function operate the sub-operations with inputs:
        - 1 operand -> and, or, not
        - 2 posting list

        It returns the result posting list.

        PS: .pop(0) for processing like queue(FIFO)
        """
        if operand == 'AND':
            return self._index.merge(bag.pop(0), bag.pop(0))
        elif operand == 'OR':
            return self._index.union(bag.pop(0), bag.pop(0))
        elif operand == 'NOT':
            return self._index.difference(bag.pop(0), bag.pop(0))
        else:
            print("Wrong operator!")
            return None
