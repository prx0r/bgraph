# DAILY-LOOP — autonomous ops

## Commands

```bash
cd /root/bgraph

# 1. Validate schemas + brands + gates
python3 scripts/validate.py

# 2. Export graphs for agents
python3 scripts/export_graph.py
python3 scripts/export_graph.py --store oddhobb

# 3. Human status board
python3 scripts/brand_status.py

# 4. Tests
python3 -m pytest tests/ -q
```

## What “good” looks like

| Signal | Expect |
|--------|--------|
| validate | `OK: N brands validated` |
| export | `exports/<id>.json` with nodes+edges |
| brand_status | 3 brands; active vs scaffold clear |
| pytest | all passed |

## After editing a brand

1. Edit `registry/brands/<id>.json`  
2. `validate.py`  
3. `export_graph.py --store <id>`  
4. Sync oddhobbies pack if products changed  
5. Sync pogpet BRANDS if domain changed  

## After adding a brand

Follow [BRAND-ADD.md](BRAND-ADD.md) end-to-end.

## When validate fails

| Error | Fix |
|-------|-----|
| missing identity.display_name | fill identity |
| store_id != filename | rename file or store_id |
| active but no enabled branches | enable a branch or set status scaffold |
| social publish not human_confirm | set gate to human_confirm |
| r2 root not under content/stores/ | fix branch.r2_layout.root |

## Git

```bash
git status
git add -A
git commit -m "bgraph: …"
# owner pushes
```
