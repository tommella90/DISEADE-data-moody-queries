from pathlib import Path
import shutil


class FileZipper:
    def __init__(self, output_path):
        self.base_path = Path("z:\\dati_moody\\zipped_files")  
        self.output_path = Path(output_path)  

    def zip_folder(self, file_name):

        zip_destination = self.base_path / file_name  
        shutil.make_archive(str(zip_destination), 'zip', root_dir=self.output_path)

        print(f"Archive created at {zip_destination}.zip")


