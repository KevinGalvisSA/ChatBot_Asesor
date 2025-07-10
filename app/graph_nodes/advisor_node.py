# app/graph_nodes/advisor_node.py
from langchain.chains import ConversationalRetrievalChain  # Actualizado
from app.utils.gemini_wrapper import get_gemini_llm
from app.vectorstore.qdrant_client import get_qdrant_retriever  # No cambia
from app.utils.prompts import get_reformat_prompt, get_conversation_summary_prompt, get_detection_prompt  # Importar los prompts

llm = get_gemini_llm()

def advisor_node(state):
    # Verificar que 'question' esté en el estado antes de acceder a ella
    if "question" not in state:
        raise ValueError("La clave 'question' no está en el estado.")
    
    retriever = get_qdrant_retriever()
    chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever)
    
    # Extraer y actualizar los datos del usuario usando get_detection_prompt
    user_message = state["question"]
    user_data = state.get("user_data", {})
    
    # Detectar el nombre y teléfono usando get_detection_prompt
    detection_prompt = get_detection_prompt(user_message, user_data)
    
    # Usar el modelo para predecir el nombre y teléfono del usuario
    detected_data = llm.predict(detection_prompt) # type: ignore
    updated_user_data = {
        "username": detected_data.get("nombre", user_data.get("username", "Desconocido")),
        "phone": detected_data.get("telefono", user_data.get("phone", "Desconocido"))
    }
    
    # Actualizar el estado con los nuevos datos del usuario
    state["user_data"] = updated_user_data

    # Realizar la consulta para obtener la respuesta
    question = state["question"]
    context_docs = state["context"]
    inputs = {
        "question": question,
        "chat_history": state["conversation_history"],
        "context": context_docs,
    }
    
    result = chain(inputs)
    
    # Obtener la respuesta y reformatearla
    agent_response = result["answer"]
    formatted_response = get_reformat_prompt(
        user_question=question,
        agent_response=agent_response,
        chat_type="chat",  # Si es un chat, o ajusta según el tipo de conversación
        user_data=state["user_data"],
        history=state["conversation_history"],
        retrival=context_docs
    )
    
    # Si es necesario, hacer un resumen de la conversación
    if len(state["conversation_history"]) > 5:  # Límite de mensajes para generar resumen
        summary_prompt = get_conversation_summary_prompt(state["conversation_history"])
        summary = llm.predict(summary_prompt) # type: ignore
        return {"response": formatted_response, "summary": summary}
    
    return {"response": formatted_response}
