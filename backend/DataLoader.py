import pandas as pd
import json
import datetime
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
                    # days_old = random.randint(1, 365)
                    
                    # Clean and combine abstract/title
                    content = f"Title: {paper.get('title', '')}\nAbstract: {paper.get('abstract', '')}"
                    content = content.replace('\n', ' ').strip()
                    
                    doc = Document(
                        page_content=content,
                        metadata={
                            'type': 'research_paper',
                            'categories': paper.get('categories', '').split(' '),
                            # 'days_old': days_old,
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
        
    def load_wikipedia_pages(file_path: str, num_pages: int = 1000):
        """
        Load wikipedia pages from gathered from WikiGenerator.py
        Filters for pages that are a subcategory of 'Computer Science'.
        
        Args:
            file_path: Path to the wikipedia json file
            num_papers: Number of papers to load
            
        Returns:
            List of document objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.loads(file.read())
                limited_data = data[:num_pages] if num_pages < len(data) else data
                documents = []
                for item in limited_data:
                    doc = Document(
                        page_content=item['content'],
                        metadata={
                            'type': 'wikipedia_page',
                            'title': item['title'],
                            'categories': item['categories']
                        }
                    )
                    documents.append(doc)
                print(f"Successfully loaded {len(documents)} pages")
                return documents
        except Exception as e:
            print(f"Error while loading wikipedia pages: {e}")
            
    
    def check_wikipedia(path = 'data/computer_science_pages.json'):
        """
        Check the attributes of the wikipedia pages and provide detailed information
        about any invalid entries.
        """
        i = 0
        none_count = 0
        invalid_entries = 0
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.loads(file.read())
                print(f"Checking {len(data)} items")
                
                for i, item in enumerate(data, 1):  # start counting at 1
                    if item is None:
                        none_count += 1
                        print(f"Entry {i} is None")
                        continue
                        
                    try:
                        missing_fields = [
                            key for key in ['title', 'content', 'categories'] 
                            if not item.get(key)
                        ]
                        
                        if missing_fields:
                            invalid_entries += 1
                            print(f"Entry {i} is missing fields: {missing_fields}")
                            print(f"Entry content: {item}")
                    except AttributeError:
                        invalid_entries += 1
                        print(f"Entry {i} is invalid type: {type(item)}")
                        print(f"Entry content: {item}")
                        
            # Print summary
            print("\nSummary:")
            print(f"Total entries: {len(data)}")
            print(f"None entries: {none_count}")
            print(f"Invalid entries: {invalid_entries}")
            print(f"Valid entries: {len(data) - none_count - invalid_entries}")
                        
        except Exception as e:
            print(f"Error occurred at entry {i}: {str(e)}")
            raise
            
    def clean_wikipedia(input_path):
        ''' Remove invalid entries from the wikipedia pages file'''
        output_path = input_path[:-5] + '_cleaned' + ".json"
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                data = json.loads(file.read())
            original_count = len(data)
            cleaned_data = [item for item in data if item != None 
                            and all(item.get(key) for key in ['title', 'content', 'categories'])
                            and all(isinstance(item.get(key), str) for key in ['title', 'content'])
                            and isinstance(item.get('categories'), list)
            ]

            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(cleaned_data, file, ensure_ascii=False, indent=2)
            
            print(f'Original entries: {original_count}')
            print(f'Cleaned entries: {len(cleaned_data)}')
            print(f'Cleaned entries: {original_count - len(cleaned_data)}')
            try:
                with open(output_path, 'r', encoding='utf-8') as file:
                    test_read = json.loads(file.read())
                    print("Successfully verified cleaned file is readable")
            except json.JSONDecodeError as e:
                print(f"Error: Cleaned file is not valid JSON: {e}")
        except Exception as e:
            print(f"Error occurred while cleaning data: {e}")
        
            


if __name__ == "__main__":
    # print(len(DataLoader.load_arxiv_papers('data/arxiv-metadata-oai-snapshot.json', 100)))
    # print(len(DataLoader.load_wikipedia_pages('data/computer_science_pages.json', 1000)))
    # DataLoader.clean_wikipedia('data/computer_science_pages.json')
    DataLoader.check_wikipedia('data/computer_science_pages_cleaned.json')
    