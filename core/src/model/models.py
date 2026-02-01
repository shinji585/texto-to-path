from abc import ABC
from typing import TypeVar, Optional,Generic,Union
from enum import Enum
from dataclasses import dataclass

# tipo generico 
T  = TypeVar('T')

# clase abstracta 
class AbstracFileNone(ABC): 
    name: str 
    extension: str 
    path: str
    content: Optional[str]
    is_directory: bool
    children: Optional[list[dict[str, Union[str, bool, None, list]]]] = None
    
# clase generica y abstracta 
class AbstractProjectRequest(ABC,Generic[T]): 
    project_name: str 
    raw_response: dict
    logs: list[str]
    structure: T   
    
class AbstractProjectType(ABC): 
    category: Union[str,Enum]
    language: Union[str,Enum]
    architecture: Union[str,Enum]
    
    
# creamos las clases que seran utilizadas por engine 
@dataclass
class FileNode(AbstracFileNone): 
    name: str
    extension: str
    path: str
    content: Optional[str]
    is_directory: bool
    children: Optional[list[dict[str, Union[str, bool, list, None]]]] = None
    
@dataclass
class ProjectRequest(AbstractProjectRequest,Generic[T]): 
    project_name: str
    raw_response: dict
    logs: list[str]
    structure: T

@dataclass
class ProjectType(AbstractProjectType): 
    category: Union[str,Enum]
    language: Union[str,Enum]
    architecture: Union[str,Enum]