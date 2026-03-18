# Plugins Contract

The PluginRegistry safely exposes native extensibility for contexts.

## Read-Only Integrity
The registry API guarantees immutability to external actors. 
- You may use `.list()`, `.names()`, or `.has(name)` to inspect loaded registries.
- **You may NOT mutate loaded registries dynamically.**
- Registration must strictly happen at **import time** (`<module>` scope) to guarantee safe asynchronous load order before the engine boots.
