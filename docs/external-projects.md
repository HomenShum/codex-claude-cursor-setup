# External projects

This is the human-readable view of the machine ledger in [`sources/external-projects.json`](../sources/external-projects.json). It records public GitHub projects directly used, configured, installed, cited as workflow authorities, represented by direct package or image declarations, or explicitly considered in historical research. It deliberately excludes transitive packages and private source repositories.

The relationship column matters. A runtime dependency, an installed local plugin, a design authority, and a rejected research lead are not interchangeable claims. An access date records when the repository and license signal were checked; it is not an immutable revision pin.

## Categories

- **Agent and workflow:** coding agents, marketplaces, plugins, MCP servers, skills, and proof protocols.
- **CI, audit, and media:** automation actions, static-analysis and browser-audit tools, deployment utilities, renderers, fonts, and media generators.
- **Python:** direct Python project, optional-extra, development, and build-system declarations.
- **Frontend:** direct application and development declarations, deduplicated by upstream repository.
- **Containers:** directly referenced image definitions and the database software delivered by those images.
- **Research-only/rejected:** evaluated influences, alternatives, false leads, and explicitly rejected options; not shipped dependencies.

## License uncertainty

License labels are discovery aids, not legal advice. **NOASSERTION** means this audit did not establish a reliable repository-wide license; it never means public-domain or unrestricted use. Repository licenses can change, individual subdirectories or plugins can have different terms, container-definition licenses do not relicense bundled software, and model or voice artifacts can have terms separate from their code repositories. Re-check the exact revision and all included assets before copying, modifying, or redistributing anything.

Three caveats deserve special attention:

- Mobbin was named as a UI-reference source without a pinned integration. The listed MCP server is the best-supported canonical match; this ledger does not claim use of a separate Mobbin skills repository.
- Piper was invoked without recording the installed package revision. Both plausible upstream implementations are retained as an explicit ambiguity, and the voice-model license remains separate.
- Motion Ladder exists as a locally copied skill, but its historical public repository URL returned 404 on 2026-08-23. Its license and public provenance remain unresolved.

## Agent and workflow sources

Agents, official marketplaces, MCP servers, installed skills, and review or proof authorities. “Observed” means the source appeared in local setup state; it does not mean this public repository bundles or enables it.

| Project | Relationship | License | Evidence and caveats |
|---|---|---|---|
| [Anthropic Claude Code](https://github.com/anthropics/claude-code) | Primary coding agent and browser-assisted implementation workflow in prior development work. | Proprietary; Anthropic Commercial Terms (repository notice reserves rights) | Historical agent playbook and setup records |
| [OpenAI Codex](https://github.com/openai/codex) | Implementation and adversarial-review agent used in cross-agent workflows. | Apache-2.0 | Historical agent playbook and current setup |
| [OpenAI Plugins](https://github.com/openai/plugins) | Official Codex plugin marketplace and example directory inspected as a setup and plugin source. | NOASSERTION (no repository-wide license detected; individual plugins may differ) | Locally observed Codex plugin catalog Review each selected plugin's own manifest and license before installation. |
| [Claude Code official plugins](https://github.com/anthropics/claude-plugins-official) | Official Claude Code plugin directory used for plugin discovery and installation patterns. | Apache-2.0 for directory code; linked plugin licenses vary | Locally observed Claude Code marketplace |
| [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) | Locally observed official bridge plugin for bounded Claude Code to Codex implementation and review workflows. | Apache-2.0 | Local plugin installation history |
| [claude-mem](https://github.com/thedotmack/claude-mem) | Locally observed Claude Code memory plugin; cited as an optional stateful extension, not bundled here. | Version-dependent: current upstream Apache-2.0; older locally registered marketplace source AGPL-3.0 | Installed claude-mem 12.0.1 cache plus locally registered marketplace checkout 6461d718f25fbe0b02daeda300bfcdcac6bbdb20 Revision: Installed package 12.0.1; marketplace source 6461d718f25fbe0b02daeda300bfcdcac6bbdb20. Current upstream declares Apache-2.0. The older marketplace checkout declares AGPL-3.0, while the installed cache has no project-root LICENSE. Do not retroactively apply the current license to the installed snapshot. |
| [Context Mode](https://github.com/mksglu/context-mode) | Locally observed context-virtualization MCP/plugin used to reduce large tool output in agent sessions. | Elastic-2.0 | Local plugin setup Revision: Installed 1.0.169; marketplace source 4d0e11053e6ad48c8c4497cdb5e5f0eec44209a9. Historical references used the older name mksglu/claude-context-mode; the canonical repository is mksglu/context-mode. |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | Claude Code plugin used for minimal-solution and over-engineering review workflows. | MIT | Historical agent playbook recorded the exact marketplace install |
| [Context7](https://github.com/upstash/context7) | MCP documentation source used for current library and framework references. | MIT | Historical MCP configuration and agent playbook |
| [Mobbin MCP server](https://github.com/mobbin/mobbin-mcp-server) | Best-fit canonical repository for the Mobbin UI-reference workflow named in historical documentation. | MIT | Historical documentation names Mobbin but does not pin a repository or revision The exact Mobbin integration was not recorded. This ledger does not claim use of the separate low-confidence mobbin/skills repository. |
| [assistant-ui skills](https://github.com/assistant-ui/skills) | Source of 13 assistant-ui skills recorded by path and content hash in a historical skills lockfile. | NOASSERTION (no repository license detected) | Historical skills-lock.json with 13 SHA-256 content hashes Citation does not grant permission to copy or redistribute these skills. |
| [Anthropic skills](https://github.com/anthropics/skills) | Source of the frontend-design skill used as a visual implementation authority. | Apache-2.0 for skills/frontend-design; no root repository license detected | Historical frontend product-authority document License is scoped to the referenced skill, not asserted for every directory in the repository. |
| [Fable Method](https://github.com/Sahir619/fable-method) | Source associated with installed proof-loop, method, and independent-judge workflow skills. | MIT | Installed skill names and historical workflow documents The installed copy did not retain an upstream commit pin. |
| [NodeKit](https://github.com/HomenShum/NodeKit) | Repository-contract and product-promotion workflow used to define proof and release gates. | MIT | Historical nodekit contract and promotion goal |
| [Cloudflare OS](https://github.com/cloudflare/cloudflare-os) | Design-pattern inspiration for a locally authored add-dimension skill; no Cloudflare OS code was bundled. | Apache-2.0 | Historical skill attribution header |
| [drawio-skill](https://github.com/Agents365-ai/drawio-skill) | Installed agent skill for generating and validating editable draw.io diagrams. | MIT | Locally installed skill source Revision: Local skill reports 1.14.0; copied snapshot has no upstream commit pin. |
| [draw.io Desktop](https://github.com/jgraph/drawio-desktop) | Native renderer/exporter used by drawio-skill for PNG, SVG, PDF, and editable diagram proof. | Apache-2.0 | drawio-skill runtime dependency and local application setup |
| [Better PR Handoff](https://github.com/HomenShum/BetterPRHandoff) | Locally installed skill for readable commits, branches, pull requests, and change handoffs. | MIT | Locally copied easier-to-read-submissions skill Revision: Local skill 1.0.0; upstream d30f1abc0ff0251000fedf1a3f25d0bad91bba6c. The requested legacy repository name redirects to this canonical repository. |
| [Motion Ladder](https://github.com/HomenShum/motion-ladder) | Locally installed skill for choosing the minimum justified UI motion level. | NOASSERTION (public repository unavailable; local copy has no license) | Locally installed skill source Historical repository URL returned 404 on 2026-08-23. The locally copied v1.0.0 skill remains evidence of use, but public provenance and license could not be established. |
| [Probe First](https://github.com/HomenShum/probe-first) | Locally installed research-before-outreach skill. | MIT | Locally installed skill source Revision: b6298c3f82f57666780bbc1e68ed6595fb97a6d1. |
| [Before/After Proof](https://github.com/HomenShum/before-after-proof) | Locally installed skill requiring before-and-after evidence for code changes. | MIT | Locally installed skill source Revision: e25ab07804da6b410b9cf174284197dec5c1fc06. |
| [Graph Hop](https://github.com/HomenShum/graph-hop) | Installed cross-thread consultation workflow used to query prior design reasoning. | MIT | Global agent instructions and locally installed skill Revision: Local dirty clone base 7674abcd627cfe89b0dc3975273f6a6a499b0d5f; upstream had advanced. |
| [Task Level Guide](https://github.com/HomenShum/task-level-guide) | Locally installed skill for classifying completed engineering tasks by scope and ownership. | MIT | Locally installed skill source Revision: 3ac089392b602d7c4626e821cc4937750cbc288e. |
| [Agentic UI QA](https://github.com/HomenShum/agentic-ui-qa) | Locally installed QA and dogfooding protocol for agentic application interfaces. | MIT | Two locally installed dirty snapshots Revision: Local bases d58d0a509591cf9a5f5c4213e50554371e3bcc35 and d2b2aec91e7596a738f7c72aba2c14b168101a10. |
| [Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) | Interaction-review authority used during frontend promotion. | MIT | Historical frontend product-authority document |
| [Web Quality Skills](https://github.com/addyosmani/web-quality-skills) | Accessibility, performance, best-practice, and web-quality audit skill authority. | MIT | Historical frontend product-authority document |
| [Playwright](https://github.com/microsoft/playwright) | Direct browser runtime and proof authority used by frontend journeys and accessibility checks. | Apache-2.0 | Frontend development manifest and product proof workflow |
| [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Directly observed local Codex MCP server for Chrome inspection, debugging, and browser automation. | Apache-2.0 | Local Codex MCP configuration Exact installed revision was not pinned. |
| [Lightpanda Browser](https://github.com/lightpanda-io/browser) | Directly observed local Codex MCP/browser tool used for anonymous high-volume DOM extraction and replay. | AGPL-3.0 with a commercial licensing option | Local Codex MCP configuration Exact installed revision was not pinned. |
| [Serena](https://github.com/oraios/serena) | Directly observed local Codex MCP server for symbol-level code retrieval, editing, and refactoring. | MIT | Local Codex MCP configuration Exact installed revision was not pinned. |
| [Convex Backend](https://github.com/get-convex/convex-backend) | Canonical source behind the directly observed Convex CLI MCP integration. | NOASSERTION (repository uses a custom or multi-part LICENSE.md; review the exact component and revision) | Local Codex MCP configuration Exact installed CLI revision was not pinned. |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | Directly observed local Codex MCP server for bounded GitHub repository and pull-request operations. | MIT | Local Codex MCP configuration Exact installed revision was not pinned. |

## CI, audit, and media sources

Pinned CI actions, repository-audit utilities, browser quality tools, deployment tooling, and media or visual assets directly used in prior work.

| Project | Relationship | License | Evidence and caveats |
|---|---|---|---|
| [uv](https://github.com/astral-sh/uv) | Python environment, dependency lock, build, and command runner. | MIT OR Apache-2.0 | Historical setup, lockfile, Dockerfile, and CI workflows Revision: 0.9.18 in CI. |
| [setup-uv](https://github.com/astral-sh/setup-uv) | GitHub Action used to install pinned uv and Python versions in CI. | MIT | Historical GitHub Actions workflows Revision: 20cfd1bf945f4377ade1205e4dbc17946fc9a30d (v10.0.1). |
| [checkout](https://github.com/actions/checkout) | GitHub Action used to check out source with persisted credentials disabled. | MIT | Historical workflows and this public setup-kit's validation workflow Revision: 3d3c42e5aac5ba805825da76410c181273ba90b1 (v7.0.1). |
| [setup-python](https://github.com/actions/setup-python) | SHA-pinned GitHub Action used by this public setup kit to install Python for validation. | MIT | Public setup-kit validation workflow Revision: 5fda3b95a4ea91299a34e894583c3862153e4b97 (v7.0.0). |
| [SchemaStore](https://github.com/SchemaStore/schemastore) | Source of the Claude Code settings JSON schema referenced by the public configuration templates. | Apache-2.0 | Public setup-kit Claude settings templates |
| [setup-node](https://github.com/actions/setup-node) | GitHub Action used to install and cache Node.js for frontend gates. | MIT | Historical GitHub Actions workflows Revision: 820762786026740c76f36085b0efc47a31fe5020 (v7.0.0). |
| [upload-artifact](https://github.com/actions/upload-artifact) | GitHub Action used to retain evaluator reports and logs. | MIT | Historical GitHub Actions workflows Revision: 043fb46d1a93c77aae656e7c1c64a875d1fc6a0a (v7.0.1). |
| [Langfuse Experiment Action](https://github.com/langfuse/experiment-action) | Pinned GitHub Action used for hosted evaluation publication and regression gates. | MIT | Historical evaluation workflows Revision: e1f126216d592429e76cef2223f9c57ba03aabe2 (v1.0.7). |
| [shadcn/ui](https://github.com/shadcn-ui/ui) | Component and design-system reference used during frontend composition. | MIT | Historical design-system and frontend workflow records |
| [CodeTour](https://github.com/microsoft/codetour) | VS Code walkthrough format used for repository tours. | MIT | Historical README and .tours artifacts |
| [Knip](https://github.com/webpro-nl/knip) | Frontend unused-file and dependency audit tool used during repository review. | ISC | Historical audit commands and reports |
| [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) | Frontend dependency-graph and architecture audit tool. | MIT | Historical audit commands and reports |
| [jscpd](https://github.com/kucherenko/jscpd) | Duplicate-code audit tool used during repository review. | MIT | Historical audit commands and reports |
| [Vulture](https://github.com/jendrikseipp/vulture) | Python dead-code audit tool used during repository review. | MIT | Historical audit commands and reports |
| [Lighthouse](https://github.com/GoogleChrome/lighthouse) | Rendered web performance and accessibility measurement tool. | Apache-2.0 | Retained frontend promotion commands and reports Revision: 13.4.1 in retained audit commands. |
| [axe-core npm packages](https://github.com/dequelabs/axe-core-npm) | Direct Playwright and CLI accessibility audit packages. | MPL-2.0 | Frontend development manifest and retained accessibility reports Revision: 4.13.0. |
| [Vercel CLI](https://github.com/vercel/vercel) | Deployment CLI used for preview, production, and rollback workflows. | Apache-2.0 | Historical deployment runbook |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Media encoding and verification tool used for product walkthrough artifacts. | LGPL-2.1-or-later for the default core; optional GPL components change obligations | Historical media-generation and verification commands |
| [Cytoscape.js](https://github.com/cytoscape/cytoscape.js) | Graph renderer vendored as a minified runtime asset. | MIT | Vendored bundle header and graph runtime Revision: 3.34.0. |
| [Geist Font](https://github.com/vercel/geist-font) | Frontend font asset source. | OFL-1.1 | Historical frontend asset and design records |
| [FeatureClipStudio](https://github.com/HomenShum/FeatureClipStudio) | Tool used to generate feature walkthrough media and proof artifacts. | MIT | Historical README attribution and generated media workflow An older repository name redirected to this canonical repository. |
| [Piper (current OHF implementation)](https://github.com/OHF-Voice/piper1-gpl) | One possible upstream for a historically invoked `python -m piper` text-to-speech step. | GPL-3.0 | Historical media command named Piper but did not record its package revision Included to expose ambiguity, not to assert that this implementation produced the artifact. |
| [Piper (archived rhasspy implementation)](https://github.com/rhasspy/piper) | Alternative archived upstream that may match the historically invoked Piper package. | MIT | Historical media command did not record the installed package revision Repository is archived. The exact Piper implementation and voice-model license remain unresolved. |

## Python projects

First-party repositories behind direct Python manifest declarations. Optional and development extras are included; lockfile-only transitive packages are not.

| Project | Relationship | License | Evidence and caveats |
|---|---|---|---|
| [FastAPI](https://github.com/fastapi/fastapi) | Direct Python dependency for HTTP application surfaces. | MIT | Historical Python manifest and lockfile |
| [Uvicorn](https://github.com/Kludex/uvicorn) | Direct Python dependency and production ASGI server. | BSD-3-Clause | Historical Python manifest, Dockerfile, and lockfile |
| [HTTPX](https://github.com/encode/httpx) | Direct Python dependency for bounded external HTTP requests. | BSD-3-Clause | Historical Python manifest and lockfile |
| [NumPy](https://github.com/numpy/numpy) | Direct Python dependency for vector and numeric operations. | BSD-3-Clause for NumPy; bundled components may carry additional notices | Historical Python manifest and lockfile |
| [Pydantic](https://github.com/pydantic/pydantic) | Direct Python dependency for validated request, response, and workflow contracts. | MIT | Historical Python manifest and lockfile |
| [OpenAI Python](https://github.com/openai/openai-python) | Direct Python SDK dependency for model planning and evaluation. | Apache-2.0 | Historical Python manifest and lockfile |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Direct Python dependency for optional local environment loading. | BSD-3-Clause | Historical Python manifest and lockfile |
| [assistant-ui](https://github.com/assistant-ui/assistant-ui) | Monorepo behind the direct Python assistant-stream package and direct frontend assistant-ui packages, templates, and shimmer plugin. | MIT | Historical Python and frontend manifests, lockfiles, and template history |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Direct Python dependency for workflow graphs and PostgreSQL checkpoints. | MIT | Historical Python manifest and lockfile |
| [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk) | Direct Python dependency for the stdio MCP server surface. | MIT | Historical Python manifest and MCP implementation |
| [Langfuse Python SDK](https://github.com/langfuse/langfuse-python) | Direct Python dependency for evaluation tracing and hosted experiment publication. | MIT | Historical Python manifest, lockfile, and evaluation workflows |
| [PyJWT](https://github.com/jpadilla/pyjwt) | Direct Python dependency for authenticated workflow token validation. | MIT | Historical Python manifest and lockfile |
| [pytest](https://github.com/pytest-dev/pytest) | Direct development dependency and scenario-test runner. | MIT | Historical Python development manifest and CI |
| [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) | Direct development dependency for async scenario tests. | Apache-2.0 | Historical Python development manifest and CI |
| [asyncpg](https://github.com/MagicStack/asyncpg) | Direct optional Python dependency for PostgreSQL persistence. | Apache-2.0 | Historical Python optional-dependency manifest and lockfile |
| [Psycopg](https://github.com/psycopg/psycopg) | Direct optional Python dependency for PostgreSQL checkpointing and pooling. | LGPL-3.0-only | Historical Python optional-dependency manifest and lockfile |
| [Neo4j Python Driver](https://github.com/neo4j/neo4j-python-driver) | Direct optional Python dependency for the graph index. | Apache-2.0 AND Python-2.0 | Historical Python optional-dependency manifest and lockfile |
| [Model2Vec](https://github.com/MinishLab/model2vec) | Direct build-time-only Python dependency used to bake static entity embeddings. | MIT | Historical Python optional-dependency manifest and build script The separately downloaded model artifact has its own model-card terms and is not represented by this code license. |
| [Hatch](https://github.com/pypa/hatch) | Build backend and packaging tool declared by the Python project. | MIT | Historical Python build-system declaration and lockfile |

## Frontend projects

First-party repositories behind direct frontend manifest declarations. Multiple packages from one monorepo appear once.

| Project | Relationship | License | Evidence and caveats |
|---|---|---|---|
| [Vercel AI SDK](https://github.com/vercel/ai) | Direct frontend dependencies for streamed AI chat state and protocol handling. | Apache-2.0 | Historical frontend manifest and lockfile |
| [Base UI](https://github.com/mui/base-ui) | Direct frontend dependency for accessible unstyled UI primitives. | MIT | Historical frontend manifest and lockfile |
| [OpenTelemetry JavaScript](https://github.com/open-telemetry/opentelemetry-js) | Direct frontend dependency for telemetry API contracts. | Apache-2.0 | Historical frontend manifest and lockfile |
| [Sigma.js](https://github.com/jacomyal/sigma.js) | Direct frontend graph rendering and node-border package source. | MIT | Historical frontend manifest and lockfile |
| [WorkOS AuthKit for Next.js](https://github.com/workos/authkit-nextjs) | Direct frontend dependency for authenticated Next.js routes. | MIT | Historical frontend manifest and lockfile |
| [WorkOS Node SDK](https://github.com/workos/workos-node) | Direct frontend-server dependency for WorkOS API integration. | MIT | Historical frontend manifest and lockfile |
| [Class Variance Authority](https://github.com/joe-bell/cva) | Direct frontend dependency for component variant composition. | Apache-2.0 | Historical frontend manifest and lockfile |
| [clsx](https://github.com/lukeed/clsx) | Direct frontend dependency for conditional class-name composition. | MIT | Historical frontend manifest and lockfile |
| [Graphology](https://github.com/graphology/graphology) | Direct frontend dependency source for graph data structures and graphology-layout-forceatlas2. | MIT | Historical frontend manifest and lockfile |
| [Lucide](https://github.com/lucide-icons/lucide) | Direct frontend icon dependency. | ISC | Historical frontend manifest and lockfile |
| [Next.js](https://github.com/vercel/next.js) | Direct frontend framework and production server. | MIT | Historical frontend manifest, lockfile, and Dockerfile Revision: 16.3.0 in the audited manifest. |
| [React](https://github.com/react/react) | Direct frontend UI runtime dependency. | MIT | Historical frontend manifest and lockfile |
| [remark-gfm](https://github.com/remarkjs/remark-gfm) | Direct frontend dependency for GitHub-flavored Markdown rendering. | MIT | Historical frontend manifest and lockfile |
| [tailwind-merge](https://github.com/dcastil/tailwind-merge) | Direct frontend dependency for deterministic Tailwind class conflict resolution. | MIT | Historical frontend manifest and lockfile |
| [tw-animate-css](https://github.com/Wombosvideo/tw-animate-css) | Direct frontend dependency for Tailwind animation utilities. | MIT | Historical frontend manifest and lockfile |
| [Zustand](https://github.com/pmndrs/zustand) | Direct frontend dependency for client state management. | MIT | Historical frontend manifest and lockfile |
| [Tailwind CSS](https://github.com/tailwindlabs/tailwindcss) | Direct frontend styling and PostCSS dependency. | MIT | Historical frontend development manifest and lockfile |
| [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped) | Source repository for direct @types/node, @types/react, and @types/react-dom development packages. | MIT for the referenced package declarations; individual definitions track upstream projects | Historical frontend development manifest and lockfile |
| [esbuild](https://github.com/evanw/esbuild) | Direct frontend build dependency and compiler used by browser-model gate tests. | MIT | Historical frontend development manifest, lockfile, and test harness |
| [Oxc](https://github.com/oxc-project/oxc) | Direct frontend formatter and linter toolchain behind oxfmt and oxlint. | MIT | Historical frontend development manifest and scripts |
| [TypeScript](https://github.com/microsoft/TypeScript) | Direct frontend type checker and compiler dependency. | Apache-2.0 | Historical frontend development manifest and CI |

## Container and database projects

Repositories behind directly referenced images plus the database runtime where the image-definition license does not cover the bundled database.

| Project | Relationship | License | Evidence and caveats |
|---|---|---|---|
| [pgvector](https://github.com/pgvector/pgvector) | Pinned PostgreSQL image extension used by CI and local compose for vector storage. | PostgreSQL License | Historical compose and CI service image Revision: 0.8.6-pg16-bookworm (CI image also digest-pinned). |
| [Postgres Docker Official Image](https://github.com/docker-library/postgres) | Source definitions for the directly referenced postgres:16-alpine development image. | MIT for image definitions; PostgreSQL itself has the PostgreSQL License | Historical local compose image Revision: 16-alpine. |
| [PostgreSQL](https://github.com/postgres/postgres) | Database runtime delivered by the directly used PostgreSQL and pgvector container images. | PostgreSQL License | Historical local and CI database services |
| [Neo4j Docker image](https://github.com/neo4j/docker-neo4j) | Source for the directly referenced neo4j:5-community compose image. | Apache-2.0 for image tooling; bundled Neo4j edition terms are separate | Historical local and production compose images Revision: 5-community. |
| [Neo4j](https://github.com/neo4j/neo4j) | Community graph-database runtime delivered by the directly used Neo4j container image. | GPL-3.0-only for Community Edition; Enterprise Edition uses separate commercial terms | Historical optional graph service and compose image |
| [Python Docker Official Image](https://github.com/docker-library/python) | Source definitions for directly used python:3.13-slim-bookworm build and runtime images. | MIT for image definitions; bundled software retains its own licenses | Historical backend Dockerfile Revision: 3.13-slim-bookworm. |
| [Node.js Docker Official Image](https://github.com/nodejs/docker-node) | Source definitions for directly used node:22-bookworm-slim frontend images. | MIT for image definitions; bundled software retains its own licenses | Historical frontend Dockerfile Revision: 22-bookworm-slim. |

## Research-only and rejected sources

Projects explicitly evaluated, compared, rejected, or corrected during research. They are citations, not application dependencies, and no code-copy claim is made.

| Project | Relationship | License | Evidence and caveats |
|---|---|---|---|
| [Prime Agent](https://github.com/PrimeIntellect-ai/prime-agent) | Research-only comparison for agent architecture; not installed, vendored, or shipped. | MIT | Historical architecture research notes |
| [HyperAgents](https://github.com/facebookresearch/HyperAgents) | Research-only influence for hierarchical agent design; no source code was copied. | CC-BY-NC-SA-4.0 | Historical architecture research and canonical-source correction Non-commercial and ShareAlike terms make this unsuitable as a normal production-code dependency. |
| [Claw Code](https://github.com/ultraworkers/claw-code) | Research-only agent-tool comparison; explicitly not adopted or copied. | MIT | Historical research notes Past review treated provenance as requiring a fresh, revision-specific audit before any adoption. |
| [Humanizer](https://github.com/blader/humanizer) | Research-only writing-style comparison; not installed or copied into the application. | MIT | Historical workflow research notes |
| [GraphRAG](https://github.com/microsoft/graphrag) | Research-only graph-retrieval architecture comparison; not a runtime dependency. | MIT | Historical graph architecture research |
| [Graphiti](https://github.com/getzep/graphiti) | Research-only temporal knowledge-graph comparison; not a runtime dependency. | Apache-2.0 | Historical graph architecture research |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | Research-only agent-harness comparison; not installed or shipped. | MIT | Historical agent architecture research |
| [Kuzu](https://github.com/kuzudb/kuzu) | Evaluated and rejected graph-database option; not a runtime dependency. | MIT | Historical graph storage comparison Repository was archived when rechecked. |
| [HyperAgent (FSoft-AI4Code)](https://github.com/FSoft-AI4Code/HyperAgent) | Historical name-collision false lead; rejected after identifying Meta's HyperAgents as the intended source. | Apache-2.0 | Historical canonical-source correction |

## Publication boundary

This catalog attributes external work; it does not relicense it. The public setup kit contains newly written documentation and templates, not copied private application source, session transcripts, credentials, caches, browser profiles, or generated runtime state. Historical evidence is summarized generically so the attribution remains useful without exposing a private repository.
