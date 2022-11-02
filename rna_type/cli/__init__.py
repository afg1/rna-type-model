import click


from rna_type.cli import (
    preparation,
    preprocessing,
    labelling,
    training,
)


@click.group()
def cli():
    pass


cli.add_command(preparation.cli)
cli.add_command(preprocessing.cli)
cli.add_command(labelling.cli)
cli.add_command(training.cli)
