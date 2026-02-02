from pathlib import Path
from dataclasses import dataclass, field

from core.src.model.models import FileNode
@dataclass
class ProjectEngine: 
    base_path: Path
    MAX_RETRIES: int = field(init=False,default=3,repr=False)
    current_logs: list[str] = field(default_factory=list)
    
    # implementamos el metodo run 
    
    
    
    

@dataclass
class ProjectRequest:
    project_name: str
    structure: list[FileNode]    
    