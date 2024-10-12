Dbt2PDF
==========================

<p align="center">
    <a href="https://dribia.github.io/driconfig">
        <picture style="display: block; margin-left: auto; margin-right: auto; width: 40%;">
            <source
                media="(prefers-color-scheme: dark)"
                srcset="https://dribia.github.io/driconfig/img/logo_dribia_blanc_cropped.png"
            >
            <source
                media="(prefers-color-scheme: light)"
                srcset="https://dribia.github.io/driconfig/img/logo_dribia_blau_cropped.png"
            >
            <img
                alt="driconfig"
                src="https://dribia.github.io/driconfig/img/logo_dribia_blau_cropped.png"
            >
        </picture>
    </a>
</p>

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![Tests](https://github.com/dribia/dbt2pdf/actions/workflows/test.yml/badge.svg)](https://github.com/dribia/dbt2pdf/actions/workflows/test.yml) [![Coverage Status](https://img.shields.io/codecov/c/github/dribia/dbt2pdf)](https://codecov.io/gh/dribia/dbt2pdf) [![Tests](https://github.com/dribia/dbt2pdf/actions/workflows/lint.yml/badge.svg)](https://github.com/dribia/dbt2pdf/actions/workflows/lint.yml) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Package | [![PyPI](https://img.shields.io/pypi/v/dbt2pdf)](https://pypi.org/project/dbt2pdf/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/dbt2pdf?color=blue&logo=pypi&logoColor=gold) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbt2pdf?logo=python&logoColor=gold) [![GitHub](https://img.shields.io/github/license/dribia/dbt2pdf?color=blue)](LICENSE)                                                                                                                                                                                                                                                                                                         |
---

> [!CAUTION]
> This project is in early development stages and is not yet ready for production use.
> Our priority at the moment is that it works for our use case, so we are not yet focusing on
> covering all possible use cases.

---

**Documentation**: <a href="https://dribia.github.io/dbt2pdf" target="_blank">https://dribia.github.io/dbt2pdf</a>

**Source Code**: <a href="https://github.com/dribia/dbt2pdf" target="_blank">https://github.com/dribia/dbt2pdf</a>

---

## Installation

This project resides in the Python Package Index (PyPI), so it can easily be installed with `pip`:

```console
pip install dbt2pdf
```

## Usage

The `dbt2pdf` package provides a command-line interface (CLI) to convert DBT models to PDF files.

To view the avilable commands and full usage documentation, run:

```shell
dbt2pdf --help
```

To view a given command usage documentation, the help flag can be used:

```shell
dbt2pdf <command> --help
```

### Examples
```shell
dbt2pdf generate \
  --manifest-path ./manifest.json \
  --title "DBT Documentation" \
  --add-author john@example.com \
  --add-author doe@example.com \
  output.pdf
```

## Contributing

[Poetry](https://python-poetry.org) is the best way to interact with this project, to install it,
follow the official [Poetry installation guide](https://python-poetry.org/docs/#installation).

With `poetry` installed, one can install the project dependencies with:

```shell
poetry install
```

Then, to run the project unit tests:

```shell
make test-unit
```

To run the linters (`ruff` and `mypy`):

```shell
make lint
```

To apply all code formatting:

```shell
make format
```

## License

`dbt2pdf` is distributed under the terms of the
[MIT](https://opensource.org/license/mit) license.
Check the [LICENSE](./LICENSE) file for further details.
