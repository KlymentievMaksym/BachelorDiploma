import os
import zipfile
import requests
from pathlib import Path
from tqdm import tqdm
from datasets import load_dataset

class DatasetManager:
    def __init__(self, data_dir="data"):
        self.root = Path(__file__).parent.resolve()
        self.data_dir = self.root
        
    def download_file(self, url: str, filename: str):
        filepath = self.data_dir / filename
        
        if filepath.exists():
            print(f"[Download Done] {filename}")
            return filepath

        print(f"[Download] {filename}...")
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(filepath, "wb") as f, tqdm(
            total=total_size, unit='B', unit_scale=True, desc=filename
        ) as pbar:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                pbar.update(len(data))
        
        return filepath

    def unzip_file(self, filepath: Path):
        extract_to = self.data_dir / filepath.stem
        if extract_to.exists():
            print(f"[Unpack Done] {filepath.stem}")
            return

        print(f"[Unpack] {filepath.name}...")
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(self.data_dir)

if __name__ == "__main__":
    manager = DatasetManager()
    
    test_url = "https://github.com/jbrownlee/Datasets/releases/download/v1.0/flower_photos.zip"
    
    zip_path = manager.download_file(test_url, "flowers.zip")
    manager.unzip_file(zip_path)