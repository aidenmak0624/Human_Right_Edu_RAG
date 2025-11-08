# --- put telemetry env flags BEFORE importing chromadb ---
import os
os.environ["CHROMADB_ANONYMIZED_TELEMETRY"] = "false"
os.environ["CHROMADB_TELEMETRY_IMPL"] = "none"  # some versions still read this

# src/core/rag_system.py
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from chromadb.config import Settings
import google.generativeai as genai


class SimpleRAG:
    """Basic RAG system for human rights education"""

    def __init__(self, persist_directory: str = "./chromadb", topics_dir: str = "data/processed",preload_topics: bool = True):
        print("🔧 Initializing RAG system...")

        # --- 0) Env & Keys ---
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not set. Put it in your .env and NEVER hardcode keys in code.")
        genai.configure(api_key=api_key)

        # --- 1) LLM ---
        self.model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        print("✅ Gemini model ready")

        # --- 2) Embeddings ---
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("✅ Embedding model loaded")

        # --- 3) Vector DB (Chroma) ---
        persist_path = Path(persist_directory)
        persist_path.mkdir(parents=True, exist_ok=True)
        self.chroma_client = PersistentClient(
            path=str(persist_path),
            settings=Settings(anonymized_telemetry=False)
        )
        print(f"✅ ChromaDB ready at {persist_path.resolve()}")

        # --- 4) State (init ONCE) ---
        self.collections: Dict[str, any] = {}
        self.topics_dir = Path(topics_dir)
        self.topics: List[str] = self._discover_topics()
        print(f"✅ Discovered topics: {self.topics}")
        print("✅ Default collection ready")
        
        if preload_topics:
            self.load_all_topics()

    # ---------- Utilities ----------
    def _discover_topics(self) -> List[str]:
        if not self.topics_dir.exists():
            return []
        return [p.name for p in self.topics_dir.iterdir() if p.is_dir()]

    def _get_or_create_collection(self, name: str):
        if name in self.collections:
            return self.collections[name]
        col = self.chroma_client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine", "description": f"Documents for {name}"}
        )
        self.collections[name] = col
        return col
    # ---------- Ingestion ----------

    def load_documents_for_topic(self, topic_name: str, min_chunk_len: int = 50):
        """Load documents under data/processed/{topic_name}/*.txt into Chroma"""
        topic_dir = self.topics_dir / topic_name
        print(f"📚 Loading documents for '{topic_name}' from {topic_dir} ...")

        if not topic_dir.exists():
            print(f"⚠️  No documents found for {topic_name} (dir not found)")
            return

        collection = self._get_or_create_collection(topic_name)


        doc_count, chunk_count = 0, 0
        for txt_file in topic_dir.glob("*.txt"):
            content = txt_file.read_text(encoding="utf-8", errors="ignore")
            chunks = [p.strip() for p in content.split("\n\n") if p.strip() and len(p.strip()) > min_chunk_len]
            if not chunks:
                continue

            # vectorize in batch
            embeddings = self.embedding_model.encode(chunks, batch_size=32, convert_to_numpy=True).tolist()

            # stable IDs (content hash) to make ingestion idempotent
            import hashlib
            def _cid(stem, i, text):
                h = hashlib.blake2b(text.encode("utf-8"), digest_size=8).hexdigest()
                return f"{stem}_c{i}_{h}"

            ids = [_cid(txt_file.stem, i, ch) for i, ch in enumerate(chunks)]
            metadatas = [{"source": txt_file.name, "topic": topic_name, "chunk_id": i} for i in range(len(chunks))]

            # requires chromadb 0.5.x
            collection.upsert(
                documents=chunks,
                embeddings=embeddings,
                ids=ids,
                metadatas=metadatas
            )
            doc_count += 1
            chunk_count += len(chunks)

        print(f"✅ Loaded {doc_count} docs ({chunk_count} chunks) -> collection '{topic_name}'")

    def load_all_topics(self):
        if not self.topics:
            print("⚠️  No topic folders found under data/processed")
            return
        print(f"📚 Loading all topics: {self.topics}")
        for topic in self.topics:
            self.load_documents_for_topic(topic)
        print("✅ All topics loaded")

    # ---------- Retrieval ----------
    def retrieve(self, query: str, topic: str, n_results: int = 6):
        # lazy-load if needed
        if topic not in self.collections:
            self.load_documents_for_topic(topic)
        if topic not in self.collections:
            print(f"⚠️  Topic '{topic}' still not available.")
            return None

        query_emb = self.embedding_model.encode(query, convert_to_numpy=True).tolist()
        return self.collections[topic].query(
            query_embeddings=[query_emb],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]  # <-- add scores
        )

    # ---------- Generation ----------
    def generate_answer(self, query: str, topic: str, difficulty: str = "intermediate") -> str:
        print(f"\n❓ Question: {query}\n📂 Topic: {topic}")

        results = self.retrieve(query, topic, n_results=4)
        if not results or not results.get("documents") or not results["documents"][0]:
            return "I couldn't find relevant information to answer that question."

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists  = results.get("distances", [[None]*len(docs)])[0]
        rank = sorted(range(len(docs)), key=lambda i: dists[i] if dists[i] is not None else 1e9)[:3]
        context = "\n\n".join(docs[i] for i in rank)
        sources = [f"{metas[i].get('source','?')} (score={dists[i]:.3f})" for i in rank]

        prompt = f"""You are a helpful educational assistant specializing in human rights.

Context from authoritative documents:
{context}

Question: {query}

Instructions:
- Provide a clear, accurate answer based on the context
- Adjust explanation for {difficulty} level
- Be educational and helpful
- If unsure, acknowledge limitations

Answer:"""

        try:
            resp = self.model.generate_content(prompt)
            answer = (getattr(resp, "text", "") or "").strip()
            if not answer:
                answer = "No response generated."
        except Exception as e:
            answer = f"Generation failed: {e}"

        citation = "\n\n📚 Sources: " + ", ".join(sorted(set(sources)))
        return answer + citation


# ---------- Quick test ----------
def test_rag():
    print("=" * 60)
    print("🌍 Testing Human Rights RAG System")
    print("=" * 60)

    rag = SimpleRAG()
    rag.load_documents_for_topic("foundational_rights")

    query = "What are human rights?"
    answer = rag.generate_answer(query, "foundational_rights")

    print("\n" + "=" * 60)
    print("ANSWER:")
    print("=" * 60)
    print(answer)
    print("=" * 60)


if __name__ == "__main__":
    test_rag()
