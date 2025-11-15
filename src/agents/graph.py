from langgraph.graph import END, StateGraph

from src.agents.nodes.query_router import QueryClassifier
from src.agents.nodes.simple_agent import SimpleAgent
from src.agents.nodes.tsmc_agent import TSMCStockSearchAgent
from src.agents.nodes.mtk_agent import MTKStockSearchAgent
from src.agents.state import ChatState

def run_graph(config: dict, user_input: str, session_id: str):
    builder = StateGraph(ChatState)
    
    builder.add_node("QueryClassifier", QueryClassifier(config))
    builder.add_node("SimpleAgent", SimpleAgent(config, session_id))
    builder.add_node("TSMCStockSearchAgent", TSMCStockSearchAgent(config, session_id))
    builder.add_node("MTKStockSearchAgent", MTKStockSearchAgent(config, session_id))
    builder.set_entry_point("QueryClassifier")
    builder.add_conditional_edges(
    "QueryClassifier",
    lambda state: state["intent"],
    {
        "tsmc": "TSMCStockSearchAgent",
        "mtk": "MTKStockSearchAgent",
        "others": "SimpleAgent"
    }
    )
    builder.add_edge("TSMCStockSearchAgent", END)
    builder.add_edge("MTKStockSearchAgent", END)
    builder.add_edge("SimpleAgent", END)
    graph = builder.compile()
    state = {"input": user_input, "history": None, "intent": None, "response": None}
    result = graph.invoke(state)
    return result.get("response")
