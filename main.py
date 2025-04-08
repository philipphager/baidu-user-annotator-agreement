from pathlib import Path
from typing import Annotated

import pandas as pd
import typer
from tqdm import tqdm
from typer import Option, Argument

import src.data as data

app = typer.Typer()


@app.command()
def parse_annotations(
    in_directory: Annotated[Path, Option(exists=True, dir_okay=True)] = "data/",
    out_directory: Path = "output/",
    in_file: Path = "annotation_data_0522.txt",
    out_file: Path = "annotations.parquet",
):
    in_path = in_directory / in_file
    out_path = out_directory / out_file

    assert in_path.exists(), f"Expert annotations not found: {in_path}"
    out_directory.mkdir(parents=True, exist_ok=True)

    print(f"Parsing: {in_path}")

    df = data.parse_annotations(in_path)
    df.to_parquet(out_path)

    print(f"Saved: {out_path}")


@app.command()
def filter_clicks(
    part: Annotated[int, Argument(min=0, max=1_999)],
    annotations_file: str = "annotations.parquet",
    in_directory: Annotated[Path, Option(exists=True, dir_okay=True)] = "data/",
    out_directory: Annotated[Path, Option(exists=True, dir_okay=True)] = "output/",
):
    part = part + 1000

    in_path = in_directory / f"part-{part:05d}.gz"
    out_path = out_directory / f"part-{part:05d}.parquet"
    annotations_path = out_directory / annotations_file

    assert in_path.exists(), f"Dataset partition not found: {in_path}"
    assert annotations_path.exists(), f"Annotations not found: {annotations_path}"

    # Parse only clicks for queries that are part of the expert-annotated dataset:
    annotation_df = pd.read_parquet(annotations_path)
    filter_queries = set(annotation_df["query"])

    print(f"Filter clicks: {in_path}")

    click_df = data.parse_clicks(in_path, filter_queries=filter_queries)
    click_df.to_parquet(out_path)

    print(f"Saved: {out_path}")


@app.command()
def concat_clicks(
    in_directory: Path = Path("output/"),
    out_directory: Path = Path("output/"),
    out_file: str = "clicks.parquet",
    remove_parsed_parts: bool = True,
):
    out_path = out_directory / out_file
    dfs = []

    for part_path in tqdm(in_directory.glob("part-*.parquet"), "Concatenate part"):
        df = pd.read_parquet(part_path)
        dfs.append(df)

    assert len(dfs) > 0, "No click partitions found to concatenate"
    click_df = pd.concat(dfs)
    click_df.to_parquet(out_path)

    print(f"Saved: {out_path}")

    if remove_parsed_parts:
        for part_path in tqdm(in_directory.glob("part-*.parquet"), desc="Remove part"):
            part_path.unlink()


if __name__ == "__main__":
    app()
