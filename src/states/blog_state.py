from typing import TypedDict
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title:str =Field(description="Title of the blog post")
    content: str = Field(description="COntent of the blog post")

class BlogState(TypedDict):
    topic:str
    blog:Blog
    current_lang:str