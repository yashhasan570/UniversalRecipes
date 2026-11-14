# Universal Recipes

Self-hosted recipe manager and meal planner: import recipes from the web, plan meals on a calendar, and build shopping lists automatically.

## Features

- Web recipe import (URL scraping) and rich recipe editing
- Meal planner with calendar, automatic shopping lists
- Multi-user households with fine-grained permissions
- REST API and OpenAPI docs for integrations
- Web + mobile-friendly frontend, PWA

## Install

- Docker: `docker compose up` with the provided compose files in `docker/`
- From source: Python backend (`uv sync` + `uvicorn`) and Nuxt frontend (`pnpm install && pnpm build`)

Configuration is environment-based: every `UNIVERSALRECIPES_*` variable can be set in `.env` (see `.env.example`).

## Contact

Telegram: [@johnconstantine570](https://t.me/johnconstantine570)
