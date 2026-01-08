from dataclasses import dataclass
import os 
import sys


# creamos la clase requests
@dataclass(init=False) 
class Request: 
    _texto: str 
    _USER: str 
    _USER_SYSTEM: str 
    contador: int = 0 
    
    # definimos el __init__
    def __init__(self,texto: str) -> None:
        # pasamos el texto 
        self._texto = texto
        Request.contador += 1 
        Request._get_user()
        Request._get_user_system()
        
    # definimos el nombre del usuario
    @classmethod
    def _get_user(cls) -> None: 
        if os.name == "nt":
            cls._USER = os.environ.get("USERNAME")
        else: 
            cls._USER = os.environ.get("USER") or os.environ.get("LOGNAME")
            
    # definimos el tipo desistema operativo 
    @classmethod
    def _get_user_system(cls) -> None:
        cls._USER_SYSTEM = sys.platform
    
    # retornamos un dict 
    def return_data(self) -> dict: 
        return {
            "System name": self._USER_SYSTEM,
            "User": self._USER,
            "Requests": self._texto 
        }
        
    # retornamos el contador 
    @classmethod
    def numbers_requests(cls) -> None:
        return cls.contador