---
name: claude-code-docs
description: Use when users ask about Claude Code features, configuration, hooks, MCP servers, skills, commands, settings, memory, or troubleshooting. Also use when you need to look up how something works in Claude Code.
---

# Claude Code Documentation Search

This skill provides semantic search over Claude Code documentation via RAG (Retrieval-Augmented Generation).

## Available MCP Tools

You have access to these MCP tools (provided by `claude-code-docs-rag` server):

1. **docs_search** - Semantic search across all documentation
   - `query`: What to search for
   - `limit`: Max results (default 5)

2. **docs_list_topics** - List all available documentation topics

3. **docs_reindex** - Re-index docs after updates

## When to Use

Use `docs_search` when:
- User asks about Claude Code features
- You need to verify how something works
- Looking up configuration options
- Finding hook/MCP/skill documentation
- Troubleshooting Claude Code issues

## Usage Pattern

1. Search for relevant documentation
2. Read and synthesize the results
3. Answer the user's question with accurate information
4. Cite the source (e.g., "According to the hooks documentation...")

## Example Queries

- "How do hooks work?" → search for "hooks PreToolUse PostToolUse"
- "MCP server configuration" → search for "MCP server add configure"
- "Memory and CLAUDE.md" → search for "CLAUDE.md memory files"
