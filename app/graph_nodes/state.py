# app/graph_nodes/state.py
from typing import Any, Dict
from typing_extensions import TypedDict

class State(TypedDict):
    messages: Any  # Esto puede ser una lista de mensajes u otra estructura de datos
    phone: str
    chatType: str
    data_user: Any
    retrival: Any
    system_message: str
    token_usage: Dict[str, Any]
