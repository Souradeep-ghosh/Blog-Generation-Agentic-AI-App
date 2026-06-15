from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    It is a class to represent the blog node
    """
    def __init__(self,llm):
        self.llm = llm
        
    def title_creation(self,state:BlogState):
        """
        This will be used to create the title for the blog.
        """
        if "topic" in state and state["topic"]:
            
            prompt= """ 
                You are an expert blog content writer. Use Markdown formatting.
                Generate a blog title for the {topic}. This title should be creative and SEO friendly 
                as well.
            
            """
            
            system_message= prompt.format(topic=state["topic"])
            response= self.llm.invoke(system_message)
            
            return {"blog": {"title": response.content}}
        
        
    def content_generator(self, state:BlogState):
        """
        This will be used to create the blog.
        """
        if "topic" in state and state["topic"]:
            system_prompt= """
            You are an expert blog writer. Use Markdown formatting and 
            generate a detailed blog content with detailed breakdown for the {topic}
            """
            
            system_message= system_prompt.format(topic=state["topic"])
            response= self.llm.invoke(system_message)
            
            return {"blog": {"title": state["blog"]["title"], "content": response.content}}
                   
            
    def translation(self,state:BlogState):
        """
        This function will translate the content to the specified language.
        """
        translation_prompt="""
        Translate the following content into {current_language}.
        -Maintain the original tone, style and formatting.
        -Adapt cultural references and idioms to be appropriate for {current_language}.
        
        ORIGINAL CONTENT: {blog_content}
        
        """
        blog_content=state["blog"]["content"]
        messages= [
            HumanMessage(translation_prompt.format(current_language=state["current_language"], blog_content=blog_content))
            
            
        ]
        translation_content = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog": translation_content}
    
    def route(self, state:BlogState):
        return {"current_language": state["current_language"]}
    
    def route_decision(self, state: BlogState):
        """
        It routes the content to the respective translation function.
        """
        if state["current_language"]=="hindi":
            return "hindi"
        elif state["current_language"]=="spanish":
            return "spanish"
        else:
            return state["current_language"]
        
            
        