# Team Marketplace

A Claude Code plugin marketplace for team distribution.

## Available Plugins

| Plugin | Type | Description |
|--------|------|-------------|
| `code-reviewer` | Agent | Reviews code for quality, security, and maintainability |
| `version-finder` | Agent | Finds latest package versions across GitHub, npm, Packagist, PyPI |
| `explaining-code` | Skill | Explains code with visual diagrams and analogies |
| `hetzner-advisor` | Skill | Recommends optimal Hetzner servers based on requirements |
| `desktop-notify` | Hook | Desktop notifications for Claude Code events (Linux) |

## Installation

### Add the Marketplace

```bash
# From GitHub (after pushing)
/plugin marketplace add your-username/team-marketplace

# Or from local path for testing
/plugin marketplace add /path/to/team-marketplace
```

### Install Individual Plugins

```bash
/plugin install code-reviewer@team-marketplace
/plugin install version-finder@team-marketplace
/plugin install explaining-code@team-marketplace
/plugin install hetzner-advisor@team-marketplace
/plugin install desktop-notify@team-marketplace
```

## Plugin Details

### code-reviewer

An agent that performs comprehensive code reviews focusing on:
- Code quality and readability
- Security vulnerabilities
- Performance considerations
- Best practices (PHP/Magento focused)

**Usage**: Automatically triggered when code is modified, or invoke manually.

### version-finder

An agent that systematically checks package registries to find the latest versions:
- GitHub Releases
- Packagist (PHP)
- npm (JavaScript)
- PyPI (Python)

**Usage**: Ask "What's the latest version of [package]?"

### explaining-code

A skill that explains code using:
- Real-world analogies
- ASCII diagrams
- Step-by-step walkthroughs
- Common gotchas

**Usage**: Ask "How does this code work?" or "Explain this function"

### hetzner-advisor

A skill that recommends Hetzner servers based on requirements:
- Budget constraints
- Workload type (web, database, AI/ML, storage)
- Resource needs (CPU, RAM, storage)
- Management preferences

**Usage**: Ask "What Hetzner server should I use for [workload]?"

### desktop-notify

A hook that sends desktop notifications on Linux systems using `notify-send`.

**Requirements**: `notify-send` (usually pre-installed on most Linux desktops)

**Events**: Triggers on Claude Code notification events.

## Development

### Directory Structure

```
team-marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── README.md
└── plugins/
    ├── code-reviewer/
    ├── version-finder/
    ├── explaining-code/
    ├── hetzner-advisor/
    └── desktop-notify/
```

### Adding a New Plugin

1. Create a new directory under `plugins/`
2. Add `.claude-plugin/plugin.json` with metadata
3. Add your agents, skills, or hooks
4. Update `marketplace.json` to include the new plugin

## License

MIT
