import duckdb
import gzip
import os


OUTPUT_DIR = "..\\..\\..\\zipped_files\\all_data_gz"


def convert_parquet_to_csv_gz(create_query, folder_name, input_path, country):

    output_csv_gz = os.path.join(OUTPUT_DIR, folder_name, f"{country}.csv.gz")
    output_dir = os.path.dirname(output_csv_gz)
    os.makedirs(output_dir, exist_ok=True)

    conn = duckdb.connect()
    final_query = f"""
        COPY 
            ({create_query(input_path, country)})
        TO 
            '{output_csv_gz}' 
        WITH 
            (FORMAT 'csv', COMPRESSION 'gzip');
    """
    conn.execute(final_query)
    conn.close()
    print(f"✅ Converted to {output_csv_gz}")
    return output_csv_gz


def split_gz_file(input_gz, max_size_mb=50):

    output_dir = os.path.dirname(input_gz)
    os.makedirs(output_dir, exist_ok=True)
    max_size_bytes = max_size_mb * 1024 * 1024

    base_name = os.path.basename(input_gz).replace(".csv.gz", "")

    with gzip.open(input_gz, "rt", encoding="utf-8") as f_in:
        header = f_in.readline()
        chunk_idx = 0
        current_size = 0
        chunk_file = None
        print(chunk_idx, current_size)

        for line in f_in:
            if chunk_file is None or current_size >= max_size_bytes:
                if chunk_file:
                    chunk_file.close()

                chunk_path = os.path.join(output_dir, f"{base_name}_chunk_{chunk_idx}.csv.gz")
                chunk_file = gzip.open(chunk_path, "wt", encoding="utf-8")
                chunk_file.write(header)
                current_size = len(header.encode("utf-8"))
                print(f"📁 Created new chunk: {os.path.abspath(chunk_path)}")
                chunk_idx += 1

            chunk_file.write(line)
            current_size += len(line.encode("utf-8"))

        if chunk_file:
            chunk_file.close()

    os.remove(input_gz)
    print(f"✅ Split complete! Files saved in: {os.path.abspath(output_dir)}")
    print(f"🗑️ Deleted original file: {input_gz}")
