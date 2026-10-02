# Resources — patterns worth stealing

> Sources are references, not runtimes. Port patterns, not whole stacks.
> Local sleep controller: `/root/sleepintel` (already cloned — prx0r/sleepintel).

## Local first

| Repo | What | How bgraph uses it |
|------|------|--------------------|
| `/root/sleepintel` | Brand/channel controller: registry YAML, templates, pipeline, Jev gates | **Primary pattern** — organiser not creator; channels.yaml shape; method contracts |
| `/root/oddhobbies` | Commerce core: stores, packs, R2 commerce assets, graph export | Product truth + store_id alignment |
| `/root/agentcom` | CompanyGraph entities/edges | Brand identity edges, credential_ref names |
| `/root/qprivately` + cmail `qp/` | Grants, gates, receipts | Later: publish/spend gates |
| `/root/influence` | Passports, Postiz connectors, human tasks | Later: publish executors |
| `/root/stevejobless` | Desired-vs-observed human queue | Later: claim/OAuth tasks |

## Social publishing (workspaces, MCP)

| Repo | Steal |
|------|--------|
| [gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) | Multi-account scheduling; already referenced in influence |
| [trypost-it/trypost](https://github.com/trypost-it/trypost) | Workspaces per brand + MCP + calendar |
| [rodrgds/openpost](https://github.com/rodrgds/openpost) | Brand workspaces, API/CLI/MCP |
| [deifos/brightbean-studio](https://github.com/deifos/brightbean-studio) | Unlimited workspaces, YT+Pinterest MCP |
| [pendpost/pendpost](https://github.com/pendpost/pendpost) | Human approval gate + MCP (matches QP law) |
| [Goloom-App/goloom](https://github.com/Goloom-App/goloom) | Light Go MCP scheduler |

## YouTube ops + analytics

| Repo | Steal |
|------|--------|
| [gmrdad82/pito](https://github.com/gmrdad82/pito) | Multi-channel YT self-host + MCP |
| [felipefontoura/youtube-studio-mcp](https://github.com/felipefontoura/youtube-studio-mcp) | Full Analytics MCP |
| [conorbronsdon/yt-analytics-mcp](https://github.com/conorbronsdon/yt-analytics-mcp) | Owner-side analytics MCP |
| [Bin-Huang/youtube-analytics-cli](https://github.com/Bin-Huang/youtube-analytics-cli) | CLI JSON for agents → analytics/ sink |
| [treycooper3/youtube-analytics-skill](https://github.com/treycooper3/youtube-analytics-skill) | Retention + drop-offs |

## R2 media patterns

| Repo | Steal |
|------|--------|
| [Planetterrian/nerranetwork](https://github.com/Planetterrian/nerranetwork) | R2 prefixes, JSON sidecars, thumb vs original ACL, manifest |
| [BuildWithHussain/vms](https://github.com/BuildWithHussain/vms) | Source/Cut/Review/Final categories; metadata-only DB |
| [syntaxsdev/mediaflow](https://github.com/syntaxsdev/mediaflow) | Go R2/S3 upload validation; CF Stream for video |
| [likaiprime/cloudflare-media-processor](https://github.com/likaiprime/cloudflare-media-processor) | Multi-tenant R2 + video thumbnail/metadata |
| [vincent/damask](https://github.com/vincent/damask) | Single-binary DAM, optional later UI |

## Shorts / repurposing (later)

| Repo | Steal |
|------|--------|
| [random-or/shorts-clipper](https://github.com/random-or/shorts-clipper) | Longform → Shorts pipeline |
| [jastfan/AutoShortAi](https://github.com/jastfan/AutoShortAi) | Local cut/edit for brand-owned footage |
| [Yacineooak/clippy-ai-agent](https://github.com/Yacineooak/clippy-ai-agent) | Long → multi-platform shorts agent |
| [shahidbaleli/Auto_You](https://github.com/shahidbaleli/Auto_You) | Free OAuth upload factory + quota guard |

## Optimisation (after volume)

| Repo | Steal |
|------|--------|
| [neterfk-coder/retention-autopsy-proyect](https://github.com/neterfk-coder/retention-autopsy-proyect) | Retention ↔ edit decisions |
| [JensBender/youtube-channel-analytics](https://github.com/JensBender/youtube-channel-analytics) | ETL + competitor compare |

## Skip for now

| Repo | Why |
|------|-----|
| Xaptured/creator-flow | Spring/Kafka/ECS — enterprise overkill |
| digitalleonard/content-studio-setup | Supabase stack, not our R2+commerce spine |
