"""Module to define a DBT manifest file representation."""

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)
    from dbt_artifacts_parser.parser import parse_manifest

__all__ = ["parse_manifest"]
