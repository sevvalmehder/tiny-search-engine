from typing import List

from src.positional_inverted_index import PositionalInvertedIndex
from src.base import BaseTextProcessor
from src.boolean_query_processor import BooleanQueryProcessor
from src.metrics import *

class QueryProcessor(BooleanQueryProcessor):
    def __init__(self) -> None:

        # First creat different index from boolean query processor
        self._index = PositionalInvertedIndex()
        
        # If dictionary cannot load, then build
        if not self._index.load():
            self._index.build()
        
        # Creat text processor for process the query
        self._preprocessor = BaseTextProcessor()

        # Keep the document count N
        self.N = self._index.get("N")[0]

        # Create a dictionary to keep idf_values
        self.idf_values = {}

    def process(self, q) -> List:
        """
        This is a function to override process function of base class.
        """

        # Decide the type of the query (free text or phrase)
        is_phrase = True if q[0] == '"' and q[-1] == '"' else False

        # Then preprocess
        q_tokens = self._preprocess(q)

        bag = []
        count = 0
        for token in q_tokens:
            bag.append(self._index.get(token.casefold()))

            if len(bag) > 1:
                sub_result = self._operation(bag, 'AND')
                if sub_result == None:
                    print("sub_result is None")
                    exit()
                
                if is_phrase:
                    sub_result = self._phrase_check(sub_result, count)
                else:
                    sub_result = self._free_text_check(sub_result)
                bag.append(sub_result)

            count += 1

        result_list = bag.pop()
        result = []
        if not is_phrase:
            result = self._free_text_query_operations(q_tokens, list((map(lambda dict:dict.get("doc_id"), result_list))))
        else:
            result = result_list
        return result

    def _phrase_check(self, sub_result, count):
        """
        The sub_result is like:
        [
            {
                "left" : [1,2,3,89],
                "right": [2,3,4,34,145],
                "doc_id": 8907
            },
            ...
        ]

        Process over left and right positions and check if 
        left positions + count gives the right positions. 
        If so keep them in a new key called positions.

        :return: The processed sub_result will be like:,
        [
            {
                "positions" : [1,2,3],
                "doc_id": 8907
            },
            ...
        ]
        """
        result = []
        for dict in sub_result:
            positions = []
            for i in dict.get("left"):
                if i+count in dict.get("right"):
                    positions.append(i)
            if len(positions) != 0:
                result.append({"positions": positions, "doc_id": dict.get("doc_id")})
        return result
    
    def _free_text_check(self, sub_result):
        """
        The sub_result is like:
        [
            {
                "left" : [1,2,3,89],
                "right": [2,3,4,34,145],
                "doc_id": 8907
            },
            ...
        ]

        Just eleminate unnecessary position informations. And keep doc ids
        
        :return: The processed sub_result will be like:
        [ {'doc_id': 8907}, ..]
        """
        ids = list((map(lambda dict:{"doc_id":dict.get("doc_id")}, sub_result)))
        return ids

    def _free_text_query_operations(self, q_tokens, doc_ids):
        """
        Cosine similarity with (log-scaled) TF-IDF weighting is used.
        The function returns the IDs of the documents as well as their cosine 
        similarity scores, ranked by their cosine similarities to the query. 
        Documents with zero cosine similarity are eliminated
        """
        """
        kelimeler | query vector   | doc1 vector  | doc2 vecotr
        common       tfidf score     tfidf score    tfidf score 
        stock        tfidf score     tfidf score    tfidf score 
        """
        document_vectors = []

        # Create document vectors
        for doc_id in doc_ids:
            vector = []
            for token in q_tokens:
                # Calculate the log scaled tf-idf score
                # Then create a vector for this document
                idf = self.get_idf(token)
                tf = self.get_tf(doc_id, token)
                score = tf*idf
                vector.append(score)

            document_vectors.append((doc_id, vector))
        
        # Create query vector
        query_vector = []
        for token in q_tokens:
            tf = calculate_tf(q_tokens.count(token))
            idf = self.get_idf(token)
            score = tf*idf
            query_vector.append(score)
        
        return [
            "Document-{} with cosine similarity:{}".format(doc_id, cosine)
            for doc_id, cosine
            in self.calculate_cosine(document_vectors, query_vector)
        ]
            
    def calculate_cosine(self, document_vectors, query_vector):
        """
        Calculate cosine similarity between query_vector and document vectors
        """
        result = {}
        for doc_id, vector in document_vectors:
            result[doc_id] = cosine(query_vector, vector)

        result = sorted(result.items(), key=lambda row:row[1], reverse=True)
        return result 

    def get_idf(self, token):
        """
        Function to get idf value belongs to given token.
        If the idf value is already exist then return
        Otherwise, calculate the idf, add it to the idf_values dict
        then return.
        """
        if token in self.idf_values.keys():
            return self.idf_values.get(token)
        else:
            idf = calculate_idf(self.N, len(self._index.get(token)))
            self.idf_values[token] = idf
            return idf

    def get_tf(self, doc_id, token):
        """
        Get the token's posting list (with positions and document id)
        Traverse it and find the positions array length belongs to 
        given document id. Then calculate log scaled tf value
        """
        f = 0
        for i in self._index.get(token):
            if i.get("doc_id") == doc_id:
                f = len(i.get("positions"))

        return calculate_tf(f)
