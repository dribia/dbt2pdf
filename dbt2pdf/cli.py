"""Dbt2Pdf Command Line Interface."""

import json
from pathlib import Path
from typing import Annotated, Optional

from rich.console import Console
from typer import Argument, Option, Typer

from dbt2pdf import __version__, utils
from dbt2pdf.manifest import parse_manifest
from dbt2pdf.pdf import PDF

app = Typer()

TITLE = "DBT Documentation"

console = Console(tab_size=4)


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main_callback(version: bool = Option(False, help="Show the package version.")):
    """Dbt2Pdf command line interface."""
    if version:
        console.print(f"dbt2pdf, version {__version__}")


@app.command()
def generate(
    destination: Path = Argument(help="Path to save the generated PDF file."),
    manifest_path: Path = Option(
        ..., help="Path to the DBT manifest file.", exists=True, dir_okay=False
    ),
    title: Annotated[str, Option("--title", help="Title of the document.")] = TITLE,
    authors: Annotated[
        Optional[list[str]],
        Option("--add-author", help="Add an author to the document."),
    ] = None,
    macro_packages: Annotated[
        Optional[list[str]],
        Option(
            "--add-macros-package",
            help="Add macros from the given package to the generated document.",
        ),
    ] = None,
):
    """Generate the PDF documentation of a DBT project."""
    with open(manifest_path, encoding="utf-8") as file:
        manifest = parse_manifest(json.load(file))
    # Extract relevant information (models and macros)
    extracted_data = []
    if macro_packages is None:
        macro_packages = []
    if authors is None:
        authors = []
    for node_info in manifest.nodes.values():
        if node_info.resource_type == "model":
            model_info = {
                "name": utils.clean_text(node_info.name),
                "description": utils.clean_text(node_info.description),
                "columns": node_info.columns,
            }
            column_descriptions_ = []
            for col_name, col_info in model_info["columns"].items():
                column_descriptions_.append(
                    {
                        "name": utils.clean_text(col_name),
                        "description": utils.clean_text(col_info.description),
                    }
                )
            model_info["column_descriptions"] = column_descriptions_
            extracted_data.append(model_info)

    # Format the data for macros (keep only the ones of the current project)
    # Format the data for macros (keep only the ones of the current project)
    macro_data = []
    for macro_name, macro_info in manifest.macros.items():
        if macro_info.package_name in macro_packages:
            macro_info_dict = {
                "name": utils.clean_text(macro_name),
                "description": utils.clean_text(macro_info.description),
                "arguments": macro_info.arguments,
            }
            arguments = macro_info_dict["arguments"]
            argument_descriptions_ = []
            for arg in arguments:
                arg_name = utils.clean_text(arg.name)
                arg_description = utils.clean_text(arg.description)
                argument_descriptions_.append(
                    {"name": arg_name, "description": arg_description}
                )
            macro_info_dict["argument_descriptions"] = argument_descriptions_
            macro_data.append(macro_info_dict)

    intro_text_ = (
        "This document provides an overview of the DBT models and macros used in the "
        "project. It includes detailed descriptions of each model and macro, including "
        "the columns or arguments associated with them. The models section lists the "
        "models with their descriptions and column details. The macros section "
        "includes information about macros, their descriptions, and arguments."
    )

    # Create a temporary PDF to count the number of pages
    temp_pdf = PDF(title=title, authors=authors)
    temp_pdf.set_top_margin(10)
    temp_pdf.set_left_margin(15)
    temp_pdf.set_right_margin(15)
    temp_pdf.page_title()
    temp_pdf.add_intro(intro_text_)

    if extracted_data:
        temp_pdf.add_page_with_title("Models")
        for model in extracted_data:
            temp_pdf.subchapter_title(model["name"])
            temp_pdf.chapter_body(
                body=model["description"],
                column_descriptions=model["column_descriptions"],
            )

    if macro_data:
        temp_pdf.add_page_with_title("Macros")
        for macro in macro_data:
            temp_pdf.subchapter_title(macro["name"])
            temp_pdf.chapter_body(
                body=macro["description"],
                argument_descriptions=macro["argument_descriptions"],
            )

    # Create the final PDF with the correct total page count
    final_pdf = PDF(title=title, authors=authors)
    final_pdf.total_pages = temp_pdf.page_no()  # Set the total page count
    final_pdf.set_top_margin(10)
    final_pdf.set_left_margin(15)
    final_pdf.set_right_margin(15)
    final_pdf.page_title()
    final_pdf.add_intro(intro_text_)

    if extracted_data:
        final_pdf.add_page_with_title("Models")
        for model in extracted_data:
            final_pdf.subchapter_title(model["name"])
            final_pdf.chapter_body(
                body=model["description"],
                column_descriptions=model["column_descriptions"],
            )

    if macro_data:
        final_pdf.add_page_with_title("Macros")
        for macro in macro_data:
            final_pdf.subchapter_title(macro["name"])
            final_pdf.chapter_body(
                body=macro["description"],
                argument_descriptions=macro["argument_descriptions"],
            )

    # Save the final PDF
    final_pdf.output(str(destination))
    console.print(f"Documentation created at {destination} :tada:", style="bold green")


if __name__ == "__main__":
    app()
