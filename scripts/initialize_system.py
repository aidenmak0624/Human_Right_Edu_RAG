from src.core.rag_system import SimpleRAG

def initialize_all():
    print("🚀 Initializing complete RAG system...")
    rag = SimpleRAG()
    rag.load_all_topics()
    print("✅ System ready!")

if __name__ == '__main__':
    initialize_all()