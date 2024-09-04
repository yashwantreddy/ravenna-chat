# app/search/bm25_search.py
from rank_bm25 import BM25Okapi
from typing import List, Dict, Tuple
import re
from app.utils.data_loader import load_zendesk_tickets

class BM25Searcher:
    def __init__(self, threshold: float = 2.0, tag_boost: float = 2.0):
        self.tickets = load_zendesk_tickets()
        self.tokenized_corpus = [self._preprocess(ticket['customer_question']) for ticket in self.tickets]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self.threshold = threshold
        self.tag_boost = tag_boost

    def _preprocess(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    def _get_tags(self, text: str) -> List[str]:
        # Extract potential tags from the text
        return re.findall(r'\b\w+\b', text.lower())

    def search(self, query: str, top_k: int = 3) -> Tuple[List[Dict], List[float]]:
        tokenized_query = self._preprocess(query)
        query_tags = self._get_tags(query)
        
        doc_scores = self.bm25.get_scores(tokenized_query)
        
        # Adjust scores based on tag matches
        for i, ticket in enumerate(self.tickets):
            ticket_tags = set(tag.lower() for tag in ticket['tags'])
            matching_tags = set(query_tags) & ticket_tags
            doc_scores[i] += len(matching_tags) * self.tag_boost

        top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]
        top_tickets = [self.tickets[i] for i in top_indices]
        top_scores = [doc_scores[i] for i in top_indices]
        return top_tickets, top_scores

    def is_query_supported(self, scores: List[float]) -> bool:
        return any(score >= self.threshold for score in scores)
