import click

from rna_type.heuristic.train_heuristic_label_model import train_heuristic_label_model


@click.group("train")
def cli():
    """
    Commands for training models
    """


@cli.command("heuristic")
@click.argument("train_data")
@click.argument("train_labels")
@click.option("--epochs", default=500, type=int)
def train_heuristic(train_data, train_labels, epochs):
    """
    Train a heuristic model using the accession data and heuristic labbeler output
    """
    train_heuristic_label_model(train_data, train_labels, epochs)
