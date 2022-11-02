import click

from rna_type.heuristic.run_heuristic_labeller import run_heuristic_labeller
from rna_type.heuristic.split_data_for_labelling import split_into, combine_from


@click.group("label")
def cli():
    """
    Commands for labeling data
    """


@cli.command()
@click.argument("input_name")
@click.argument("output_dir", type=click.Path())
@click.option("--chunks", default=100, type=int)
def split(input_name, output_dir, chunks):
    """
    Split a dataframe (grouped) into a given number of chunks

    This makes processing on codon easier
    """
    split_into(input_name, output_dir, chunks)


@cli.command("heuristic")
@click.argument("data")
@click.argument("output")
def heuristic(data, output):
    """
    Run the suite of heuristic label functions on the data
    """
    run_heuristic_labeller(data, output)


@cli.command("label-model")
@click.argument("model_file")
@click.argument("data_to_label")
@click.argument("heuristic_labels")
@click.argument("output_file")
def lm_labeller(model_file, data_to_label, heuristic_labels, output_file):
    """
    This will run the label model over unlabelled data. Requires you to run the heuristic labeller first
    """
    pass


@cli.command("split")
@click.argument("train_data")
@click.argument("output_dir")
@click.option("--chunks", default=100, type=int)
def split(train_data, output_dir, chunks):
    split_into(train_data, output_dir, chunks)


@cli.command("combine")
@click.argument("output_name")
@click.argument("input_files", nargs=-1)
def combine(output_name, input_files):
    combine_from(output_name, input_files)
