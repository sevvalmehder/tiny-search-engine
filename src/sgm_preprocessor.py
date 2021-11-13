import os
import re
import time
from dataclasses import dataclass

from base import BaseTextProcessor, BaseDataAccess

"""
Here are some global variables
"""
dataset_path = "reuters21578"

@dataclass
class Document():
    """
    Object for keeping necessary parts of each documents

    id -> NEWID element
    content -> includes both TITLE and BODY
    """
    id: int
    content: str

class SGMPreprocessor(BaseTextProcessor):

    def __init__(self) -> None:
        self._dataset = dataset_path
        self._docs = [] # List of Document

        super().__init__()

    def _sgm_parser(self, content):
        """
        SGM parser to parse sgm file to id, title and body.
        This function create the `self.docs` i.e list of Document
        """

        for doc in re.finditer("<REUTERS(.*?)</REUTERS>", content, re.DOTALL):
            doc = doc.group(0)
            
            # Get the id from doc
            # But continue with another document if there is no id information
            id = re.findall("NEWID=\"(.*?)\">", doc, re.DOTALL)
            if not id:
                continue

            # Get the title and body informations
            title = re.findall("<TITLE>(.*?)</TITLE>", doc, re.DOTALL)
            body = re.findall("<BODY>(.*?)</BODY>", doc, re.DOTALL)
            
            # If they not exist then assign them an empty string
            title = title[0] if title else ""
            body = body[0] if body else ""

            # Create content with joining title and body strings
            # Note: join will append a whitespace between two strings
            content = " ".join([title, body])

            # Create Document with id and content
            document = Document(int(id[0]), content)
            self._docs.append(document)

    def run(self):
        
        start_parsing = time.perf_counter()

        # List the .sgm file in dataset folder
        sgm_files = [path for path in os.listdir(self._dataset) if path.endswith('sgm')]

        # Iterate over docs and create self._docs list
        for sgm in sgm_files:
            sgm_content = self.data.read(os.path.join(self._dataset, sgm), encoding='latin-1')
            self._sgm_parser(sgm_content)
        
        end_parsing = time.perf_counter()
        print(f"[Done] SGM files are parsed in {end_parsing - start_parsing:0.4f} seconds")

        for doc in self._docs:
            self._text = doc.content
            self.case_folding()
            self.punctuation_remove()
            doc.content = self._text
        
        end_preprocess = time.perf_counter()
        print(f"[Done] Documents are preprocessed in {end_preprocess - end_parsing:0.4f} seconds")

        

