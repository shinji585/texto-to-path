from pathlib import Path 
from src.models.RequestsProcess import RequestsProcess
import json 

class Main:
    
    # para obtener la ruta donde tenemos que guardar los datos  
    PATH: Path = Path.cwd().parent / "logs"
    PROCESO: RequestsProcess = RequestsProcess()
    
    # ahora que ya tenemos al requestsProcess cargado tenemos que realizar los procesos donde obtenemos la ruta principal
    def main(self) -> None:
        # llamamos la funcion save_metadata
        self.save_meta_data()
        
        # creamos la requests 
        self.create_request()
    
    # salvamos en memoria la meta data (esto le permitira a el sistema aprender mas adelante)
    def save_meta_data(self) -> None: 
        # llamamos user_enter de requestsprocess
        meta_data = self.PROCESO.user_enter()
        
        # definimos la ruta donde se guardaran los metada datos 
        data_rout: Path = self.PATH / "meta_data.json"
        
        # creamos la carpeta si esta no existe 
        data_rout.parent.mkdir(parents=True, exist_ok=True)
        
        # creamos o guardamos en el json 
        if data_rout.exists(): 
            with data_rout.open(mode="a", encoding="utf-8") as f: 
                json_string = json.dumps(meta_data.return_data(), ensure_ascii=False)
                f.write(json_string + "\n")
        else: 
            with data_rout.open(mode="w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)
                
    # tenemos que tomar el result que nos envia el classify 
    def create_request(self) -> None: 
        # llamamos classify desde requestsprocess
        raw_results = self.PROCESO.classify() 
        
        # limpiamos el diccionario 
        raw_results = {k: v for k,v in raw_results.items() if v != "UNKNOWN"}
        
        # verificamos que no este vacio 
        if not raw_results: 
            raise("Your request was not understood by the system.")
        
        # verificamos que la accion a realizar no falte 
        if "action" not in raw_results:
            raise("The action to perform was not found.")
        
        # extraemos las categorias 
        category = raw_results.get("category","MISC")
        
        # si no encontramos objecto asumimos que es un folder (por seguridad)
        obj_type = raw_results.get("object","FOLDER")
        
        # construimos la ruta 
        output_path: Path = self.PATH / category
        
        # ejecutamos la intencion 
        
        try:
            output_path.mkdir(parents=True,exist_ok=True)
            
            if obj_type == "FOLDER":
                print(f"Structure created on: {output_path}")
                
            elif obj_type == "FILE":
                # creamos el archivo 
                file_path = output_path / "new_request.txt"
                file_path.touch()  # creamos el archivo 
                print(f"File created on: {output_path}")
        except Exception as e: 
            print(f"Error when creating the resource: {e}")
        
        