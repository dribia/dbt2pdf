# Contribute

<p style="text-align: center; padding-bottom: 1rem;">
    <a href="https://dribia.github.io/dbt2pdf">
        <img
            src="../img/logo_dribia_blau_cropped.png"
            alt="dbt2PDF"
            style="display: block; margin-left: auto; margin-right: auto; width: 40%;"
        >
    </a>
</p>

<p style="text-align: center;">
    <em>Contributions to Dribia libraries are always welcome!</em>
</p>

## Mantainers
dbt2PDF is maintained by:

* Dribia Code - <code@dribia.com>

## Issues
Questions, feature requests and bug reports are all welcome as [discussions or issues](https://github.com/dribia/dbt2pdf/issues).

Please note which version of the library are you using whenever reporting a bug.
```shell
python -c "import dbt2pdf; print(dbt2pdf.__version__)"
```

It would be very useful too to know which OS and Python version are your running dbt2PDF from.

## Contribute
In order to contribute, the first step is to clone yourself the code:
[repository](https://github.com/dribia/dbt2pdf):
```shell
git clone https://github.com/dribia/dbt2pdf.git
```
Then, you can step into the project's root and, assuming that you have both [Poetry](https://python-poetry.org/) and
[pre-commit](https://pre-commit.com/) installed, run:
```shell
poetry install && pre-commit install
```

Now you should be ready to start coding and prepare your [pull request](https://github.com/dribia/dbt2pdf/pulls).

Remember that you can run linting and tests locally with:

```shell
sh scripts/lint.sh
sh scripts/test.sh
```

Happy coding!
