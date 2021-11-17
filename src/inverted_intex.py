import time
import pickle

from src.base import BaseInvertedIndex
import src.sgm_preprocessor as sp

class InvertedIndex(BaseInvertedIndex):
    """
    Inverted Index class with high level functions.

    functions:
    - build: to build a dictionary
    - save: to save the dictionary
    - load: to load the saved dictionary if exist
    - merge: intersection operation
    - uninon: union operation
    """
    def __init__(self) -> None:
        super().__init__()
        self.sgmp = sp.SGMPreprocessor()
        

    def build(self):
        """
        Building inverted intex with using SGM Preprocessor
        """

        # First run the SGMPreprocessor to build the doc list.
        self.sgmp.run()

        start_building = time.perf_counter()

        for doc in self.sgmp.docs:
            # Get the token list and append
            tokens = self.sgmp.tokenize(doc.content)
            tokens = list(set(tokens) - set(self.sgmp.stopwords))

            for token in tokens:
                self.add(token, doc.id)
        
        end_building = time.perf_counter()
        print(f"[Done] Inverted Index is builded in {end_building - start_building:0.4f} seconds")
        
        self.save()
            
    def save(self):
        with open("dictionary.pkl", "wb") as f:
            pickle.dump(self.dictionary, f)
            f.close()
        print("[Done] Dictionary is saved!")

    def load(self) -> bool:
        try:
            with open("dictionary.pkl", "rb") as f:
                self.dictionary = pickle.load(f)
                f.close
            print("[Done] Dictionary is loaded!")
            return True
        except(FileNotFoundError):
            print("[LOG] Dictionary not found!")
            return False

    def merge(self, l, r):
        """
        Return the intersection of the left(l) and right(r) postings

        It represents the AND operation.
        """
        # Initialize indexes and result as an empty list
        # i represents the pointer of long list and j belongs to short one
        i, j = 0, 0
        result = []

        short, long = (l, r) if len(l) < len(r) else (r, l)
        while i < len(long) and j < len(short):
            if long[i] == short[j]:
                result.append(long[i])
                j += 1
                i += 1
            elif long[i] > short[j]:
                j += 1
            else:
                i += 1
            

        return result

    def union(self, l, r):
        """
        Return the union of the left(l) and right(r) postings

        It represents the OR operation.
        """
        # Initialize indexes and result as an empty list
        # i represents the pointer of long list and j belongs to short one
        i, j = 0, 0
        result = []

        short, long = (l, r) if len(l) < len(r) else (r, l)

        # This loop ends when short list traversed
        while i < len(long) and j < len(short):
            if long[i] <= short[j]:
                result.append(long[i])
                if long[i] == short[j]:
                    j += 1
                i += 1
            else:
                result.append(short[j])
                j += 1
        
        # We may still have elements in long list.
        # These remain elements are added to result

        return result + long[i:]

    def difference(self, l, r):
        """
        Return the difference of the left(l) and right(r) postings

        It represents the NOT operation. (l-r or l/r)
        """
        result = l.copy()

        for i in r:
            if i in result:
                result.remove(i)
        
        return result