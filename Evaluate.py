from SearchEngine import SearchEngine
from deepeval import assert_test
from deepeval.metrics import (
    AnswerRelevancyMetric, 
    FaithfulnessMetric, 
    ContextualRelevancyMetric, 
    ContextualPrecisionMetric
)
from deepeval.test_case import LLMTestCase
from deepeval import evaluate
import tiktoken

class Evaluate:
    
    def evaluate_response(self, query: str, engine):
        ''' 
        Evaluate the quality of the response to a query
        
        Args:
            query (str): The query to evaluate
            engine (SearchEngine): The search engine to use for evaluation
        '''
        contexts = engine.query_retriever(query)
        response = engine.generate_response(query, contexts)
        
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
    
    def estimate_cost(documents, model = 'text-embedding-3-small'):
        ''' 
        Estimate the cost of generating embeddings for a list of documents
        
        Args: 
            documents (List[Document]): List of documents to generate embeddings for
            model (str): The model to use for generating embeddings
        '''
        print(f"Estimating cost for {len(documents)} documents")
        enc = tiktoken.encoding_for_model(model)
        total_tokens = sum(len(enc.encode(doc.page_content)) for doc in documents)
        cost = (total_tokens / 1000000) * .02
        print(f"Estimated cost: ${cost:.2f} for {total_tokens} tokens")
        
if __name__ == "__main__":
    engine = SearchEngine(float('inf'), float('inf'))
    Evaluate.estimate_cost(engine.documents)
    