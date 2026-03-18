import sys
import os
import time

# Bind root path for local package execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from pipeline import ContextPipeline
from mode import MinimalMode
from compression import StandardCompressor
from provider import MockProvider
from budget import TokenBudget
from metrics import MetricsCollector
from sources import FileSource

def main():
    console = Console()
    console.print(Panel.fit("[bold cyan]🌊 ContextFlow Dev Dashboard/Help Console[/bold cyan]", border_style="cyan"))
    
    console.print("[yellow]Simulating long-running Agent loop... Loading verbose logs and memory...[/yellow]")
    
    # 1. Dummy simulation
    metrics = MetricsCollector()
    pipeline = ContextPipeline(
        sources=[],
        mode=MinimalMode(),
        compressor=StandardCompressor(),
        provider=MockProvider(),
        budget=TokenBudget(max_tokens=50),
        metrics=metrics
    )
    
    noisy_goal = "Analyze the database schema     \n\n\n   please kindly output valid JSON  \n\n `{ 'table': 'users' }` "
    
    with console.status("[bold green]Compressing and Executing Pipeline...", spinner="dots"):
        response = pipeline.run(noisy_goal)
        time.sleep(1) # Fake network delay for visualization
        
    # 2. Output Visualization (Admin Table Replacement)
    table = Table(title="Pipeline Telemetry & Savings", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="green")

    table.add_row("Tokens Before (Raw Input)", str(metrics.data.get("tokens_before", 0)))
    table.add_row("Tokens After (Compressed)", str(metrics.data.get("tokens_after", 0)))
    
    ratio = metrics.data.get("compression_ratio", 0)
    savings_str = f"{(1 - ratio) * 100:.1f}% Reduction" if ratio > 0 else "0%"
    table.add_row("Data Dropped (Cost Saved)", f"[bold red]{savings_str}[/bold red]")
    
    latency = metrics.data.get("latency_ms", 0)
    table.add_row("Time to Compress", f"{latency:.2f} ms")
    
    console.print(table)
    
    console.print("\n[bold]LLM Response:[/bold]")
    console.print(Panel(response, border_style="blue"))
    console.print("\n[italic gray]Note: In production deployments, developers pipe this exact metrics telemetry to their Datadog/LangSmith instances rather than relying on a web UI UI, maintaining ContextFlow as a zero-dependency headless library.[/italic gray]")

if __name__ == "__main__":
    main()
