---
name: hetzner-advisor
description: Use when users ask about Hetzner servers, need help choosing a server, want to compare dedicated vs cloud, need infrastructure recommendations for their projects, or mention Hetzner in the context of hosting decisions.
---

# Hetzner Server Advisor

Recommend the optimal Hetzner server based on user requirements.

## Workflow

1. **Gather requirements** using the questions below
2. **Select category** based on requirements
3. **Read reference file** for chosen category
4. **Recommend specific server(s)** with justification

## Questions to Ask

Ask these questions to understand requirements (skip if already provided):

1. **Budget**: Monthly budget in EUR?
2. **Workload**: What will the server run? (web app, database, AI/ML, storage, etc.)
3. **Resources**: Specific CPU/RAM/storage needs?
4. **GPU**: Need GPU for AI/ML workloads?
5. **Management**: Self-managed (root) or fully managed?
6. **Scale**: Single server or need to scale horizontally?
7. **Traffic**: Expected monthly traffic volume?

## Category Selection

| Category | Price Range | Best For |
|----------|-------------|----------|
| Web Hosting | €1.60-20/mo | Static sites, WordPress, small CMS |
| Managed | €34-221/mo | Need Apache/MariaDB without admin work |
| Cloud | €3.49-294/mo | Scalable, API-driven, multiple instances |
| Dedicated | €37-988/mo | Full control, predictable performance |

### Decision Logic

```
IF need_gpu:
    → Dedicated GPU (GEX series)
ELIF workload == "simple_website" AND no_admin_skills:
    → Web Hosting
ELIF need_managed_stack AND no_admin_skills:
    → Managed Server
ELIF need_horizontal_scaling OR api_driven OR pay_per_use:
    → Cloud
ELSE:
    → Dedicated
```

## Quick Reference

| Use Case | Recommendation |
|----------|----------------|
| Personal blog | Web Hosting S (€1.60/mo) |
| WordPress business site | Web Hosting M/L or Managed MC30 |
| Small web app | Cloud CX23 (€3.49/mo) |
| Production web app | Cloud CCX23 or Dedicated AX42 |
| High-traffic application | Dedicated AX102/EX63 |
| Database server (high RAM) | EX130-R or AX162-R |
| Storage/backup server | SX65/SX135/SX295 |
| AI inference | GEX44 (RTX 4000, €184/mo) |
| AI training | GEX131 (RTX PRO 6000, €889/mo) |
| Enterprise/compliance | Dell DX series |
| Kubernetes cluster | Cloud CCX or Dedicated AX |
| ARM64 workloads | Cloud CAX series |

## Reference Files

Read the appropriate reference file for detailed specifications:

- **[references/dedicated.md](references/dedicated.md)**: EX, AX, SX, GPU, Dell dedicated servers
- **[references/cloud.md](references/cloud.md)**: CX, CAX, CPX, CCX cloud servers
- **[references/managed.md](references/managed.md)**: Managed servers and web hosting

## Recommendation Format

When recommending, include:

1. **Primary recommendation** with model name and price
2. **Key specs** (CPU, RAM, Storage, Network)
3. **Why this choice** (match to requirements)
4. **Alternative** if budget or needs change
5. **Link** to Hetzner product page
