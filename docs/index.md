# DriConfig

<p align="center">
    <a href="https://dribia.github.io/dbt2pdf">
        <picture style="display: block; margin-left: auto; margin-right: auto; width: 40%;">
            <source
                media="(prefers-color-scheme: dark)"
                srcset="https://dribia.github.io/dbt2pdf/img/logo_dribia_blanc_cropped.png"
            >
            <source
                media="(prefers-color-scheme: light)"
                srcset="https://dribia.github.io/dbt2pdf/img/logo_dribia_blau_cropped.png"
            >
            <img
                alt="dbt2pdf"
                src="https://dribia.github.io/dbt2pdf/img/logo_dribia_blau_cropped.png"
            >
        </picture>
    </a>
</p>

<p style="text-align: center">
<a href="https://github.com/dribia/dbt2pdf/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/dribia/dbt2pdf/workflows/Test/badge.svg?query=branch%3Amain" alt="Test">
</a>
<a href="https://github.com/dribia/dbt2pdf/actions?query=workflow%3ALint" target="_blank">
    <img src="https://github.com/dribia/dbt2pdf/workflows/Lint/badge.svg?query=branch%3Amain" alt="Lint">
</a>
<a href="https://github.com/dribia/dbt2pdf/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/dribia/dbt2pdf/workflows/Publish/badge.svg?query=branch%3Amain" alt="Publish">
</a>
<a href="https://github.com/dribia/dbt2pdf/actions?query=workflow%3ADocs" target="_blank">
    <img src="https://github.com/dribia/dbt2pdf/workflows/Docs/badge.svg?query=branch%3Amain" alt="Docs">
</a>
<a href="https://codecov.io/gh/dribia/dbt2pdf" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/dribia/dbt2pdf?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/dbt2pdf" target="_blank">
    <img src="https://img.shields.io/pypi/v/dbt2pdf?color=%2334D058&label=pypi%20package" alt="PyPI version">
</a>
<a href="https://pypistats.org/packages/dbt2pdf" target="_blank">
    <img src="https://img.shields.io/pypi/dm/dbt2pdf?color=%2334D058" alt="PyPI downloads">
</a>
</p>

<p style="text-align: center;">
    <em>A CLI to convert dbt models to PDFs.</em>
</p>

---

**Documentation**: <a href="https://dribia.github.io/dbt2pdf" target="_blank">https://dribia.github.io/dbt2pdf</a>

**Source Code**: <a href="https://github.com/dribia/dbt2pdf" target="_blank">https://github.com/dribia/dbt2pdf</a>

---

dbt2pdf provides a command-line interface (CLI) to convert dbt models to PDF files.

## Key features

* **CLI**: An easy to use command-line interface (CLI) that can be used to convert dbt models to PDF files.
* **Customizable**: Allows you to customize certain aspects of the output file.
* **Easy to use**: Easy to use and can be integrated into your dbt workflow.
* **Open source**: Open source and free to use.

## Example

```commandline
dbt2pdf generate \
  --manifest-path ./manifest.json \
  --title "DBT Documentation" \
  --add-author john@example.com \
  --add-author doe@example.com \
  output.pdf
``
