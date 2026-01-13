# ciso-cli

Minimal Typer-based CLI client for CISO Assistant API.


## Development workflow
To code the CLI, use the following workflow:
```bash
docker run -v $PWD:/usr/src/app -it --rm  python:3.11 /bin/bash
cd /usr/src/app
ciso build info
```

This will allow for a consistent development environment where the code is executed in the container.




# Testing

```bash
pip install -e ".[test]"

pytest
```

## Con coverage:

```bash
pytest --cov=ciso_cli --cov-report=term-missing
```
