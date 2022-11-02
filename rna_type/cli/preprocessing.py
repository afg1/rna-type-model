import click

from rna_type.preprocessing.group_data import group_by
from rna_type.preprocessing.load_and_split_data import load_and_split


@click.group("preprocess")
def cli():
    """
    Commands for preprocessing data
    """


@cli.command()
@click.argument("ungrouped_parquet")
@click.argument("column")
@click.argument("output_parquet")
def group_data(ungrouped_parquet, column, output_parquet):
    group_by(ungrouped_parquet, column, output_parquet)


@cli.command()
@click.argument("grouped_data", type=click.File("r"))
@click.option("--rng_seed", type=int, default=-1)
def split_train_test(grouped_data, rng_seed):
    load_and_split(grouped_data, rng_seed)
