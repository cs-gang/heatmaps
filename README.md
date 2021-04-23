# heatmaps

## Contributing

### Initial Dev environment Setup
This project uses Poetry as the dependency manager.
Run `poetry install` to install all dependencies.
Then run `poetry run pre-commit install` to install pre-commit hooks.

### Running
The project can be run using docker-compose:
`docker compose up`

Alternately, to run without Docker:
**Step 0: Install all dependencies**
This project uses MongoDB, and you will need a local instance running if you want to run
this project.

**Step 1: Make a `.env` file**
The `.env` must contain the following:
```
DATABASE_URL=<your database URI here>
DEBUG=true
```
