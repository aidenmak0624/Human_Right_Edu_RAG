# scripts/smoke_test.py
from src.core.rag_system import SimpleRAG

if __name__ == "__main__":
    rag = SimpleRAG(preload_topics=True)
    cases = [
        ("What is the CRC?", "childrens_rights"),
        ("What is CEDAW?", "womens_rights"),
        ("What are human rights?", "foundational_rights"),
    ]
    for q, t in cases:
        print("\n" + "="*60)
        print(f"❓ {q} | 🗂 {t}")
        print(rag.generate_answer(q, t)[:1200])
