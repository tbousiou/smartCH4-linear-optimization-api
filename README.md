# smartCH4 Biogas Waste Optimization API
Optimize the cost of waste for biogas production using linear programming. For a given list of substrates and their characteristics find the optimal mix that optimizes cost while keeping the biogas production in a given target.

# Installation
Clone the repo

`git clone repo_url`

Install a python virtual environment and required packages.

`python3 -m venv venv`

`source venv/bin/activate`

`pip install fastapi ortools pandas` or `pip install -r requirements.txt`

# Execution
For development use `dev` command

`fastapi dev api.py`

For production use `run` command. You mighy need to specify a port number with `xxxx`

`fastapi run api.py --port xxxx`

# Deploy as a Linux service
For production it's better to create a linux systemd service.

Edit `example.service` and replace `/path_to_app` with

Copy `example.service` to `/etc/systemd/system`

Reload the service files to include the new service.

`sudo systemctl daemon-reload`

Start your service

`sudo systemctl start your-service.service`

To enable your service on every reboot

`sudo systemctl enable example.service`

Of course there other ways for deployment see https://fastapi.tiangolo.com/deployment/