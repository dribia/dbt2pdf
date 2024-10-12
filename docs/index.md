# dbt2pdf

<p style="text-align: center; padding-bottom: 1rem;">
    <a href="/dbt2pdf">
        <img
            src="./img/logo_dribia_blau_cropped.png"
            alt="Dribia"
            style="display: block; margin-left: auto; margin-right: auto; width: 40%;"
        >
    </a>
</p>

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![Tests](https://github.com/dribia/dbt2pdf/actions/workflows/test.yml/badge.svg)](https://github.com/dribia/dbt2pdf/actions/workflows/test.yml) [![Coverage Status](https://img.shields.io/codecov/c/github/dribia/dbt2pdf)](https://codecov.io/gh/dribia/dbt2pdf) [![Tests](https://github.com/dribia/dbt2pdf/actions/workflows/lint.yml/badge.svg)](https://github.com/dribia/dbt2pdf/actions/workflows/lint.yml) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Package | [![PyPI](https://img.shields.io/pypi/v/dbt2pdf)](https://pypi.org/project/dbt2pdf/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/dbt2pdf?color=blue&logo=pypi&logoColor=gold) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbt2pdf?logo=python&logoColor=gold) [![GitHub](https://img.shields.io/github/license/dribia/dbt2pdf?color=blue)](LICENSE)                                                                                                                                                                                                                                                                                                         |

<p style="text-align: center;">
    <em>A CLI utility to automatically generate your DBT project's PDF documentation.</em>
</p>

---

**Documentation**: <a href="https://dribia.github.io/dbt2pdf" target="_blank">https://dribia.github.io/dbt2pdf</a>

**Source Code**: <a href="https://github.com/dribia/dbt2pdf" target="_blank">https://github.com/dribia/dbt2pdf</a>

---

## Key features

* **CLI**: Easy to use CLI to generate a PDF documentation out of your DBT project.
* **Customizable**: Allows you to customize certain aspects of the output file.
* **Easy to use**: Easy to use and can be integrated into your dbt workflow.
* **Open source**: Open source and free to use.

## Installation
**dbt2pdf** is available on PyPI, so you can install it with `pip`:
```shell
pip install dbt2pdf
```

## Example

```commandline
dbt2pdf generate \
  --manifest-path ./manifest.json \
  --title "DBT Documentation" \
  --add-author john@example.com \
  --add-author doe@example.com \
  output.pdf
```
