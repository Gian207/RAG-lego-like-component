# slitting.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class Slitting:
    def __init__(self, _chunk_size, _chunk_overlap=200):
        
        self.splitter = RecursiveCharacterTextSplitter(   
				chunk_size=_chunk_size,  
				chunk_overlap=_chunk_overlap,  
				length_function=len,  
				is_separator_regex=False,
				add_start_index=True
        )

    def slit_docs(self, _doc):
        for _doc in _doc:
          assert isinstance(_doc, Document)
        return self.splitter.split_documents([_doc])

       
