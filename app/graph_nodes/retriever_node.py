# app/graph_nodes/retriever_node.py
from app.vectorstore.qdrant_client import get_qdrant_retriever  # No cambia

def retriever_node(state):
    # Verifica que 'question' esté en el estado antes de acceder a ella
    if "question" not in state:
        raise ValueError("La clave 'question' no está en el estado.")
    
    retriever = get_qdrant_retriever()

    # Recuperar documentos relevantes de Qdrant usando el historial de la conversación
    context = retriever.get_relevant_documents(state["question"])

    # Agregar contexto adicional si es necesario
    return {"context": context, "conversation_history": state["conversation_history"]}
