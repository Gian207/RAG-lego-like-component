# RAG-lego-like-component

A RAG system consists of a retriever and a large language model. In response to a user query, the retriever identifies most relevant content from a corpus, which the LLM then uses to generate a response. This formulation allows for a multitude of design choices, including the selection of an appropriate retrieval method, chunk size, splitting technique and embedding model. It is not always the case that a RAG system will perform optimally in all contexts. Its efficacy may vary depending on the specific data domain, corpus size and cost budget in question. Therefore, the creation of a universal architecture for all use cases is not a viable solution; rather, it is essential to analyze each case individually in order to identify the most suitable parameters.


To simplify the creation of the RAG system, a modular, Lego-like design was developed.

<img width="500" alt="Meme generation" src="https://github-production-user-asset-6210df.s3.amazonaws.com/96686091/395840772-040e9b02-1071-41d5-a724-4c2aa87b71eb.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20241215%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241215T094625Z&X-Amz-Expires=300&X-Amz-Signature=a209fcbe4ee1e70360844978f99a22cde42fe25978b931395f04329988a9ae84&X-Amz-SignedHeaders=host" />


# Rag-eval
A RAG systems evaluation is done using fixed benchmark datasets.
However, when a benchmark is not available, it must be created from scratch using the private data.

## Benchmark creation proposal: Generative Universal Evaluation LLM and Information retrieval
To accomplish this effectively, we acknowledge that manually creating hundreds of question-context-answer examples from documents is a time-consuming and labor-intensive task. Therefore, utilizing a large language model (LLM) to generate synthetic test data offers a more efficient solution that reduces both time and effort.

<img width="478" alt="Meme generation" src="https://github.com/user-attachments/assets/d8ba5947-29dd-411d-84b4-4d8579ed29d1" />

Therefore, to facilitate the benchmark creation process, an automated method was developed.

At the time of writing, various frameworks exist for creating synthetic training data. The main one is RAGAS, but is not the optimal choice for smaller LLMs, as they are not always able to generate the requisite output in the desired JSON format. 
In order to solve this problem, the following approach was developed.

### Algoritm 
We first split the text document into a given chunk_size using the recursive text splitter method and then we store these in in-memory qdrantDB vector store. Now, for each context that is larger than 100 characters, we create a question using an LLM. 
Then we test if a given query can retrieve its original passage as the top result using its retrieve: If the retriever returns the original context where the question came from, we assign a score of 1, 0 otherwise. 
We create a benchmark with the following structure: 
ID: each rows represent a context with a unique id, in order to check if the retrieved content is the same as the contenxt.
• question: the generated query by the LLM starting from the context;
• context: the spitted document is considered as the context provided
if the lenght of the chunks is greater than a treeshold;
• retrieved_content: the content retrieved from the system given the query;
• retrieved_id: the chunk ID retrieved by the retriever system;
• score: 1 if the retrieved context is equals to the context, 0 otherwise;

<img width="700" alt="Algoritm for benchmark generation" src="https://github.com/user-attachments/assets/40e70155-04f4-43fa-845f-a35168a67406" />

