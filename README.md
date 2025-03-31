# Baidu-ULTR User Annotator Disagreement

This repository contains a parser for the [Baidu-ULTR dataset](https://arxiv.org/abs/2207.03051) to filter all click sessions with a query that is occuring inside the expert-annotated test set. This repository contains just the parser code, you can download the output files of the parser [here](https://huggingface.co/datasets/philipphager/baidu-ultr-user-annotator-agreement/).

Once downloaded, you can load the files as parquet files in pandas:
```
!pip install pandas pyarrow

import pandas as pd


click_df = pd.read_parquet("clicks.parquet")
annotation_df = pd.read_parquet("annotations.parquet")
```
