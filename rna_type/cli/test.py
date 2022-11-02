import click

from rna_type.heuristic.test_heuristic_model import test_model


@click.group("test")
def cli():
    """
    Commands for testing models
    """


@cli.command("trusted")
@click.argument("model_file")
@click.argument("test_data")
def test_model(model_file, test_data):
    """
    Generic tester for a model.

    This will give you a bunch of metrics like accuracy, f1-score and whatever else I think is useful
    """
    test_model(model_file, test_data)
