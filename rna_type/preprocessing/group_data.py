#!/usr/bin/env python

import polars as pl
import click


@click.command()
@click.argument("ungrouped_parquet")
@click.argument("column")
@click.argument("output_parquet")
def group_by(ungrouped_parquet, column, output_parquet):
    """
    Read a parquet version of the database dump and group it by the specified column

    I would have liked to do this with
    """
    print(f"Reading and grouping by {column}... ")
    data = pl.read_parquet(ungrouped_parquet)
    print(data)
    trusted_ids = [4, 8, 16, 18, 20, 24, 37]
    data = data.with_column(pl.col("dbid").is_in(trusted_ids).alias("trusted"))
    data = (
        data.groupby(column)
        .agg(
            [
                pl.col("*").list(),
                pl.col("trusted").any().alias("contains_trusted"),
            ]
        )
        .drop("trusted")
    )
    print(data)

    print("grouping done, writing to output parquet...")
    data.write_parquet(output_parquet)

    print("Done!")


if __name__ == "__main__":
    group_by()
