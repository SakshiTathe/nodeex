# knowledge_graph_service.py
# knowledge_graph_service.py
import networkx as nx
import os
import pickle

class KnowledgeGraphService:
    def __init__(self, graph_path="user_knowledge_graph.gpickle"):
        self.graph_path = graph_path
        if os.path.exists(graph_path):
            try:
                self.graph = nx.read_gpickle(graph_path)
                print("📂 Loaded existing Knowledge Graph.")
            except Exception:
                with open(graph_path, "rb") as f:
                    self.graph = pickle.load(f)
                print("📂 Loaded Knowledge Graph using pickle (compatibility mode).")
        else:
            self.graph = nx.Graph()
            print("🆕 Created new Knowledge Graph.")

    def add_user_chat(self, user_id, message, emotion, disease, topic):
        node_label = f"{user_id}_{topic}_{emotion}"
        self.graph.add_node(
            node_label,
            type="UserMessage",
            message=message,
            emotion=emotion,
            topic=topic
        )

        # link with disease
        if disease:
            if disease not in self.graph.nodes:
                self.graph.add_node(disease, type="Disease")
            self.graph.add_edge(node_label, disease, relation="related_to")

        # Save the graph safely
        try:
            nx.write_gpickle(self.graph, self.graph_path)
        except Exception:
            with open(self.graph_path, "wb") as f:
                pickle.dump(self.graph, f)

        print(f"💬 Added message for {user_id} (emotion: {emotion}, topic: {topic})")
