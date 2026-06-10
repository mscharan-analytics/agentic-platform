import asyncio
from agent_platform import OllamaRAG, RAGDocument
from agent_platform.model_gateway import get_model_gateway, ModelProvider


def test_model_gateway_invoke_langchain_fallback() -> None:
    gateway = get_model_gateway()
    response = asyncio.run(gateway.invoke("Hello, model! Are you there?", model="llama2"))
    
    assert response.provider == ModelProvider.OLLAMA
    # Should complete either using actual ChatOllama or falling back cleanly to the stub response
    assert response.content is not None
    assert len(response.content) > 0


def test_rag_document_retrieval() -> None:
    rag = OllamaRAG()
    
    docs = [
        RAGDocument(content="The project security policy requires multi-factor authentication for administrative users."),
        RAGDocument(content="Developers must use Python 3.11 or higher for all backend microservices."),
        RAGDocument(content="Docker images must be built and validated in the CI/CD pipeline before release."),
    ]
    
    asyncio.run(rag.add_documents(docs))
    
    # Query for Python version constraint
    results = asyncio.run(rag.query("What Python version is required for services?", k=1))
    
    assert len(results) == 1
    assert "Python 3.11" in results[0].content
    
    # Query for security requirements
    results_sec = asyncio.run(rag.query("admin MFA controls", k=1))
    assert len(results_sec) == 1
    assert "multi-factor authentication" in results_sec[0].content
