# mypy: ignore-errors

from pydantic import BaseModel, Field, PrivateAttr, model_validator
from pathlib import Path
from typing import Optional, List, Any
import redis
from os import getenv
from src.core.fileNode import FileNode
from src.core.project_request import ProjectRequest

class ProjectEngine(BaseModel): 
    
    base_path: Path = Field(default_factory=lambda: Path.cwd() / "output")
    max_retries: int = Field(default=3, alias="MAX_RETRIES")
    current_logs: List[int] = Field(default_factory=list)
    _redis: redis.Redis = PrivateAttr()
    
    @model_validator(mode="after")
    def initialize_engine(self) -> 'ProjectEngine': 
        self._redis = redis.Redis(
            host=getenv("REDIS_HOST", "redis"),
            port=6379,
            decode_responses=True
        )
        
        self.base_path.mkdir(parents=True,exist_ok=True)
        
        # check if the cache file exits 
        (self.base_path.parent / "cache").mkdir(exist_ok=True)
        
        # check if generator exits 
        (self.base_path.parent / "generator").mkdir(exist_ok=True)
        
        return self
    
    
    def create_node(self,name: str,path: str,is_directory: bool,content:Optional[str] = None) -> FileNode: 
        """ create a instance of file node with predefine logic"""
        extension = ".py" if not is_directory else ""
        
        return FileNode(
            name=name,
            extension=extension,
            path=path,
            content=content,
            is_dir=is_directory,
            children=[]
        )
        
    def execute_build(self, req: ProjectRequest[FileNode]) -> None: 
        self.base_path.mkdir(parents=True, exist_ok=True)
        full_path_project = self.base_path / req.project_name
        full_path_project.mkdir(parents=True, exist_ok=True)
        
        for node in req.structure:
            self._build_recursive(full_path_project, node)
        
    def _build_recursive(self, current_base: Path, node: FileNode) -> None: 
        this_node_path = current_base / node.name.lstrip("/")
        
        if node.is_dir:
            this_node_path.mkdir(parents=True, exist_ok=True)
            if hasattr(node, 'children') and node.children:
                for child in node.children:
                    self._build_recursive(this_node_path, child)
        else:
            this_node_path.parent.mkdir(parents=True, exist_ok=True)
            this_node_path.write_text(node.content or "")
            
    def save_to_cache(self,req:ProjectRequest): 
        key = f"project:{req.project_name}"
        self._redis.set(key,req.model_dump_json(),ex=3600)
        
        # save the cache on the cache path 
        cache_path = self.base_path.parent / "cache" / f"{req.project_name}.json"
        cache_path.write_text(req.model_dump_json(indent=4))
        
        
    def get_from_cache(self,project:str) -> Optional[ProjectRequest]: 
        cache_str = self._redis.get(f"project:{project}")
        
        if cache_str: 
            return ProjectRequest[FileNode].model_validate_json(cache_str)
        
        
        return None
    
    def generate_output(self,req: ProjectRequest[FileNode]) -> dict: 
        generator_path = self.base_path.parent / "generator"
        generator_path.mkdir(exist_ok=True)
        
        
        # create the data that is going to stay on generator 
        report = {
            "project": req.project_name,
            "engine_logs": self.current_logs,
            "structure_applied": True,
            "location": str(self.base_path / req.project_name)
        }
        
        # save the file in /generator
        report_file = generator_path / f"report_{req.project_name}.json"
        report_file.write_text(req.model_dump_json(indent=4))
        
        return report