import wikipediaapi
import json
import signal
import sys

class WikiGenerator:   
    def __init__(self):
        self.wiki_wiki = wikipediaapi.Wikipedia(
            user_agent='RAG Testing (lavalampcoder@gmail.com)', 
            language='en'
        )
        self.interrupted = False
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        print("\nSaving current progress...")
        self.interrupted = True

    def get_category_members(self, category, max_level=1, maxCount = float('inf'), counter=None):
        """
        Recursively fetches all pages in a category and its subcategories.
        """
        members = []
        
        if counter is None:
            counter = {"count": 0}  # Use a dict to allow modification in recursive calls
        elif counter["count"] >= maxCount or self.interrupted:
            return members
        
        if not category.exists():
            print(f"Category {category.title} doesn't exist!")
            return members
            
        for c in category.categorymembers.values():
            if c.ns == wikipediaapi.Namespace.CATEGORY and max_level > 0:
                # Recursively fetch subcategories
                members.extend(self.get_category_members(c, max_level - 1, maxCount,  counter))
            elif c.ns == wikipediaapi.Namespace.MAIN:
                # Fetch page details for regular pages
                members.append(self.get_page_details(c))
                counter["count"] += 1
                if counter["count"] % 100 == 0:
                    print(f"Fetched {counter['count']} pages...")
        
        return members
    
    def get_page_details(self, page):
        """
        Extracts the name, title, and categories of a Wikipedia page.
        """
        try:
            dict = {
                "title": page.title,
                "content": page.text,
                "categories": list(page.categories.keys())  # Convert keys view to list for JSON serialization
            }
            return dict
        except Exception as e:
            print(f"Error fetching page details: {e} \n Page: {page}")
            return None

    def save_to_json(self, data, filename):
        """
        Saves the extracted data to a JSON file.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    dataGenerator = DataGenerator()
    
    category_name = "Category:Computer_science"
    cat = dataGenerator.wiki_wiki.page(category_name)

    print(f"Fetching pages in '{category_name}'...")
    pages = dataGenerator.get_category_members(cat, max_level=4, maxCount=1000000)
    
    print(len(pages), "pages fetched.")
    dataGenerator.save_to_json(pages, "./data/computer_science_pages.json")