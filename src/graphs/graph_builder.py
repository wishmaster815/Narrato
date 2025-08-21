from langgraph.graph import START, END, StateGraph
from src.states.blog_state import BlogState
from src.llms.groqllm import GroqLLM
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
    
    def build_language_graph(self):
        """
        Build a graph for blog generation with inputs topic and language
        """
        self.blog_node_obj=BlogNode(self.llm)
        print(self.llm)
        ## Nodes
        self.builder.add_node("title_creation", self.blog_node_obj.title_creation)
        self.builder.add_node("content_generation",self.blog_node_obj.content_generation)
        self.builder.add_node("hindi_translation",lambda state: self.blog_node_obj.translation({**state, "current_language": "hindi"}))
        self.builder.add_node("french_translation",lambda state: self.blog_node_obj.translation({**state, "current_language": "french"}))
        self.builder.add_node("route",self.blog_node_obj.route)

        ## edges and conditional edges
        self.builder.add_edge(START, "title_creation")
        self.builder.add_edge("title_creation", "content_generation")
        self.builder.add_edge("content_generation", "route")

        ## conditional edge
        self.builder.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "hindi":"hindi_translation",
                "french":"french_translation"
            }
        )
        self.builder.add_edge("hindi_translation",END)
        self.builder.add_edge("french_translation",END)
        return self.builder

    def setup_graph(self,usecase):
        if usecase=="topic":
            self.build_topic_graph()
        if usecase=="language":
            print("Language block")
            self.build_language_graph()

        return self.builder.compile()
        
llm = GroqLLM().get_llm()
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_language_graph().compile()