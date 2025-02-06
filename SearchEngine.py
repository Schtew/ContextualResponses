import os
from DataLoader import DataLoader
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from deepeval import assert_test
from deepeval.metrics import (
    AnswerRelevancyMetric, 
    FaithfulnessMetric, 
    ContextualRelevancyMetric, 
    ContextualPrecisionMetric
)
from deepeval.test_case import LLMTestCase
from deepeval import evaluate

class SearchEngine:
    def __init__(self, arXiv = 1000):
        """
        Initialize the SearchEngine with an optional number of arXiv papers to load.

        Args:
            arVix (int, optional): Number of papers to load. If 0, source arXiv will not be used.
        """
        self.key = os.environ.get('OPENAI_API_KEY')
        self.model = ChatOpenAI(model="gpt-3.5-turbo-0125")
        self.embedding = OpenAIEmbeddings()
        store = LocalFileStore('./cache')
        cached_embedding = CacheBackedEmbeddings.from_bytes_store(self.embedding, store, namespace=self.embedding.model)
        self.documents = []
        if arXiv:
            self.documents = DataLoader.load_arxiv_papers('data/arxiv-metadata-oai-snapshot.json', arXiv)
        # print(self.documents[0])
        self.vectorstore = FAISS.from_documents(documents=self.documents, embedding=cached_embedding)
        
    def query_retriever(self, query, k = 4):
        """Retrieve relevant contexts based on the query"""
        results = self.vectorstore.similarity_search(query, k = k)
        texts = []
        for r in range(len(results)):
            texts.append(results[r].page_content) #Note: Metadata is not used currently
        return texts

    def generate_response(self, query: str, contexts = None) -> str:
        """Generate a response based on the query and retrieved contexts"""
        if not contexts:
            contexts = self.query_retriever(query)
        context_texts = "\n\n".join(contexts)
        prompt = f"""Based on the following contexts, answer the question.
        
        Contexts:
        {context_texts}
        
        Question: {query}
        
        Answer:"""
        
        response = self.model.invoke(prompt)
        return response.content
    
    def evaluate_response(self, query: str) -> str:
        contexts = self.query_retriever(query)
        response = self.generate_response(query, contexts)
        
        # Create test cases
        test_case = LLMTestCase(
            input = query,
            actual_output = response,
            retrieval_context = contexts
        )
        
        # Metrics
        metrics = [
            AnswerRelevancyMetric(),
            FaithfulnessMetric(),
            ContextualRelevancyMetric(),
            # ContextualPrecisionMetric() Needs expected_output
        ]

        # Evaluate
        evaluate([test_case], metrics)
        # return results

    
if __name__ == "__main__":
    search_engine = SearchEngine()
    # result = search_engine.generate_response("What is the impact of quantum computing on cryptography?")
    # print(result)
    search_engine.evaluate_response("What is the impact of quantum computing on cryptography?")
        
        