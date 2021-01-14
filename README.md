# Darling


## Build requirements
  - python  >= 3.5
  - discord.py `pip install discord.py`

## To run
  - Install requirements with pip
  - Run src/main.py

## TODO(priority order): 
- Add problem submission commands
  - Backup, send to judges
    - Figure out how to represent and claim submissions
      - Seperate claiming and judging
        - Post submission to judge channel, emoji reaction to claim
        - On claim, DM judge with details. Judge can now run pass or fail commands with failure reason
  - Primary, autograde
  - Event start time
  - Remote client failsafe
