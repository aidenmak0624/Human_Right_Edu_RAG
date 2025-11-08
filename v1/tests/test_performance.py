"""
Test RAG system performance
Measure response times and quality
"""

import sys
sys.path.append('.')

import time
from src.core.rag_system import SimpleRAG

def test_response_time():
    """Measure average response time"""
    print("⏱️  Testing Response Times...")
    
    rag = SimpleRAG()
    
    queries = [
        ("What are human rights?", "foundational_rights"),
        ("What is the CRC?", "childrens_rights"),
        ("What is CEDAW?", "womens_rights"),
    ]
    
    times = []
    
    for query, topic in queries:
        start = time.time()
        answer = rag.generate_answer(query, topic)
        end = time.time()
        
        elapsed = end - start
        times.append(elapsed)
        
        print(f"  {topic}: {elapsed:.2f}s")
    
    avg_time = sum(times) / len(times)
    print(f"\n  Average: {avg_time:.2f}s")
    
    if avg_time < 3:
        print("  ✅ Performance: Excellent (< 3s)")
    elif avg_time < 5:
        print("  ✅ Performance: Good (< 5s)")
    else:
        print("  ⚠️  Performance: Slow (> 5s)")
    
    return avg_time


def test_retrieval_speed():
    """Measure retrieval-only speed"""
    print("\n⚡ Testing Retrieval Speed...")
    
    rag = SimpleRAG()
    
    start = time.time()
    results = rag.retrieve("What are human rights?", "foundational_rights", n_results=3)
    end = time.time()
    
    elapsed = end - start
    print(f"  Retrieval time: {elapsed:.3f}s")
    
    if elapsed < 0.5:
        print("  ✅ Retrieval: Very Fast")
    elif elapsed < 1.0:
        print("  ✅ Retrieval: Fast")
    else:
        print("  ⚠️  Retrieval: Could be faster")


def run_performance_tests():
    print("=" * 60)
    print("⚡ PERFORMANCE TESTING")
    print("=" * 60)
    
    test_response_time()
    test_retrieval_speed()
    
    print("\n" + "=" * 60)
    print("✅ Performance tests complete")
    print("=" * 60)


if __name__ == '__main__':
    run_performance_tests()