import os
import zipfile
import gzip
import time
import shutil


import os
import zipfile
import gzip
import shutil

def extract_and_recompress(zip_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)  
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.lower().endswith('.dta'):
                print(f"Skipping {file}, as it is a .dta file.")
                continue
            
            print(file)
            extracted_path = zip_ref.extract(file, output_dir)

            if os.path.dirname(extracted_path) != output_dir:
                new_path = os.path.join(output_dir, os.path.basename(extracted_path))
                shutil.move(extracted_path, new_path)
                extracted_path = new_path
            
            if extracted_path.lower().endswith('.csv'):
                gzip_path = extracted_path + ".gz"
                
                # Check if the .gz file already exists
                if os.path.exists(gzip_path):
                    print(f"Skipping {gzip_path}, already exists.")
                    try:
                        os.remove(extracted_path)  # Try removing the CSV file
                    except PermissionError:
                        print(f"Warning: Unable to delete {extracted_path}, retrying...")
                        time.sleep(1)  # Wait 1 second and retry
                        os.remove(extracted_path)
                    continue
                
                # Compress the file
                with open(extracted_path, 'rb') as f_in:
                    with gzip.open(gzip_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # Ensure the file is closed before attempting to delete
                time.sleep(0.5)  # Small delay to release file lock
                try:
                    os.remove(extracted_path)
                except PermissionError:
                    print(f"Warning: Unable to delete {extracted_path}, retrying...")
                    time.sleep(1)  # Wait and retry deletion
                    os.remove(extracted_path)


zip_path = "subs_eu.zip" 
output_dir = "subs_eu_compressi" 

# processed_countries = {"AT", "BE", "BG", "CY"} 
extract_and_recompress(zip_path, output_dir)
print("Processing complete!")

