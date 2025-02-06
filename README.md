Proof of Concept RAG model which references documents from various sources and to provide contextual LLM responses.

ArXiv-10 database: https://www.kaggle.com/datasets/Cornell-University/arxiv

TODO:
- Implement StackOverflow db and wikipedia db
    - Implement cleaning for StackOverflow and chunking for Wikipedia.
- Rerank results retrieved by similarity with metadata.
    - Implement corresponding retreival evaluations.
- Implement DeepEval for testing generated responses.
    - Find/create a list of expected outputs for eval purposes.
- Consider various prompts.
