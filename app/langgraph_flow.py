# app/langgraph_flow.py
from langgraph.graph import StateGraph  # Asegúrate de importar StateGraph
from app.graph_nodes.input_node import input_node  # Importar la función input_node
from app.graph_nodes.retriever_node import retriever_node  # Importar la función retriever_node
from app.graph_nodes.advisor_node import advisor_node  # Importar la función advisor_node
from app.graph_nodes.state import State  # Importar el TypedDict State

def build_langgraph():
    # Crear StateGraph usando el TypedDict State
    graph_builder = StateGraph(State)

    # Añadir nodos
    graph_builder.add_node("input", input_node)  # input_node debería agregar "question" al estado
    graph_builder.add_node("retriever", retriever_node)  # Asegúrate de que el estado tiene la clave 'question'
    graph_builder.add_node("advisor", advisor_node)  # Agregar el nodo advisor
    
    # Asegúrate de que el estado se pase correctamente entre nodos
    graph_builder.add_edge("input", "retriever")
    graph_builder.add_edge("retriever", "advisor")
    
    # Configura el punto de entrada y salida
    graph_builder.set_entry_point("input")
    graph_builder.set_finish_point("advisor")

    # Compila el grafo
    compiled_graph = graph_builder.compile()

    return compiled_graph
