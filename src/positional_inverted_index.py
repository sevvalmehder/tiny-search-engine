import time
import re

from src.inverted_intex import InvertedIndex
class PositionalInvertedIndex(InvertedIndex):
    """
    Positional Inverted Index class with high level functions
    
    functions:
    - save & load functions are same with the base class
    """

    def __init__(self) -> None:
        """
        The index shema for posiiton inverted index is like that:
        {
            "key": [
                "positions": [1, 4, 20],
                "doc_id": 9001
            ],
            "another key": [
                "positions": [17],
                "doc_id": 9002
            ]
        }
        """
        super().__init__()     

    def build(self):
        """
        Building positional inverted index with using SGM Preprocessor
        """

        self.sgmp.run()

        start_building = time.perf_counter()
        for doc in self.sgmp.docs:
            doc.content = self.sgmp.stopword_remove(doc.content)

            # Get the token list and append
            tokens = self.sgmp.tokenize(doc.content)

            for position, token in enumerate(tokens):
                self.add(token, {"positions": [position], "doc_id": doc.id})

        self.add("N", len(self.sgmp.docs))
        end_building = time.perf_counter()
        print(f"[Done] Inverted Index is builded in {end_building - start_building:0.4f} seconds")
        
        self.save()
    
    def _insert(self, key, value):
        """
        This is a function that overrides the _insert function from base class(BaseInvertedIndex)

        - key 
        - value -> a dict has include position and doc_id
        """
        # posting is like -> [{"positions":[1], "doc_id":4}, {"positions":[5], "doc_id":8}]
        posting = self.dictionary.get(key)
        
        # Find the index that showing where this id should be added
        start = 0
        end = len(posting) - 1
        the_index = -1

        while start <= end:
            middle = int((start+end)/2)

            if posting[middle].get("doc_id") == value.get("doc_id"):
                the_index = middle
                break
            elif posting[middle].get("doc_id") > value.get("doc_id"):
                end = middle - 1
            else:
                start = middle + 1

        if the_index == -1:
            posting.insert(start, value)
        else:
            posting[the_index].get("positions").extend(value.get("positions"))


    def merge(self, l, r):
        """
        This is a function that overrides the merge function from base class(InvertedIndex)
        """
        # Initialize indexes and result as an empty list
        # i represents the pointer of long list and j belongs to short one
        i, j = 0, 0
        result = []

        short, long = (l, r) if len(l) < len(r) else (r, l)
        while i < len(long) and j < len(short):
            if long[i].get("doc_id") == short[j].get("doc_id"):
                if len(l) < len(r):
                    result_dict = {
                        "left": short[j].get("positions"),
                        "right": long[i].get("positions"),
                        "doc_id": long[i].get("doc_id")
                    }
                else:
                    result_dict = {
                        "left": long[i].get("positions"),
                        "right": short[j].get("positions"),
                        "doc_id": long[i].get("doc_id")
                    }
                result.append(result_dict)
                j += 1
                i += 1
            elif long[i].get("doc_id") > short[j].get("doc_id"):
                j += 1
            else:
                i += 1

        return result
    
    def union(self, l, r):
        """
        This is a function that overrides the union function from base class(InvertedIndex)
        """
        # Initialize indexes and result as an empty list
        # i represents the pointer of long list and j belongs to short one
        i, j = 0, 0
        result = []

        short, long = (l, r) if len(l) < len(r) else (r, l)

        # This loop ends when short list traversed
        while i < len(long) and j < len(short):
            if long[i].get("doc_id") <= short[j].get("doc_id"):
                result.append(long[i])
                if long[i].get("doc_id") == short[j].get("doc_id"):
                    j += 1
                i += 1
            else:
                result.append(short[j])
                j += 1
        
        # We may still have elements in long or short list.
        # These remain elements are added to result
        return result + long[i:] + short[j:]
    
    def difference(self, l, r):
        """
        This is a function that overrides the difference function from base class(InvertedIndex)
        """
        pass
        

