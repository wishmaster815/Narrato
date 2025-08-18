from langgraph.graph import START, END, StateGraph
from src.llms.groqllm import GroqLLM
from src.states.blog_state import BlogState
from src.nodes.blog_node import BlogNode
class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.builder = StateGraph(BlogState)
    
    def build_topic_graph(self):
        """
        create a graph to generate content
        """

        blog_node_obj = BlogNode(llm = self.llm)
        # nodes
        self.builder.add_node("title_creation",blog_node_obj.title_creation)
        self.builder.add_node("content_generator",blog_node_obj.content_generation)

        # edges
        self.builder.add_edge(START, "title_creation")
        self.builder.add_edge("title_creation", "content_generator")
        self.builder.add_edge("content_generator", END)
        
        return self.builder
