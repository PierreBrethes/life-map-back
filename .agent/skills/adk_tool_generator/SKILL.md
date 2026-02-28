---
name: adk-tool-generator
description: Adds a new actionable tool for the Gemini ADK Agent. Use this whenever you need to give the AI agent a new capability.
---

# ADK Tool Generator

Strict guidelines for creating new Agent Development Kit (ADK) tools in the `life-map-back` project.

## When to use this skill
- When the Gemini agent needs a new way to interact with the database or external services.
- When refactoring existing agent functions in `agents/tools/`.

## How to use it
1. **Delegation**: The ADK tool must NEVER implement business logic or complex database queries itself. It must instantiate the appropriate Service class from `app.services` and delegate the work to it.
2. **Session Management**: Use the context manager `async with get_async_session() as session:` to instantiate the db session inside the tool (unless a global session manager for the agent's turn is later implemented).
3. **Pydantic Validation**: Try to type-hint the tool parameters using native Python types or Pydantic models where supported by the ADK, so validation happens automatically before the function executes. Convert string UUIDs to standard Python `UUID` objects securely.
4. **Error Handling**: Always wrap the tool logic in a `try...except Exception as e:` block and return a safe dictionary indicating the error (e.g., `{"status": "error", "message": str(e)}`). Never let the tool crash the agent loop.
5. **Docstrings**: Provide clear, detailed docstrings. The language of the docstring (French or English) should match the language the ADK prompt uses to understand the tool's purpose. Explain each parameter clearly in the `Args:` section.
