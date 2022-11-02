import click

from rna_type.preparation.convert_data import convert_to_parquet


@click.group("prepare")
def cli():
    """
    Commands for preparing data
    """


@cli.command("convert")
@click.argument("dump_name")
@click.argument("output_name")
def convert(dump_name, output_name):
    """
    Convert a CSV dump from the database into a parquet file for easier handling
    """
    convert_to_parquet(dump_name, output_name)
