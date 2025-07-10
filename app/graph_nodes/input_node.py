# app/graph_nodes/input_node.py
def input_node(state):
    # Verifica si 'question' está en el estado antes de pasarla
    if "question" not in state:
        raise ValueError("La clave 'question' no está en el estado.")
    
    return {"question": state["question"]}
