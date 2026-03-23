# mypy: ignore-errors

from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Dict, Any

T = TypeVar("T")

class ProjectRequest(BaseModel,Generic[T]): 
    project_name: str 
    structure: list[T] 
    logs: list[str] = Field(default_factory=list)
    raw_response: Dict[str, Any] = Field(default_factory=dict)
    
    
    class Config:
        """ this allow that T could be whatever thing"""
        arbitrary_types_allowed = True