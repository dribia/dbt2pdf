The `dbt2pdf` package provides a command-line interface (CLI) to convert dbt models to PDF files.

To view the available commands and full usage documentation, run:
```commandline
dbt2pdf --help
```

To view a given command usage documentation, the help flag can be used:
```commandline
dbt2pdf <command> --help
```

The only command available is `generate`, which converts dbt models to PDF files.

## Generate PDF files

To generate PDF files from dbt models, you can use the `generate` command:
```commandline
dbt2pdf generate
```

!!! Warning
    There is a required argument which is the destination path to save the PDF files:

    ```commandline
    dbt2pdf generate path/to/save/output.pdf
    ```

There are many options available to customize the PDF files generated. The following sections describe the available options.

### Define the dbt manifest file path
!!! Warning
    This is a required option. If not provided, the command will fail.

To define the dbt manifest file path, you can use the `manifest-path` option:
```commandline
dbt2pdf generate --manifest-path "path/to/manifest.json"
```

### Set title for the PDF
To set the title for the PDF, you can use the `title` option:
```commandline
dbt2pdf generate --title "My Title for dbt Documentation"
```

!!! Note
    The default title is "DBT Documentation".

### Add authors

To add authors to the documentation, you can use the `add-author` option:
```commandline
dbt2pdf generate --add-author "Jane Doe <jane@example.com>"
```

You can add multiple authors by using the `add-author` option multiple times:
```commandline
dbt2pdf generate \
 --add-author "Jane Doe <jane@example.com>"
 --add-author "John Doe <john@example.com>"
```

### Include macros in the documentation

To include macros in the documentation, you can use the `add-macros-package` option:
```commandline
dbt2pdf generate --add-macros-package "my_macros"
```

### Include logos
It is possible to include up to two logos in the documentation. To include a logo, you can use the `add-logo` option:
```commandline
dbt2pdf generate --add-logo "path/to/logo.png"
```

To include a second logo, you can use the `add-logo` option multiple times:
```commandline
dbt2pdf generate \
 --add-logo "path/to/logo1.png"
 --add-logo "path/to/logo2.png"
```

!!! Warning
    There is a maximum of two logos that can be included.
    The first one in the command line will be bigger and displayed on top of
    the title page, whereas the second one will be smaller and displayed under
    the title on the title page.
