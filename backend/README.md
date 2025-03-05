Proof of Concept RAG model which references documents from various sources and to provide contextual LLM responses.

ArXiv-10 database: https://www.kaggle.com/datasets/Cornell-University/arxiv

TODO:
- Rerank results retrieved by similarity with metadata. Wiki results overweighed at the moment.
- Find/create a list of expected outputs for eval purposes. 
- Consider various prompts. 
- Implement Flask for backend.

Completed:
- Implement Wikipedia db ✅
    - Implement chunking for Wikipedia. ✅
- Implement DeepEval for testing generated responses. ✅
- Add React front end. ✅
- Implement local vector storage for faster retrieval and cost savings. ✅
