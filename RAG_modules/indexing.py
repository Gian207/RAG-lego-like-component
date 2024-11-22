from qdrant_client import models, QdrantClient
 #create the embedding model
from RAG_modules.embedding import Embedding


class Indexing:
    
    def __init__(self, data, embedding_model_name):
        self.data = data
        self.embedding_model = Embedding(embedding_model_name)

        self.client = QdrantClient(":memory:")
        self.client.create_collection(
            collection_name="evaluation",
            vectors_config=models.VectorParams(
                size=self.embedding_model.get_embedding_dimension(),  # Vector size is defined by used model
                distance=models.Distance.COSINE,
            )
        )
        self.client.upload_points(
            collection_name="evaluation",
            points=[
                models.PointStruct(
                    id=idx, vector=self.embedding_model.embedding(doc["page_content"]).tolist(), payload=doc
                )
                for idx, doc in enumerate(documents_to_dicts(self.data))
            ],
        )
        self.retrieved_ids = []
    
    def getRetrievedIds(self):
        return self.retrieved_ids
    
    def getLastRetrievedIds(self):
        return self.retrieved_ids[-1]

    
    def retriever_context(self,query:str ): 
        global empty_query
        hits = self.client.search(
                    collection_name="evaluation",
                    query_vector=self.embedding_model.encode_query(query).tolist(),
                    limit=1,
                     )
        if (len(query) < 5 or query == "_"):
            self.retrieved_ids.append(-1)
        else:
            self.retrieved_ids.append(hits[0].payload["retriver_id"])
        return hits[0].payload["page_content"]


    
def documents_to_dicts(documents):
        """
        Convert a list of Document objects into a list of dictionaries.
        
        Parameters:
        - documents: A list of Document objects.
        
        Returns:
        - A list of dictionaries where each dictionary represents a Document object.
        """
        dicts_list = []
        for doc in documents:
            doc_dict = {
                'page_content': doc.page_content,
                'filename': doc.metadata["filename"],
                'retriver_id': doc.metadata["id"],
            }
            dicts_list.append(doc_dict)
        
        return dicts_list
    
      