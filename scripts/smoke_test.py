# test_queries.py
from src.core.rag_system import SimpleRAG

rag = SimpleRAG()
rag.load_all_topics()

# Test queries for different topics
test_queries = [
    ("What is the CRC?", "childrens_rights"),
    ("What is CEDAW?", "womens_rights"),
    ("What are human rights?", "foundational_rights"),
]

for query, topic in test_queries:
    print("\n" + "="*60)
    answer = rag.generate_answer(query, topic)
    print(answer)