# heatmaps

## Contributing

### Initial Dev environment Setup
This project uses Poetry as the dependency manager.
Run `poetry install` to install all dependencies.
Then run `poetry run pre-commit install` to install pre-commit hooks.

This project also uses npm for managing the CSS and JavaScript files during development.
Run `npm install` to install the development dependencies.

### Working with Javascript and CSS files

#### CSS
The css files are compiled using Sass. When you have finished writing in the `main.sass` file, run `npm run css-build` to compile it into a css file in the same directory.

Alternatively, if you prefer to see the changes as you are writing to the file, you can run `npm run css` to automatically compile the `main.sass` file whenever you make changes as long as the process is running in the terminal.

#### Javascript
When you want to deploy the app, minify the files using `npm run minify-js --jsfilepre=JSfilename.js --jsfilepre=JSfilename.min.js`. This will create a new `.js` file, so don't forget to correct your html files

Minification can help load your website several times faster, so make sure to do it before deployment.

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
