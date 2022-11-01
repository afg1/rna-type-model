#!/usr/bin/env python
import polars as pl
import click


@click.command()
@click.argument("dump_name")
@click.argument("output_name")
def convert_to_parquet(dump_name, output_name):
    """
    Load a csv dump from the database and rewrite it as parquet.

    Parquet has a couple of benefits:
    - It is way smaller (20GB -> 500MB)
    - It is MUCH faster to load
    - It can handle the grouped data format we need later
    """
    print("Loading CSV dump to convert to parquet...")
    data = pl.read_csv(dump_name)
    data.write_parquet(output_name)
    print("Conversion finished!")


if __name__ == "__main__":
    convert_to_parquet()
