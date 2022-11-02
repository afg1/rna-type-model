import polars as pl
import click
import numpy as np


def split_into(input_name, output_dir, chunks):
    """
    Split the now huge dataset into a number of chunks to process in parallel
    """

    all_data = pl.read_parquet(input_name)

    num_entries = all_data.height

    chunk_size = int(np.ceil(num_entries / chunks))
    print(chunk_size, num_entries)

    for chunk_no in range(0, chunks):
        offset = chunk_no * chunk_size
        output_path = f"{output_dir}/chunk_{chunk_no}.parquet"
        df_slice = all_data.slice(offset, chunk_size).clone()
        df_slice.write_parquet(f"{output_path}")


if __name__ == "__main__":
    split_into()
