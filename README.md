## <!-- <h1>Attendance System Server API + Database</h1> -->

<div style="width: 100%; display: flex; justify-content: center; align-items:center; margin: 20px;">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQn_3MFhCzXcwI3GWIDTsWJg2HXDTG7TwGovA&s" alt="FastAPI logo" style="height: 100px; width: 100px;" />
</div>

<br />

Tech used:

-   FastAPI
-   MySQL
-   PyJWT
-   SQLAlchemy

<br />

You must have these installed on your machine:

-   [x] Python 3.11.\*
-   [x] MySQL
-   [x] Visual Studio Code or PyCharm
-   [x] Docker Desktop

<br />

<h4>Installation and setup (Localhost)</h4>

```bash

git clone git@github.com:itsmenoahpoli/jfca-fastapi-api.git

cd jfca-attendance-system-api

python -m venv .venv

# For windows
.venv/Scripts/activate

# For MacOS
source .venv/bin/activate

pip install -r requirements.txt

fastapi dev app/main.py
```

<hr />

<h4>Installation and setup (Docker)</h4>

```bash

docker compose build

docker compose up -d

```

API Swagger documentation can be found at: `http://localhost:8000/docs` or `http://localhost:8000/redoc`
