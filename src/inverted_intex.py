import time
import pickle

from base import BaseInvertedIndex
import sgm_preprocessor as sp

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
            tokens = list(set(tokens))

            for token in tokens:
                self.add(token, doc.id)
        
        end_building = time.perf_counter()
        print(f"[Done] Inverted Index is builded in {end_building - start_building:0.4f} seconds")
            
    def save(self):
        with open("dictionary.pkl", "wb") as f:
            pickle.dump(self.dictionary, f)
            f.close()
        print("[Done] Dictionary is saved!")

    def load(self):
        with open("dictionary.pkl", "rb") as f:
            self.dictionary = pickle.load(f)
            f.close
        print("[Done] Dictionary is loaded!")

    def merge(self):
        pass
    
    def union(self):
        pass