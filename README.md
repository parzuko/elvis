<p align = "center">
  <a href="https://discord.com/api/oauth2/authorize?client_id=755529764835426355&permissions=8&scope=bot"><img alt="Elivs" src="top.png"></a>
</p>

#### Elvis is a music + utility bot written in python using [discord.py](https://discordpy.readthedocs.io/en/latest/). Elvis comes with all traditional music commands and a few easter egg commands. Use Elvis as is, or set him up your way!


## :computer: Installing Locally

```bash

# install ffmpeg
sudo apt update
sudo apt install ffmpeg

# Clone this repository.
git clone https://github.com/parzuko/elvis.git
cd elvis

# install pipenv
pip install pipenv

# Install dependencies
pipenv install --ignore-pipfile

# only for linux
pipenv uninstall discord
pipenv install discord.py[voice]

# Run it locally
pipenv run main.py
```

---

Made with ♥ by Jivansh Sharma :v: [Say Hi!](https://www.linkedin.com/in/jivansh/)