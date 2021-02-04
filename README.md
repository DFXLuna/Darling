# Darling


## Build requirements
  - python  >= 3.7
  - discord.py `pip install discord.py`

## To run
  - Install requirements with pip
  - export your bot token as the environment variable `BOT_TOKEN`
    - On linux `export BOT_TOKEN=token`
  - Run src/main.py
    - On ubuntu 20.04 `python3 src/main.py`

# Before Contest
- Set problem number in submission database and scoringCog
- Set point values in teamScores

## TODO(priority order):
- open_submissions
- close_submissions
- Async reg flush
- optimize mutex locks
- optimize multiple awaits to concurrent

## Bugs
