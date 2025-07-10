from app.vectorstore.qdrant_client import get_qdrant_retriever  # No cambia

def retriever_node(state):
    # Verifica que 'question' esté en el estado antes de acceder a ella
    if "question" not in state or not state["question"]:
        raise ValueError("La clave 'question' no tiene un valor válido.")
    
    retriever = get_qdrant_retriever()  # Obtener la función envolvente
    
    # Recuperar documentos relevantes de Qdrant usando la pregunta
    context = retriever(state["question"])  # type: ignore # Llamar a la función envolvente
    
    # Asegurarnos de que los documentos tienen contenido válido
    for i, doc in enumerate(context):
        # Verificamos que 'text' exista y sea un string válido
        text_content = doc.get("page_content", None)
        if not text_content or not isinstance(text_content, str):
            # Si el contenido no es válido, creamos un nuevo Document con el valor predeterminado
            context[i] = doc.__class__(page_content="No se encontró información relevante.", **doc.dict())  # type: ignore # Crear un nuevo Document con contenido predeterminado
    
    # Agregar contexto adicional si es necesario
    return {"context": context, "conversation_history": state["conversation_history"]}


