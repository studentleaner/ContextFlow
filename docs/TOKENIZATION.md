# Tokenization & Budget Constraints

ContextFlow treats a Large Language Model's Context Window as limited, highly expensive RAM. 

## The `TokenEstimator`
Instead of predicting array lengths through raw string length `/ 4` character approximations, ContextFlow natively bounds `tiktoken.encoding_for_model(model)` into a core `TokenEstimator`.

When data passes into the `TokenBudget` orchestration block, every `ContextItem` is explicitly assigned a byte-pair length.

## Smart Budget Slicing Algorithms
When the array overflows `max_tokens` (e.g., 6000), standard agents ruthlessly truncate the bottom half of the array—frequently destroying recent prompt history.

ContextFlow takes a safer approach:
1. **Priority Culling:** The algorithm hunts backward for strings marked `priority=0` (usually redundant tool logs or agent thought-loops) and purges them completely.
2. **System Preservation:** Items marked `role = "system"` are entirely immune to all truncation.
3. **Semantic Slicing:** If the array STILL overflows the budget despite noise purging, ContextFlow mathematically counts backward and gracefully appends `[TRUNCATED BUDGET]` to the earliest non-system string, leaving exactly 100% of the allowed context limit intact without breaking JSON schemas at the slice margin.
