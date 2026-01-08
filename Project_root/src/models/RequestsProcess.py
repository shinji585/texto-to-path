from pathlib import Path
from art import text2art
from src.models.request import Request

class RequestsProcess:
     
     _user: Request
     _tokens: list
     
     # creamos el diccionario con palabras claves
     _KEY_WORDS: dict = {
          "actions": {
               "CREATE": ["create","make","generate","build","crear","hacer"],
               "SAVE": ["guardar","save","store","backup"]
          },
          "objects": {
               "FILE": ["file","archivo","documento","txt"],
               "FOLDER": ["folder","directoy","carpeta","dir"]
          },
          "categories":{
               "INVOICES": ["invoices","facturas","recibos"],
               "REPORTS": ["reports","reportes","informes"],
               "LOGS": ["logs","registros","bitacora"]
          }
     }
     
     # creamos la funcion que tomara la entrada del usuario 
     def user_enter(self) -> Request: 
          
          try:
               print(text2art("text to path"))
               user_request_text = str(input("Enter your request: "))
               
               # guardamos en self 
               self._user = Request(texto=user_request_text)
               # preparamos los datos para la clasificacion
               self._tokens =  user_request_text.lower().split()
               
               # retornarmos los metadatos de la peticion  
               return self._user
          except Exception as e: 
               raise e 
          
     # clasificamos la informacion 
     def classify(self) -> dict: 
          
          # buscamos coincidencias 
          result: dict = {
               "action": self._find_match(tokens=self._tokens,bunket_name="actions"),
               "object": self._find_match(tokens=self._tokens,bunket_name="objects"),
               "category": self._find_match(tokens=self._tokens,bunket_name="categories")
          }
          
          # retornamos el resultado 
          return result
     
     # luego de obtener la requests tenemos que formatear la solicitud que fue hecha 
     def _find_match(self,tokens: list,bunket_name: str) -> str:
            # buscamos las coincidencias entre el token y lo que viene siendo la constantes 
            for key, keywords in self._KEY_WORDS[bunket_name].items():
                 if any(k in tokens for k in keywords):
                      return key
            return "UNKNOWN"