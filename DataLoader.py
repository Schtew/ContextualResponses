import pandas as pd
import json
import random
from langchain_core.documents import Document
import re

class DataLoader:
    def load_arxiv_papers(file_path: str, num_papers: int = 1000):
        """
        Load arXiv papers from: https://www.kaggle.com/datasets/Cornell-University/arxiv
        Filters for papers with computer science ('cs') in the categories.
        
        Args:
            file_path: Path to the arxiv-metadata-oai-snapshot.json file
            num_papers: Number of papers to load
            
        Returns:
            List of document dictionaries
        """
        documents = []
        papers_processed = 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    paper = json.loads(line)
                    
                    if not paper.get('categories', '').startswith('cs'):
                        continue
                    # Calculate a random age for the paper (for demo purposes)
                    days_old = random.randint(1, 365)
                    
                    # Clean and combine abstract/title
                    content = f"Title: {paper.get('title', '')}\nAbstract: {paper.get('abstract', '')}"
                    content = content.replace('\n', ' ').strip()
                    
                    doc = Document(
                        page_content=content,
                        metadata={
                            'type': 'research_paper',
                            'department': paper.get('categories', '').split(' '),
                            'days_old': days_old,
                            'authors': re.split(', | and ', paper.get('authors', '')), #TODO: test regex
                            'update_date': paper.get('update_date', ''),
                            'title': paper.get('title', '')
                        }
                    )
                    documents.append(doc)
                    
                    papers_processed += 1
                    if papers_processed >= num_papers:
                        break
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
                    continue
                    
        print(f"Successfully loaded {len(documents)} papers")
        return documents
        
if __name__ == "__main__":
    print(len(DataLoader.load_arxiv_papers('data/arxiv-metadata-oai-snapshot.json', 100)))