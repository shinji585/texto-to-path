# mypy: ignore-errors

from pydantic import BaseModel, Field, model_validator
from typing import Optional

class FileNode(BaseModel): 
    name: str 
    extension: Optional[str] = None
    path: str = "src/api.py"
    content: Optional[str] = None
    is_dir: bool
    children: Optional[list["FileNode"]] = Field(default_factory=list)
    
    class Config: 
        """this allow the class get an object from a data base, pydantic transform it to the model automatically"""
        from__attributes = True
        
    @model_validator(mode="after")
    def check_directory_content(self): 
        if self.is_dir and self.content is not None: 
            raise ValueError("A directory cannot have content")
        return self