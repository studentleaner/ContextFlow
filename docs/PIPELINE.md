# Pipeline Contract

ContextPipeline is the main orchestrated loop of data. 

## Strict Execution Ordering Map
The pipeline explicitly enforces a static node structure. This order locks to:
1. `mode`: Stripping / Formatting (Semantic subsetting, formatting constraints)
2. `rank`: Prioritizing and scoring
3. `compress`: Deduplicating, summarization or distillation natively
4. `cache`: Short-circuiting execution natively over duplicated chunks
5. `budget`: Cropping to strict token limits before OOMs occur
6. `provider`: Bounding asynchronous calls explicitly

Any custom plugins loaded downstream MUST comply with these 6 static steps to execute effectively natively.
Pipelines rigorously lock these invariants dynamically during asynchronous execution to prevent out-of-order crashes or cache corruptions.
