import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

from src.core.project_Engine import ProjectEngine
from src.core.ai_handler import ask_gemini_for_structure

console = Console()
app = typer.Typer(help="AI Project Architect CLI")


@app.command()
def build(promp: str = typer.Argument(...,help="Description of project"),force: bool = typer.Option(False,"--force","-f",help="Force new generation")): 
    console.print(Panel.fit("[bold cyan] AI Project Generator[/bold cyan]", border_style="blue"))
    
    with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),transient=True) as progress: 
        progress.add_task(description="Motor configurate...", total=None)
        engine = ProjectEngine()
        
        # save schema AI 
        progress.add_task(description="Gemini request...", total=None)
        try: 
            req = ask_gemini_for_structure(promp)
            
            schemas_path = Path.cwd() / "schemas"
            schemas_path.mkdir(exist_ok=True)
            schema_file = schemas_path / f"schema_{req.project_name}.json"
            
            # save json 
            schema_file.write_text(req.model_dump_json(indent=4))
            console.log(f"[*] AI Schema saved: schemas/{schema_file.name}")
            
        except Exception as e: 
            console.print(f"[bold red][!] Error:[/bold red] {e}")
            raise typer.Exit(code=1)
        
        # build 
        progress.add_task(description="Building project files...", total=None)
        try:
            engine.execute_build(req)
            engine.save_to_cache(req)
            engine.generate_output(req)
            console.log(f"[*] Build completed for {req.project_name}")
        except Exception as e:
            console.print(f"[bold red][!] Build error:[/bold red] {e}")
            raise typer.Exit(code=1)
        
    console.print(Panel(f"Project [green]{req.project_name}[/green] generated successfully", title="Success"))