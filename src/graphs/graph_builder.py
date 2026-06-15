from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm=llm
        self.graph=StateGraph(BlogState)

    def build_topic_graph(self):
        """
        Build a graph to generate blogss based on topic
        """
        self.graph = StateGraph(BlogState)
        self.blog_node_obj=BlogNode(self.llm)
        print(self.llm)
        ## Nodes
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_obj.content_generation)

        ## Edges
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation",END)

        return self.graph
    
    def build_language_graph(self):
        self.graph = StateGraph(BlogState)
        self.blog_node_obj = BlogNode(self.llm)
        print(self.llm)
        
        ## Nodes
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generator", self.blog_node_obj.content_generator)
        self.graph.add_node("Hindi_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "hindi"}))
        self.graph.add_node("Spanish_translation", lambda state: self.blog_node_obj.translation({**state, "current_language": "spanish"}))
        self.graph.add_node("route", self.blog_node_obj.route)  # ← only once, uses route (returns dict)

        ## Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generator")
        self.graph.add_edge("content_generator", "route")

        ## Conditional edges
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,  # ← separate router function
            {
                "hindi": "Hindi_translation",
                "spanish": "Spanish_translation"
            }
        )
        self.graph.add_edge("Hindi_translation", END)
        self.graph.add_edge("Spanish_translation", END)
        return self.graph

    def setup_graph(self,usecase):
        if usecase=="topic":
            self.build_topic_graph()
        elif usecase=="language":
            self.build_language_graph()
        return self.graph.compile()
    

## Below code is for the langsmith langgraph studio
llm=GroqLLM().get_llm()

## get the graph
graph_builder=GraphBuilder(llm)
graph_watch=graph_builder.build_language_graph().compile()

