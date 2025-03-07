import numpy as np
import gzip
import shutil
import os


def split_in_chunks(df, n_chunks):
    indices = np.array_split(df.index, n_chunks)
    slices = [df.iloc[idx] for idx in indices]
    return slices


def compress_csv_files(folder_to_zip: str, zip_output: str) -> None:
    os.makedirs(zip_output, exist_ok=True)

    for file_name in os.listdir(folder_to_zip):
        if file_name.endswith(".csv"):
            input_csv = os.path.join(folder_to_zip, file_name)
            output_csv_gz = os.path.join(zip_output, file_name + ".gz")  # Add .gz extension

            with open(input_csv, 'rb') as f_in:
                with gzip.open(output_csv_gz, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            print(f"Compressed {input_csv} to {output_csv_gz}")


