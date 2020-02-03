# ecp-grade-notifier

A Github Action that sends you a Telegram message when you get a new grade on [notesetdossier.ecp.fr](http://notesetdossier.ecp.fr/).

## How it works

- it runs every N minutes (thanks to a scheduled Github Action)

- it uses [Selenium for Python](https://selenium-python.readthedocs.io/) and its [Gecko driver](https://github.com/mozilla/geckodriver) (\~ headless Firefox) to go to [notesetdossier.ecp.fr](http://notesetdossier.ecp.fr/) and fetch your grades

- it compares the fetched grades with your previous grades (_hacky_: your previous grades are stored _inside_ the repository)

- if a change was made, it sends you a Telegram message and then commits the new grades to the repo (_note_: you should get pinged **at least once**, because the script sends you the message before attempting to commit the new grades)

## Setup

- fork this repository

  _important_: make the fork private if you don't want your grades to be public

- add two [secrets](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets) to your repository

  - `ECP_SSO_PASSWORD`: your ECP CAS password

  - `TELEGRAM_BOT_TOKEN`: a valid Telegram bot token
    - create a Telegram bot using [BotFather](https://telegram.me/BotFather)
    - send `/start` to the bot on Telegram (otherwise it can't send you private messages)

- update the relevant constants in `env.sh`

  - `TELEGRAM_CHAT_ID`: you can use [the user info bot](https://t.me/userinfobot) to get your personal user id

  - other constants are self-explanatory

- push the `env.sh` update

- if everything went well

  - you should receive a message with your current grades within 2 minutes

  - the action should have committed your current grades in `data/grades`

  - the logs should be available in the actions tab of your fork

  - the action should run every 30 minutes in the future

    _disclaimer_: the action takes about 1 minute to run, which can eat a significant chunk of your 2000 minutes monthly quota, you can update the CRON expression in `.github/workflows/alert.yml` to make it run less frequently
