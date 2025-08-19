from src.states.blog_state import BlogState
class BlogNode:
    def __init__(self,llm):
        self.llm = llm
    
    def title_creation(self, state:BlogState):
        """
        create a title for the blog
        """
        if "topic" in state and state["topic"]:
            prompt = """
                        You are an exprt blog content writer. Use markdown formatting. Generate a blog title for the topic {topic}. This title should be creatuve and SEo friendly.
                    """
            system_message = prompt.format(topic = state["topic"]) #act as a placceholder ey value that will replace to whats written in the prompt
            response = self.llm.invoke(system_message)
            return {
                "blog":{"title":response.content}
            }

    def content_generation(self, state:BlogState):
        """
        create a detailed blog on the given topic
        """
        if "topic" in state and state["topic"]:
            prompt = """You are an expert blog content writer. Use markdown formatting.create a detailed blog content with detailed breakdown of the {topic}"""
            system_message = prompt.format(topic = state["topic"])
            response = self.llm.invoke(system_message)
            return {
                "blog":{
                    "title":state["blog"]["title"],
                    "content":response.content
                }
            }