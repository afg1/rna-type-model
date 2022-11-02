import polars as pl
import numpy as np
import gzip as gz


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


def combine_from(output_file, input_files):
    """
    Combine many numpy labels into one

    Sort the filenames first to ensure correct ordering!
    """
    input_files_sorted = sorted(input_files)
    fh = gz.GzipFile(input_files_sorted[0], "r")
    all_labels = np.load(fh)
    for input_file in input_files_sorted[1:]:
        fh = gz.GzipFile(input_file, "r")
        all_labels = np.vstack((all_labels, np.load(fh)))

    ofh = gz.GzipFile(output_file, "w")
    np.save(ofh, all_labels)
