"""Retrieval-Augmented Generation (RAG) module utilizing local Ollama embeddings."""

from __future__ import annotations

import logging
import math
from typing import Any, List, Dict

logger = logging.getLogger(__name__)


class RAGDocument:
    """Represents a text document stored in the RAG knowledge base."""

    def __init__(self, content: str, metadata: Dict[str, Any] | None = None) -> None:
        self.content = content
        self.metadata = metadata or {}


class OllamaRAG:
    """Manages document chunking, indexing, and vector search querying."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "nomic-embed-text") -> None:
        self.base_url = base_url
        self.model = model
        self.documents: List[RAGDocument] = []
        self._embeddings: List[List[float]] = []
        self._has_langchain = False

        try:
            from langchain_ollama import OllamaEmbeddings
            self._ollama_embeddings = OllamaEmbeddings(base_url=self.base_url, model=self.model)
            self._has_langchain = True
        except ImportError:
            logger.warning("langchain-ollama not installed; running RAG in simulated/fallback mode")
            self._ollama_embeddings = None

    async def add_documents(self, docs: List[RAGDocument]) -> None:
        """Add documents to the index and compute their embeddings."""
        self.documents.extend(docs)
        if not self._has_langchain or not self._ollama_embeddings:
            # Vocabulary-based TF fallback will compute vectors dynamically at query time
            return

        try:
            texts = [doc.content for doc in docs]
            embeddings = await self._ollama_embeddings.aembed_documents(texts)
            self._embeddings.extend(embeddings)
        except Exception as e:
            logger.error(f"Failed to generate real embeddings via Ollama: {e}. Falling back to simulation.")
            self._ollama_embeddings = None

    async def query(self, text: str, k: int = 2) -> List[RAGDocument]:
        """Perform vector similarity search and retrieve top-k matching documents."""
        if not self.documents:
            return []

        # If running in simulated mode (no LangChain or error fetching embeddings)
        if not self._has_langchain or not self._ollama_embeddings:
            import re
            
            def get_words(t: str) -> List[str]:
                return re.findall(r'\w+', t.lower())

            all_docs_words = [get_words(doc.content) for doc in self.documents]
            query_words = get_words(text)

            # Build a dynamic vocabulary
            vocab = list(set(word for doc in all_docs_words for word in doc))
            if not vocab:
                return self.documents[:k]

            vocab_index = {word: idx for idx, word in enumerate(vocab)}

            def get_tf_vector(words: List[str]) -> List[float]:
                vec = [0.0] * len(vocab)
                for w in words:
                    if w in vocab_index:
                        vec[vocab_index[w]] += 1.0
                return vec

            query_vector = get_tf_vector(query_words)
            embeddings = [get_tf_vector(doc_words) for doc_words in all_docs_words]
        else:
            try:
                query_vector = await self._ollama_embeddings.aembed_query(text)
            except Exception as e:
                logger.error(f"Failed to embed query: {e}. Falling back to simulation.")
                # Force fallback evaluation
                self._ollama_embeddings = None
                return await self.query(text, k)
            embeddings = self._embeddings

        def dot_product(v1: List[float], v2: List[float]) -> float:
            return sum(x * y for x, y in zip(v1, v2))

        def magnitude(v: List[float]) -> float:
            return math.sqrt(sum(x * x for x in v))

        similarities = []
        for idx, doc_vector in enumerate(embeddings):
            mag1 = magnitude(query_vector)
            mag2 = magnitude(doc_vector)
            if mag1 == 0 or mag2 == 0:
                sim = 0.0
            else:
                sim = dot_product(query_vector, doc_vector) / (mag1 * mag2)
            similarities.append((sim, self.documents[idx]))

        # Sort by similarity score descending
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in similarities[:k]]
