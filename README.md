<h1 align="center">Welcome to bugtracker 🪳</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://mit-license.org/" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/nicodalfonso" target="_blank">
    <img alt="Twitter: nicodalfonso" src="https://img.shields.io/twitter/follow/nicodalfonso.svg?style=social" />
  </a>
</p>
<p align="center">
  <img alt="Preview of bugtracker" src="./preview.gif" />
</p>

> A website to track development progress on bug reports and feature request tickets.
>
> File tickets, assign users, edit existing tickets, add details, and update ticket status. View the status of every ticket direcly from the homepage.
>
> Site is limited to authenticated users, only. Each user has an overview page where their contact info and assigned tickets are displayed.

## Prerequisites
- [`Python 3`](https://www.python.org/downloads/)
- [`Poetry`](https://python-poetry.org/)

## Install

After dowloading the repo, do the following:

```sh
poetry install
poetry shell
python manage.py migrate
```

## Usage

On first use, create a new `superuser`:

```sh
poetry shell
python manage.py createsuperuser
```

To start a local server:

```sh
python manage.py runserver
```

To view the website in your browser, navigate to `localhost:8000`.

Login with the username and password created for your superuser

## Author

👤 **Nico D Alfonso**

* Website: https://nicodalfonso.com
* Twitter: [@nicodalfonso](https://twitter.com/nicodalfonso)
* Github: [@nicodalfonso](https://github.com/nicodalfonso)
* LinkedIn: [@nicodalfonso](https://linkedin.com/in/nicodalfonso)

# Acknowledgements

_This project was initially created as a part of the Software Engineering Certification program from [Kenzie Academy](https://kenzie.academy)_

## 📝 License

Copyright © 2022 [Nico D Alfonso](https://github.com/nicodalfonso).<br />
This project is [MIT](https://mit-license.org/) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_