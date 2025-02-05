import os
from DataLoader import DataLoader
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


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
        self.documents = []
        if arXiv:
            self.documents = DataLoader.load_arxiv_papers('Data/arxiv-metadata-oai-snapshot.json', arXiv)
        print(self.documents[0])
        self.vectorstore = FAISS.from_documents(documents=self.documents, embedding=self.embedding)
        
    def search(self, query, k = 4):
        results = self.vectorstore.similarity_search(query, k = k)
        return results
    
if __name__ == "__main__":
    search_engine = SearchEngine()
    results = search_engine.search("What is the impact of quantum computing on cryptography?")
    print(results[:5])
        
        
        