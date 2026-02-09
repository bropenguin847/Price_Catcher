# Price Catcher

<img alt="OpenDOSM" src="https://sesricdiag.blob.core.windows.net/content-api-site-blob/Images/events/2719/2719-b.jpg" style="width: 20%; border-radius: 15px;">

Price Catcher is a Python-Flask based game that let's user guess grocery prices across Malaysia. There are two modes: "Delta" and "The Price is Right".

Data is based on OpenDOSM's Price Catcher catalogue.

Deployed on Render as webservices.

## Contents

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [References](#references)

## Dependencies

- `Flask`
- `pandas`
- `pyarrow`
- `fastparquet`

## Installation

Install all libraries needed through pip

> [!NOTE]  
> Create a virtual environment to run this project. Then activate it with git bash.

```bash
$ git clone https://github.com/bropenguin847/Price_Catcher.git
$ cd price-catcher
$ pip install -r /path/to/requirements.txt
```

## Usage

Launch app.py from terminal.
Visit your localhost:(port) to launch the page.

### File Structure

```shell
.
└── PRICE_CATCHER/
    ├── .venv
    ├── .gitignore
    ├── requirements.txt
    ├── static/
    │   └── styles/
    │       └── style.css
    ├── templates/
    │   ├── index.html
    │   └── pricecatcher.html
    ├── app.py
    └── game.py
```

### References

- [OpenDOSM Price Catcher](https://open.dosm.gov.my/data-catalogue/pricecatcher)
- [Lookup Premise](https://data.gov.my/data-catalogue/lookup_premise)
- [Lookup Item](https://data.gov.my/data-catalogue/lookup_item)
- [README template](https://github.com/alichtman/shallow-backup/blob/main/README.md)
- [File Tree Maker](https://tree.nathanfriend.com/)
- [Render Flask Deployoment](https://render.com/docs/deploy-flask)
- [Flask sessions](https://testdriven.io/blog/flask-sessions/)
- [w3 schools CSS Demo](https://www.w3schools.com/cssref/playdemo.php?filename=playcss_align-items)

### License

<img alt="MIT License" src="https://upload.wikimedia.org/wikipedia/commons/c/c3/License_icon-mit.svg" style="width: 15%;">

[MIT LICENSE](LICENSE)
