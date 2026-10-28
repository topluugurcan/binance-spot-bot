# Binance Spot Signal Bot (safe starter)

This starter reads public Binance Spot candle data and prints a basic EMA 9/21 signal.
It does **not** connect to a trading account and does **not** place real orders.

## Files
- `bot.py` — signal-only Python script
- `requirements.txt` — dependency
- `.github/workflows/bot.yml` — manual GitHub Actions workflow

## Run in GitHub
1. Create a **private** repository named `binance-spot-bot`.
2. Add these three files, preserving the `.github/workflows/bot.yml` path.
3. Open **Actions** → **Binance Spot Signal Bot** → **Run workflow**.
4. Open the run and inspect the `Run signal bot` step logs.

## Safety
- Never commit API keys or secrets.
- This project has no code to submit orders.
- A GitHub Actions workflow is not a 24/7 trading service; this workflow runs only when manually triggered.
- EMA signals are educational and do not guarantee profit.
