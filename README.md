# pyce-cream API

## Main Components

* Python 12.x
* [FastApi 0.111.x](https://fastapi.tiangolo.com/tutorial/)
* [FastApi - Cache 0.2.1](https://pypi.org/project/fastapi-cache2/)
* [SQLAlchemy 2.x](https://docs.sqlalchemy.org/en/20/contents.html)

## Configuring Environment

1. Install [Python 3.12](https://www.python.org/downloads/)
2. Create a virtual env and install dependencies
```bash
pyce-cream-api$ python3.12 -m venv ./env
pyce-cream-api$ source env/bin/activate
(env) pyce-cream-api$ pip install -r requirements.txt
```
3. Inspect/Edit with your preferred IDE
4. Run or Build a docker image
```bash
(env) pyce-cream-api$ fastapi dev main.py --port 8000
```
```bash
(env) pyce-cream-api$ docker build -t pyce-cream .
```
5. Optionally, run tests from `test_main.http`

### Project Structure

```
├── Dockerfile
├── infra
│   └── ...
├── main.py
├── models
│   └── ...
├── requirements.txt
├── routes
│   └── ...
├── test_main.http
└── ucs
    ├── flavor
    │   └── ...
    ├── token
    │   └── ...
    └── user
        └── ...
```

* **Dockerfile** - Minimal configuration to build an image
* **infra** - Database, repositories and other infra-related scripts
* **models** - Core models of this API
* **requirements.txt** - Project dependencies - install them before running the project
* **routes** - FastAPI routes definition scripts
* **test_main.http** - Sample requests
* **ucs** - Use cases around _flavor, user and jwt-tokens_