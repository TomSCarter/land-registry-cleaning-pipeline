from src.cleaning import config
from src.cleaning.pipeline import CleaningPipeline

if __name__ == "__main__":
    pipeline = CleaningPipeline(config)
    df, report = pipeline.run()
    print(report.to_string())