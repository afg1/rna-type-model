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
    data = pl.read_parquet(ungrouped_parquet).groupby(column).agg_list()

    print("grouping done, writing to output parquet...")
    data.write_parquet(output_parquet)

    print("Done!")



if __name__ == "__main__":
    group_by()

