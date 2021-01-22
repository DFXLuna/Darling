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

## TODO(priority order): 
- Add problem submission commands
  - Backup, send to judges
      - list_ungraded_submissions
      - factor judge check
      - list_team_submissions
      - allow claiming specific problem
      - judge_help, student_help
  - Primary, autograde
  - Event start time
    - Could use cog loading and unload to facilitate this
  - optimize mutex locks
  - Remote client failsafe
