"""
Comprehensive RAG testing
Test different query types, topics, and edge cases
"""

import sys
sys.path.append('.')

from src.core.rag_system import SimpleRAG

def test_all_topics():
    """Test that all 9 topics work"""
    print("=" * 60)
    print("🧪 Testing All 9 Topics")
    print("=" * 60)
    
    rag = SimpleRAG()
    
    # Test queries for each topic
    test_cases = [
        ("What are human rights?", "foundational_rights"),
        ("What is the CRC?", "childrens_rights"),
        ("What is CEDAW?", "womens_rights"),
        ("What is UNDRIP?", "indigenous_rights"),
        ("What are minority rights?", "minority_rights"),
        ("What is freedom of speech?", "freedom_expression"),
        ("What is the ICCPR?", "civil_political_rights"),
        ("What is the right to education?", "right_to_education"),
        ("What are economic rights?", "economic_social_cultural"),
    ]
    
    passed = 0
    failed = 0
    
    for query, topic in test_cases:
        print(f"\n📝 Testing: {topic}")
        print(f"   Query: {query}")
        
        try:
            answer = rag.generate_answer(query, topic)
            
            # Check if answer is reasonable
            if len(answer) > 50 and "couldn't find" not in answer.lower():
                print(f"   ✅ PASS - Got answer ({len(answer)} chars)")
                passed += 1
            else:
                print(f"   ⚠️  WARN - Answer too short or not found")
                print(f"   Answer: {answer[:100]}...")
                failed += 1
                
        except Exception as e:
            print(f"   ❌ FAIL - Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return passed, failed


def test_retrieval_quality():
    """Test that retrieval returns relevant content"""
    print("\n" + "=" * 60)
    print("🧪 Testing Retrieval Quality")
    print("=" * 60)
    
    rag = SimpleRAG()
    
    # Test retrieval without generation
    query = "What are the rights of children?"
    topic = "childrens_rights"
    
    print(f"\nQuery: {query}")
    print(f"Topic: {topic}\n")
    
    results = rag.retrieve(query, topic, n_results=3)
    
    if results and results['documents'][0]:
        print(f"✅ Retrieved {len(results['documents'][0])} chunks")
        
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            print(f"\n--- Chunk {i+1} ---")
            print(f"Source: {metadata.get('source', 'Unknown')}")
            print(f"Preview: {doc[:200]}...")
            
        return True
    else:
        print("❌ No results retrieved")
        return False


def test_different_query_types():
    """Test different types of questions"""
    print("\n" + "=" * 60)
    print("🧪 Testing Different Query Types")
    print("=" * 60)
    
    rag = SimpleRAG()
    
    query_types = [
        ("Definition", "What is the UDHR?", "foundational_rights"),
        ("Specific Article", "What does Article 1 say?", "foundational_rights"),
        ("Concept", "Why are human rights important?", "foundational_rights"),
        ("Date/Fact", "When was the CRC adopted?", "childrens_rights"),
        ("List", "What are the core principles of children's rights?", "childrens_rights"),
        ("Comparison", "How does CEDAW protect women?", "womens_rights"),
    ]
    
    for query_type, query, topic in query_types:
        print(f"\n📝 {query_type} Query")
        print(f"   Q: {query}")
        
        try:
            answer = rag.generate_answer(query, topic)
            print(f"   ✅ Got answer ({len(answer)} chars)")
            
            # Show first 150 chars of answer
            print(f"   Preview: {answer[:150]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")


def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n" + "=" * 60)
    print("🧪 Testing Edge Cases")
    print("=" * 60)
    
    rag = SimpleRAG()
    
    # Test 1: Very short query
    print("\n1. Very short query:")
    answer = rag.generate_answer("CRC?", "childrens_rights")
    print(f"   {'✅ Handled' if answer else '❌ Failed'}")
    
    # Test 2: Unrelated query
    print("\n2. Completely unrelated query:")
    answer = rag.generate_answer("What is the weather today?", "foundational_rights")
    print(f"   Answer: {answer[:100]}...")
    
    # Test 3: Very long query
    print("\n3. Very long query:")
    long_query = "Can you please explain in great detail with multiple examples " * 5 + "what are human rights?"
    answer = rag.generate_answer(long_query, "foundational_rights")
    print(f"   {'✅ Handled' if answer else '❌ Failed'}")
    
    # Test 4: Query with special characters
    print("\n4. Query with special characters:")
    answer = rag.generate_answer("What's the CRC's main goal?", "childrens_rights")
    print(f"   {'✅ Handled' if answer else '❌ Failed'}")


def run_all_tests():
    """Run all test suites"""
    print("\n")
    print("🚀 " + "=" * 58 + " 🚀")
    print("    COMPREHENSIVE RAG SYSTEM TEST SUITE")
    print("🚀 " + "=" * 58 + " 🚀")
    
    # Run tests
    test_all_topics()
    test_retrieval_quality()
    test_different_query_types()
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\nNext: Review results and fix any issues")


if __name__ == '__main__':
    run_all_tests()