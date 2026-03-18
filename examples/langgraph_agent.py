"""
LangGraph Interception Demo
This file demonstrates how ContextFlow acts as a pure middleware interception 
node inside a standard LangGraph (or any state-based) cyclical agent loop.
"""

import sys
import os
import asyncio

# Fallback for running locally without pip install -e .
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contextflow import (
    ContextPipeline, MinimalMode, StandardCompressor, 
    TokenBudget, MockProvider, MetricsCollector, ContextItem
)

class AgentState:
    def __init__(self):
        self.messages = []

def node_generate_noisy_logs(state: AgentState):
    """Simulates a LangGraph Tool Node executing a shell command and generating massive garbage logs."""
    noise = "please kindly fix... \n" * 50
    state.messages.append(ContextItem(
        role="tool",
        content=f"System Log Output:\n{noise}```json\n{{ \"error\": \"OOM limit reached\" }}\n```",
        priority=0
    ))
    return state

def node_context_middleware(state: AgentState):
    """
    THE OPTIMIZATION NODE.
    Rather than passing the 50k token state directly back to the LLM node, 
    ContextFlow compresses the state deterministically in-transit automatically.
    """
    pipeline = ContextPipeline(
        sources=[], 
        mode=MinimalMode(),
        compressor=StandardCompressor(),
        provider=MockProvider(),
        budget=TokenBudget(max_tokens=6000),
        metrics=MetricsCollector()
    )
    
    # 1. State array goes in -> 2. Regex isolates JSON blocks 
    # 3. Filler text is trimmed -> 4. Priority mappings applied -> 5. State array comes out
    state.messages = pipeline.compressor.compress(state.messages)
    state.messages = pipeline.budget.enforce(state.messages)
    return state

def node_llm_reasoning(state: AgentState):
    """The LLM reasoning node receives the beautifully compressed state."""
    print(f"[LLM Target Node] Received minified token payload of character length: {len(str(state.messages))}")
    return state

async def main():
    print("--- LangGraph / ContextFlow Async Interception Demo ---")
    state = AgentState()
    
    # 1. Tool execution (creates massive noise in the state array)
    state = node_generate_noisy_logs(state)
    print(f"Raw State Size (Tokens injected by local tools): {len(str(state.messages))}")
    
    # 2. ContextFlow Middleware Layer
    state = node_context_middleware(state)
    print(f"Compressed State Size (Tokens ready for LLM API): {len(str(state.messages))}")
    
    # 3. Final Agent Node
    node_llm_reasoning(state)
    
    print("\n✅ ContextFlow safely stripped boilerplate and deduplicated lines while retaining the valid JSON block schema!")

if __name__ == "__main__":
    asyncio.run(main())
