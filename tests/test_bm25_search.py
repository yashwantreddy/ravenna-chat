# tests/test_bm25_search.py
import pytest
from app.search.bm25_search import BM25Searcher

# Mock data for testing
MOCK_TICKETS = [
    {
        "ticket_id": "001",
        "customer_question": "How do I reset my password?",
        "support_agent_response": "To reset your password, go to the login page and click 'Forgot Password'.",
        "tags": ["password", "reset", "login"]
    },
    {
        "ticket_id": "002",
        "customer_question": "Can I upgrade my subscription plan?",
        "support_agent_response": "Yes, you can upgrade your plan in the account settings.",
        "tags": ["subscription", "upgrade", "account"]
    },
    {
        "ticket_id": "003",
        "customer_question": "What is your refund policy?",
        "support_agent_response": "Our refund policy allows returns within 30 days of purchase.",
        "tags": ["refund", "policy", "purchase"]
    }
]

@pytest.fixture
def mock_load_zendesk_tickets(monkeypatch):
    def mock_load():
        return MOCK_TICKETS
    monkeypatch.setattr("app.search.bm25_search.load_zendesk_tickets", mock_load)

@pytest.fixture
def bm25_searcher(mock_load_zendesk_tickets):
    return BM25Searcher(threshold=1.0, tag_boost=1.0)

def test_search_exact_match(bm25_searcher):
    query = "How do I reset my password?"
    results, scores = bm25_searcher.search(query)
    assert len(results) == 3  # We always return top 3 results
    assert results[0]['ticket_id'] == "001"
    assert scores[0] > scores[1]  # First result should have highest score

def test_search_partial_match(bm25_searcher):
    query = "upgrade subscription"
    results, scores = bm25_searcher.search(query)
    assert results[0]['ticket_id'] == "002"
    assert "subscription" in results[0]['tags']

def test_search_with_tags(bm25_searcher):
    query = "account upgrade"
    results, scores = bm25_searcher.search(query)
    assert results[0]['ticket_id'] == "002"  # Should match due to 'account' tag
    assert scores[0] > 1.0  # Score should be boosted due to tag match

def test_is_query_supported(bm25_searcher):
    supported_query = "reset password"
    unsupported_query = "unrelated topic"
    
    supported_results, supported_scores = bm25_searcher.search(supported_query)
    unsupported_results, unsupported_scores = bm25_searcher.search(unsupported_query)
    
    assert bm25_searcher.is_query_supported(supported_scores) == True
    assert bm25_searcher.is_query_supported(unsupported_scores) == False

def test_preprocess(bm25_searcher):
    text = "How do I Reset my PASSWORD?"
    processed = bm25_searcher._preprocess(text)
    assert processed == ['how', 'do', 'i', 'reset', 'my', 'password']

def test_get_tags(bm25_searcher):
    text = "Reset account password"
    tags = bm25_searcher._get_tags(text)
    assert set(tags) == {'reset', 'account', 'password'}

def test_search_no_results(bm25_searcher):
    query = "completely unrelated query"
    results, scores = bm25_searcher.search(query)
    assert len(results) == 3  # Should still return top 3, even if not relevant
    assert all(score < bm25_searcher.threshold for score in scores)

def test_tag_boosting(bm25_searcher):
    query_with_tag = "login issues"
    query_without_tag = "issues"
    
    results_with_tag, scores_with_tag = bm25_searcher.search(query_with_tag)
    results_without_tag, scores_without_tag = bm25_searcher.search(query_without_tag)
    
    assert scores_with_tag[0] > scores_without_tag[0]  # Tag match should boost score

if __name__ == "__main__":
    pytest.main()