# Simple Habit Tracker

A very simple and minimalistic habit tracker.

## Backend

### Running locally

Ensure you have docker installed, and simply run:

```bash
cd backend
docker compose up
```

The server should be available at http://localhost:8080

### Running tests

Ensure you have Python3 installed, then create and activate a virtual environment:

```bash
cd backend
python3 -m venv venv
. venv/bin/activate
```

Then install the required dependencies:

```bash
pip3 install -r requirements.txt
```

Finally, run the pytest tests:

```bash
python3 -m pytest
```

## Frontend

![Screenshot of app](./docs/screenshots/app.png)

The frontend is compatible with the backend implementation, modulo the streak
and last check-in date summaries, which are not currently returned by the
`GET /habits` endpoint.

### Running locally

Ensure you have node.js and npm installed, then run:

```bash
cd frontend
npm install
npm run dev
```

The app should load at http://localhost:5173

### Browser compatibility

The base app has been tested on the latest versions of Firefox and Chrome.
Styling might not work on e.g. older versions of Safari, due to the use of the
new [CSS nesting](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting)
feature.

For date calculations (number of days since last check in), the cutting-edge
[Temporal
API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal)
was used (for fun and experimentation), which as of the time of writing, is only
supported in Firefox (v139+). For production, we could use a polyfill, an
existing npm library, or simply write the date comparison function ourselves.
