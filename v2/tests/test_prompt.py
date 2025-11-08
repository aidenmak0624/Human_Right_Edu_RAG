from src.core.rag_system import SimpleRAG

def test_difficulty_levels():
    """Test that different difficulty levels produce appropriate responses"""
    rag = SimpleRAG(preload_topics=True)
    
    test_cases = [
        {
            "query": "What are human rights?",
            "topic": "foundational_rights",
            "difficulties": ["beginner", "intermediate", "advanced"]
        },
        {
            "query": "How does the CRC protect children?",
            "topic": "childrens_rights",
            "difficulties": ["beginner", "intermediate", "advanced"]
        }
    ]
    
    for case in test_cases:
        print(f"\n{'='*60}")
        print(f"Query: {case['query']}")
        print(f"{'='*60}\n")
        
        for difficulty in case["difficulties"]:
            print(f"\n--- {difficulty.upper()} LEVEL ---")
            answer = rag.generate_answer(
                case["query"], 
                case["topic"], 
                difficulty
            )
            print(answer)
            print()

if __name__ == "__main__":
    test_difficulty_levels()
