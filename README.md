# Darling


## Build requirements
  - python  >= 3.5
  - discord.py `pip install discord.py`

## To run
  - Install requirements with pip
  - export your bot token as the environment variable `BOT_TOKEN`
    - On linux `export BOT_TOKEN=token`
  - Run src/main.py
    - On ubuntu 20.04 `python3 src/main.py`

# Before Contest
- Set problem number in submission database
- Set point values in teamScores

## TODO(priority order):
- Check passes of particular problem
- Check team score
- Event start time
  - Could use cog loading and unload to facilitate this
- Async reg flush
- optimize mutex locks
- optimize multiple awaits to concurrent


## Bugs
- (Unconfirmed) Issue claiming by uuid the last problem in list
