#!/usr/bin/env python

import polars as pl
import click

@click.command()
@click.argument("in_name")
@click.argument("out_name")
def load_and_convert(in_name:str, out_name:str):
    df = pl.read_csv(in_name)

    print(f"Converted CSV with {df.height} rows to parquet")

    df.write_parquet(out_name, compression_level=10)




if __name__ == "__main__":
    load_and_convert()