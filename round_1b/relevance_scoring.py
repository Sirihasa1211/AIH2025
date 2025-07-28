import numpy as np
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class HybridScorer:
    def __init__(self,
                 embedding_model_name='all-MiniLM-L12-v2',
                 embedding_weight=0.8,
                 keyword_weight=0.2,
                 max_keywords=10):
        self.embedder = SentenceTransformer(embedding_model_name)
        self.kw_model = KeyBERT(model=self.embedder)
        self.embedding_weight = embedding_weight
        self.keyword_weight = keyword_weight
        self.max_keywords = max_keywords

    def keyword_score(self, keywords, text):
        text_lower = text.lower()
        count = sum(1 for kw in keywords if kw.lower() in text_lower)
        return count / max(len(keywords), 1)

    def score_sections(self, query_text, sections_data):
        """
        Input:
          - query_text: concatenated persona + JTBD string
          - sections_data: list of dicts with 'text' key containing section text
        Returns:
          list of tuples: (section_index, hybrid_score, semantic_score, keyword_score)
          sorted descending by hybrid_score
        """
        # Compute embeddings
        query_embedding = self.embedder.encode(query_text, convert_to_numpy=True)
        texts = [s['text'] for s in sections_data]
        section_embeddings = self.embedder.encode(texts, convert_to_numpy=True, batch_size=16)

        # Semantic similarity
        semantic_scores = cosine_similarity([query_embedding], section_embeddings)[0]

        # Extract keywords from query
        keywords_scores = self.kw_model.extract_keywords(query_text,
                                                        keyphrase_ngram_range=(1, 2),
                                                        top_n=self.max_keywords,
                                                        stop_words='english')
        keywords = [kw for kw, score in keywords_scores]

        # Keyword overlap scores
        keyword_scores = np.array([self.keyword_score(keywords, text) for text in texts])

        # Hybrid weighted score
        hybrid_scores = (self.embedding_weight * semantic_scores) + (self.keyword_weight * keyword_scores)

        results = [(idx, hybrid_scores[idx], semantic_scores[idx], keyword_scores[idx]) for idx in range(len(sections_data))]
        results.sort(key=lambda x: x[1], reverse=True)
        return results
