# DivineGuard GovCon Pulse

GovCon Pulse is a DivineGuard IT Services LLC product initiative, founded and created by Aaron Frazier Jr.

A runnable Python and SQLite starter for a government-contract opportunity pipeline. It stores a title, official source link, stage and optional evidence link. It is a local command-line application, with no external dependencies, frontend, live SAM.gov import or cloud synchronization.

## Quick start

Complete the development setup below, then run:

```sh
python -m pulse add "Example opportunity - replace before use" https://sam.gov/
python -m pulse list
# Use the ID printed by add:
python -m pulse stage RECORD_ID Watching
python -m pulse stage RECORD_ID Submitted --evidence https://example.com/replace-with-receipt
```

The sample is illustrative only. Replace evidence URLs with real accessible records; the starter validates URL syntax but does not fetch or independently verify evidence. It never submits a bid.

The default database is `data/pulse.db`. To select another database, set `PULSE_DB` in your shell or pass `python -m pulse --db /private/path/pulse.db list`. `.env` is not automatically loaded in this repository. Copying `.env.example` alone does not change configuration.

## Data model and evidence

Stages: Imported, Watching, Drafting, Submitted, Received, Awarded, Paid and Passed. New entries always start as Imported. Submitted, Received, Awarded and Paid require an evidence URL. Stages remain user-entered claims. An award requires award evidence; payment requires payment evidence. A research link or AI response is not either.

SQL statements bind parameters. Source and evidence links must use HTTPS and cannot include embedded credentials. The database is local and unencrypted; use an access-controlled disk. There is no multi-user authorization, immutable event history, evidence validation, migration framework, backup automation or deadline scheduler yet. Stage updates replace the current evidence field, so this is not an audit ledger.

## Tests and next implementation steps

Tests cover persistence, quoted input, source URL rejection, evidence requirements and invalid updates. Next: add append-only stage history, schema migrations, controlled import/export, authenticated backend and official-notice ingestion. Move storage behind an API before connecting a browser or mobile client.

## Repository family

| Repository | Responsibility |
| --- | --- |
| [GovCon Pulse](https://github.com/Mrfrazier14/divineguard-govcon-pulse) | Local opportunity tracking and evidence links |
| [Gray Fox AI](https://github.com/Mrfrazier14/divineguard-gray-fox-ai) | Server-side Anthropic and OpenAI adapters |
| [SaaS Platform](https://github.com/Mrfrazier14/divineguard-saas-platform) | Shared AWS identity, storage and runtime foundation |

## Development

Python 3.11+ is required. Each repository has its own environment; run commands from its root.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

GitHub Actions runs tests on Python 3.11 and 3.13. `.env`, local databases, virtual environments and AWS configuration are ignored. `.env.example` contains placeholders only. Never commit keys, credentials, customer data or bid evidence containing private information.

Read [architecture](docs/ARCHITECTURE.md) for the future integration boundary. These are new starter implementations; they do not migrate the earlier desktop application or hosted pilot. No production readiness, live billing, bid submission or deployed AWS service is implied.
