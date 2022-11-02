import click


from rna_type.cli import (
    preparation,
    preprocessing,
    labelling,
)


@click.group()
def cli():
    pass


cli.add_command(preparation.cli)
cli.add_command(preprocessing.cli)
cli.add_command(labelling.cli)
