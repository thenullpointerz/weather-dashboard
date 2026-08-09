# Weather Dashboard

A weather dashboard for Mexico City showing current conditions, an hourly forecast, a 7-day forecast, and a temperature trend chart — with an AI-generated one-line summary of the day's weather.

Live: https://weathy-dashboard.web.app

## How it works

A Python script fetches weather data from the [Open-Meteo API](https://open-meteo.com/) (no API key required) and writes it to `weather_data.json`. A GitHub Actions workflow runs that script every hour and commits the updated file back to this repo. The React dashboard fetches `weather_data.json` directly from GitHub's raw content URL on page load, so it always shows the latest data without needing to be redeployed.

```
Open-Meteo API ──(hourly cron)──▶ fetch_weather.py ──▶ weather_data.json ──▶ committed to repo
                                                                                     │
                                                                                     ▼
                                                              dashboard fetches raw JSON on load
```

`weather_data.json` includes 7 days of historical data alongside the 7-day forecast (via Open-Meteo's `past_days` parameter), which is what powers the trend chart.

## Tech stack

**Data pipeline**
- [Python](https://www.python.org/) + [`requests`](https://pypi.org/project/requests/) — fetches and reshapes the Open-Meteo response
- [Anthropic Claude API](https://www.anthropic.com/) (Claude Haiku 4.5) — generates the one-line weather summary
- [GitHub Actions](https://github.com/features/actions) — runs the fetch script on an hourly schedule

**Dashboard** (`dashboard/`)
- [React 19](https://react.dev/) + [Vite](https://vitejs.dev/)
- [Recharts](https://recharts.org/) for the temperature trend chart
- [Firebase Hosting](https://firebase.google.com/docs/hosting) for deployment

## Getting started

### Data pipeline

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # or `source .venv/Scripts/activate` in Git Bash
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "your-key-here"   # optional — see below
python fetch_weather.py
```

This writes `weather_data.json` in the project root. If `ANTHROPIC_API_KEY` isn't set (or the Anthropic account has no API credit), the script still runs fine — it just skips the `summary` field and logs a warning instead of failing.

### Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:5173. The dashboard fetches data straight from this repo's `master` branch on GitHub, so it works the same locally as in production.

## GitHub Actions setup

The workflow (`.github/workflows/fetch_weather.yml`) needs one repo secret:

| Secret | Used for |
|---|---|
| `ANTHROPIC_API_KEY` | Generating the weather summary. If unset, the summary is silently skipped (see above). |

Set it with:

```bash
gh secret set ANTHROPIC_API_KEY --repo <your-username>/weather-dashboard
```

The workflow also needs `permissions: contents: write` (already set in the workflow file) so it can commit the updated `weather_data.json` back to the repo.

## Deployment

The dashboard deploys to Firebase Hosting:

```bash
cd dashboard
npm run build
npx firebase deploy
```

`dashboard/firebase.json` and `dashboard/.firebaserc` point at the `weathy-dashboard` Firebase project; update `.firebaserc` if you're deploying to your own project.

## History

This project started as [Weathy](https://github.com/thenullpointerz/Weathy), a Spring Boot + Twitter bot that posted Mexico City's weather every 6 hours. That bot's hosting went down and it's since been retired — this dashboard is its replacement, rebuilt from scratch with a static-site + GitHub Actions architecture instead of a standing backend server.
