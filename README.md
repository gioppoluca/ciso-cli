# ciso-cli

Minimal Typer-based CLI client for CISO Assistant API.


## Development workflow
To code the CLI, use the following workflow:
```
docker run -v $PWD:/usr/src/app -v /var/run/docker.sock:/var/run/docker.sock -it --rm  python:3.9.10 /bin/bash
cd /usr/src/app
pip3 install -r requirements.txt
python main.py prepare prepare
```

This will allow for a consistent development environment where the code is executed.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .

cp .env.example .env
# edit .env

ciso build info
```
