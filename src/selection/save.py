from pathlib import Path

def save_parquet(df, processed_path, processed_filename):
    """Write to data/processed/ as Parquet"""
    folder = Path(processed_path)
    folder.mkdir(exist_ok=True, parents=True)
    file = folder / processed_filename
    df.to_parquet(file, index=False)
    return file

