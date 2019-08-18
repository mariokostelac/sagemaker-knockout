# 🥊 sagemaker-knockout
Knock the SageMaker instance out when it's not active!

## ❓ Why?
Are you enjoying big powerful, pricey SageMaker instances to experiment with your data, but often forget to shut it down after you're done? 💸💸💸😳

`sagemaker-knockout` will knock your machine out when it's inactive! 👾

## ⚙️ How does it work?
It tracks three metrics to detect the activity. If any of them report as active, machine will not shut down.
- **Jupyter connections** - if Jupyter server has incoming connections opened, it means you have an open console or notebook tab (with laptop opened). We do not want to shut the machine down in that case
- **GPU usage** - if you've left your laptop closed, but are running GPU intensive operations, we'll detect that (threshold is set to 5%)
- **GPU usage** - if you've left your laptop closed, but are running CPU intensive operations, we'll detect that (threshold is set to 10%)

## 🧠 Setup
In order to make sure you don't need to remember to run this program to shut down your machine 😅, the most covenient setup is to change the SageMaker's lifecycle configuration.

Add this snippet of code to "Start notebook" script:
```bash
#!/bin/bash

# make the script fail if anything fails
set -e

# set up the language so we don't support just ASCII
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

echo "Setting up 🥊 sagemaker-knockout..."
pip3 install sagemaker-knockout
python3 -m sagemaker_knockout run --daemonize --max-inactive-minutes 60
sleep 3
python3 -m sagemaker_knockout check-daemon
```

As you can guess, we are running this program in the background (daemonizing) and you can change the inactivity period after which the shutdown process kicks in. Feel free to change it to any number that suits you (yes, I do like long lunch breaks 🍔).
