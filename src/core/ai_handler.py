# mypy: ignore-errors

import google.generativeai as genai
from os import getenv
from src.core.project_request import ProjectRequest
from src.core.fileNode import FileNode

api_key = getenv("GEMINI_API_KEY")
if not api_key: 
    raise ValueError("No GEMINI_API_KEY was found in the environment.")
    
genai.configure(api_key=api_key)

def ask_gemini_for_structure(user_prompt: str) -> ProjectRequest: 
    model = genai.GenerativeModel('models/gemini-flash-latest')
    

    schema_manual = {
        "type": "object",
        "properties": {
            "project_name": {"type": "string"},
            "structure": {  # <--- CAMBIO: Ahora se llama 'structure'
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "content": {"type": "string"},
                        "is_dir": {"type": "boolean"}
                    },
                    "required": ["name", "is_dir"]
                }
            }
        },
        "required": ["project_name", "structure"] # <--- CAMBIO: Requerimos 'structure'
    }
    
    # request and response 
    response = model.generate_content(
        f"Generates a technical file structure for {user_prompt}",
        generation_config=genai.GenerationConfig(
            # Indicamos que la respuesta será un JSON
            response_mime_type="application/json",
            # CAMBIO AQUÍ: Convertimos el modelo de Pydantic a un esquema JSON estándar
            response_schema=schema_manual
        )
    )
    
    return ProjectRequest[FileNode].model_validate_json(response.text)