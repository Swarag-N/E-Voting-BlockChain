# E-Votings System Based on Blockchain

## Project Report

### Fall Semester 2020

| Course Code |         Course Name         | Slot |
| :---------: | :-------------------------: | :--: |
|  `BCI3004`  | Security of E-Based Systems |  F1  |

### Under Guidance 0f

## Ananda Kumar S Sir (SCOPE)

### Teammates

- Swarag Narayanasetty (18BCI0154)
- P. Sai Rama Reddy (18BCI0119)
- Koka Vyshnav (18BCI0135)

---

## Basic Requiremnts

Softwares Used are

- Postman
- Docker
- VS Code
- ngrok

## Installation is Staight forward for

Postman, VS Code

### Docker

- Better work with Docker Desktop
- Keep the Docker Installation in WSL( Windows Sub System for linux)

#### ngrok

- Used for port mapping to the cloud so that everything can be accesdd from the internet
- Use the Official Documentation, straight forward

---

## Setting Up Work Environment

- It is better to use virtual env of python
  refer from :- `url https://docs.python.org/3/tutorial/venv.html`
  in app working directory

```bash
python3 -m venv voting
```

Once you’ve created a virtual environment, you may activate it.

On Windows, run:

```bash
voting\Scripts\activate.bat
```

On Unix or MacOS, run:

```bash
source tutorial-env/bin/activate
```

---

## Installing Dependencies

in app working directory

```bash
python3 install -r requirments.txt
```

This would install all the Dependencies

## You can run check the Application by

```bash
python3 app.py
```

## For checking with mutliple ports on same system, it is requested to docker along with ngrok

Build a docker image,

```bash
docker build -t voting .
```

Run the image as container

```bash
docker run --rm -p 4000:5000 blockchain //1
```

now using ngrock we can publish the routes
this below snippet is to run in Ubuntu(Windows Subsystem for Linux)

```bash
ngrok http 4000 //2
```

this would provide an url to access the servers

if wanted check with many other servers start

---

## Checking

now in the POSTMAN Application, import the given collection which will be in JSON form
after importing check the environment variables to the url given in ngrok
