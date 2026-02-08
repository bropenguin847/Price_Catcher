# Price Catcher

Price Catcher is a Python-Flask based game that let's user guess grocery prices across Malaysia.

Data is based on OpenDOSM's Price Catcher catalogue.

# Contents

-[Installation](#installation)
-[Dependencies](#dependencies)
-[Usage](#usage)
-[File Structure](#file-structure)
-[References](#references)

## Installation
Install all libraries needed through pip

> [!NOTE]  
> Create a virtual environment to run this project. Then activate it with git bash.

```bash
$ git clone https://github.com/bropenguin847/Price_Catcher.git
$ cd price-catcher
$ pip install -r /path/to/requirements.txt
```

## Dependencies

---

- `Flask`
- `pandas`

## Usage
Launch app.py from terminal.
Visit your localhost:(port) to launch the page.


### File Structure

```shell
.
└── PRICE_CATCHER/
    ├── .venv
    ├── .gitignore
    ├── README.md
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
[OpenDOSM Price Catcher](https://open.dosm.gov.my/data-catalogue/pricecatcher)
[Lookup Premise](https://data.gov.my/data-catalogue/lookup_premise)
[Lookup Item](https://data.gov.my/data-catalogue/lookup_item)
[README template](https://github.com/alichtman/shallow-backup/blob/main/README.md)
[File Tree Maker](https://tree.nathanfriend.com/)
