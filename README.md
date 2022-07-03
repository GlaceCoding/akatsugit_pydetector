# akatsugit_pydetector
This is a personnal learning **fullstack** project to learn how to do datascience with python some data in an API REST. 

**Archived project:** Matplotlib is nice to use but need to be server side, that why I will do math in clientside with JS. See: https://github.com/GlaceCoding/42iceberg

**WARNING: DEV IN PROGRESS**

Actually graph appear in CLI: (Next step will be to use Flask+ReactJS).

<img src="https://user-images.githubusercontent.com/92152391/163854380-9a800a39-01a0-44e7-84f7-7fd7671db8e7.png" width="480" />

## Install

Requires python3.1+, and pip.

1. Install (with the Makefile):

```sh
make
```

2. Copy `default.yml` and paste to `local.yml` in `./app/config`, replace `{SECRET}` with our secret data. You have to make a new application in [the 42 API](https://profile.intra.42.fr/oauth/applications/new) to get our `cid` and `secret`.

## Usage

### Run

```sh
make run
```

## Technology

<p align="center">
	<a href="https://wordart.com/f0olwstvuu7y/akatsugit-technology">
		<img src="https://user-images.githubusercontent.com/92152391/158834899-7df3bbfc-6263-422b-bc87-7586b6640316.png" width="400" align="center"><br>
		<span>See interactive cloud<span>
	</a>
</p>

### Languages

Languages: Python / SQL (with SQLite3) / SH+MAKEFILE.

### Concept
  - Database with [SQLite3](https://docs.python.org/3/library/sqlite3.html).
  - Get data on API REST with [requests][req], [requests-oauthlib][reqoauth], [requests-cache][reqc] module.
  - Makefile to init [virtual environments](https://docs.python.org/3/library/venv.html), install python requirements.txt, and run the application.

[req]: https://pypi.org/project/requests/
[reqoauth]: https://pypi.org/project/requests-oauthlib/
[reqc]: https://pypi.org/project/requests-cache/
