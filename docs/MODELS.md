# Model Architecture

The model is a tool, not Gary. Identity, roles, security policy, memory, host records, and procedures survive model replacement.

Provider order is local llama.cpp first, optional free remote model when explicitly enabled, then user assistance if local capability is insufficient.

Local model lifecycle: discover GGUF files, register metadata, evaluate resources, load only when needed, unload when idle/stopping, and switch without changing Gary identity.

Session continuity passes user objective, host identity, findings, completed actions, unresolved questions, and pending approvals to the replacement model.
