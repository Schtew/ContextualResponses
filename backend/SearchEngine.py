import os
from DataLoader import DataLoader
from Evaluate import Evaluate
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

class SearchEngine:
    #For Flask implementation, utilize generate response to sort between perfered sources, not init. 1 init per page reload for now (should be account/instance in theory)
    def __init__(self, arXiv = float('inf'), wiki = float('inf')):
        """
        Initialize the SearchEngine with an optional number of arXiv papers to load.

        Args:
            arVix (int, optional): Number of papers to load. If 0, source arXiv will not be used.
            wiki (int, optional): Same as stated
        """
        self.key = os.environ.get('OPENAI_API_KEY')
        self.model = ChatOpenAI(model="gpt-3.5-turbo-0125")
        self.embedding = OpenAIEmbeddings(model='text-embedding-3-small')
        if os.path.exists("faiss_index/index.faiss"):
            print("Utilizing cached vectorstore...")
            self.vectorstore = FAISS.load_local('faiss_index', self.embedding, allow_dangerous_deserialization=True)
        else: 
            print("Creating vectorstore...")
            self.documents = []            
            if arXiv:
                self.documents = DataLoader.load_arxiv_papers('data/arxiv-metadata-oai-snapshot.json', arXiv)
            if wiki:
                self.documents += DataLoader.load_wikipedia_pages('data/computer_science_pages_cleaned.json', wiki)
            self.vectorstore = FAISS.from_documents(documents=self.documents, embedding=self.embedding)
            self.vectorstore.save_local("faiss_index")
        
    def _cache_exists(self, cache_dir: str = "cache/"):
        return os.path.exists(os.path.join(cache_dir, "faiss_index"))
    
    def query_retriever(self, query, k = 4, arXiv = False, wiki = False, debugging = False):
        """Retrieve relevant contexts based on the query"""
        filter_dict = None
        if arXiv and not wiki:
            filter_dict = {"type": "research_paper"}
        elif wiki and not arXiv:
            filter_dict = {"type": "wikipedia_page"}
        elif arXiv and wiki:
            filter_dict = None
        elif not arXiv and wiki:
            # Return nothing- no context requested
            return []
        results = self.vectorstore.similarity_search(query, k = k, filter=filter_dict)
        if debugging:
            print(results)
        texts = []
        for r in range(len(results)):
            texts.append(results[r].page_content) #Note: Metadata is not used currently
        return texts

    def generate_response(self, query: str, contexts = None, arXiv = False, wiki = False, debugging = False) -> str:
        """Generate a response based on the query and retrieved contexts"""
        if not contexts:
            contexts = self.query_retriever(query, arXiv=arXiv, wiki=wiki, debugging=debugging)
        context_texts = "\n\n".join(contexts)
        # Potentially change prompt if no context is requested.
        prompt = f"""Based on the following contexts, answer the question.
        
        Contexts:
        {context_texts}
        
        Question: {query}
        
        Answer:"""
        
        response = self.model.invoke(prompt)
        return response.content
    
if __name__ == "__main__":
    # docs = DataLoader.load_arxiv_papers('data/arxiv-metadata-oai-snapshot.json')
    # docs += DataLoader.load_wikipedia_pages('data/computer_science_pages_cleaned.json')
    search_engine = SearchEngine()
    result = search_engine.generate_response("What is the impact of quantum computing on cryptography?", None, True, False, True)
    print(result)
    # evaluator = Evaluate()
    # evaluator.estimate_cost(docs)
    # evaluator.evaluate_response("What is the impact of quantum computing on cryptography?", search_engine)
        
        