# This script generates a testset for the evaluation of the LLMs manally prepare the bachmark.csv file.
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()
from RAG_modules.loader import DataLoader
from RAG_modules.splitting import Slitting
from RAG_modules.indexing import Indexing

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
def get_llm(model):
    if model == "llama":
        model_name = "llama3:instruct"
    elif model == "gemma":
        model_name = "gemma2:2b-instruct-q8_0"

    llm = Ollama(
        model=model_name,
        base_url=os.getenv('OLLAMA_API'),
        temperature=0.40,
        top_p=0.90,
        top_k=30,
        num_ctx=500
    )

    prompt = ChatPromptTemplate.from_template("""Il tuo compito è quello di formulare una domanda a partire da un contesto dato, rispettando le regole indicate di seguito: 
                        1. La domanda deve avere una risposta completa a partire dal contesto dato.
                        2. La domanda deve essere formulata a partire da una parte che contiene informazioni non banali. 
                        3. La risposta non deve contenere collegamenti. 
                        4. La domanda deve essere di difficoltà moderata. 
                        5. La domanda deve essere ragionevole e deve poter essere compresa e risolta dagli esseri umani. 
                        6. Non usare frasi come “ha fornito il contesto”, ecc. nel contesto della domanda.                               
                      Contesto:
                      ---------
                      {contesto}
                      ---------
                      Rispondi con solo la domanda riformualta.""")
    return prompt, llm


def generate_benchmark(model, embName, chunk_size):

  #LOADING THE DOCUMENTs
  docs = DataLoader().load()
  #SPLITTING THE DOCUMENTS
  text_splitter = Slitting(chunk_size)
  documents_slitted = text_splitter.slit_docs(docs)
  for i, doc in enumerate(documents_slitted):
          doc.metadata["id"] = i
  #INDEXING THE DOCUMENTS
  index = Indexing(documents_slitted, embName)
  prompt, llm = get_llm(model)
  
  filtered_docs = [doc for doc in documents_slitted if len(doc.page_content) > 100]

  import pandas as pd
  benchmark_dir = 'benchmark'
  if not os.path.exists(benchmark_dir):
    os.makedirs(benchmark_dir)

  output_file = 'benchmark/banchmark_size'+str(chunk_size)+'_'+model+'_with_embedding_'+embName+'.csv'
  print("Path: ", output_file) 
  if os.path.exists(output_file):
     print("File exists")
     data = pd.read_csv(output_file)
  else:
    print("File does not exists, so we create a new one")
    data = pd.DataFrame(columns=['question', 'context',  'retrieved_context','retrieve_id','num_empty_query','score'])
    data.to_csv(output_file, index=False)

  chain = prompt | llm 
  with open(output_file, 'a', newline='') as f:
    for doc in filtered_docs:
            context = doc.page_content
            question = chain.invoke({"contesto": context})
            retrieved_context = index.retriever_context(question)
            retrieve_id = index.getLastRetrievedIds()
            score = int(retrieve_id == doc.metadata["id"])
            empty_query = index.getRetrievedIds().count(-1)

            # Append the new row to the CSV file
            new_row = {
                'question': question,
                'contexts': context,
                'retrieved_context': retrieved_context,
                'retrieve_id': retrieve_id,
                'num_empty_query': empty_query,
                'score': score,
            }
            pd.DataFrame([new_row]).to_csv(f, header=False, index=False)

  # Calculate and print the score
    data = pd.read_csv(output_file)
    score = data["score"].sum()
    hit_rate = score /len(data) if len(data) > 0 else 0
    print("Hit rate: ", hit_rate)

  data.to_csv(output_file, index=False)

  return hit_rate


import csv
import argparse



def main():
    parser = argparse.ArgumentParser(description="Create a benchmark file for the evaluation of retrieval component")
    parser.add_argument("-s", "--size", nargs=1, required=True, help="Chunk size to split the document")
    parser.add_argument("-l", "--llm", nargs=1, required=True, choices=['llama', 'gemma'], help="The LLM model to use for generating the questions")
    parser.add_argument("-e", "--embedding", nargs=1, required=True, help="The embedding model to use for the evaluation")
    args = parser.parse_args()

    chunk_size = int(args.size[0])
    model = args.llm[0]
    embedding_model = args.embedding[0]  # Example: msmarco-MiniLM-L-6-v3
    
    hit_rate = generate_benchmark( model,embedding_model, chunk_size)

    
    if not os.path.exists("result"):
        os.makedirs("result")

    if not os.path.exists("result/score_and_combination.csv"):
        with open("result/score_and_combination.csv", "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Chunk Size", "Model", "Embedding Model", "Hit_rate"])
            csvwriter.writerow([chunk_size, model,embedding_model, hit_rate,])
    else: 
      with open("result/score_and_combination.csv", "a", newline='') as csvfile:
          csvwriter = csv.writer(csvfile)
          csvwriter.writerow([chunk_size, model,embedding_model, hit_rate])

if __name__ == "__main__":
    main()
    




        
 

