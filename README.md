# Baidu-ULTR User Annotator Disagreement

This repository contains a parser for the [Baidu-ULTR dataset](https://arxiv.org/abs/2207.03051) to filter all click sessions with a query that is occuring inside the expert-annotated test set. This repository contains just the parser code, you can download the output files of the parser [here](https://huggingface.co/datasets/philipphager/baidu-ultr-user-annotator-agreement/).

Once downloaded, you can load the files as parquet files in pandas. But be aware that the files are heavily compressed, so loading them into RAM might be challenging. It's advisable to only load the columns you need. The available columns for each dataset are:

| Expert-Annotated Data (Baidu-ULTR Test Set) | User Clicks (Baidu-ULTR Train Set) |
|---------------------------------------------|------------------------------------|
| `query_no`                                  | `query_no`                         |
| `query_id`                                  | `query_id`                         |
| `query`                                     | `query`                            |
| `title`                                     | `title`                            |
| `abstract`                                  | `abstract`                         |
| `label`                                     | —                                  |
| `frequency_bucket`                          | —                                  |
| —                                           | `url_md5`                          |
| —                                           | `position`                         |
| —                                           | `media_type`                       |
| —                                           | `displayed_time`                   |
| —                                           | `serp_height`                      |
| —                                           | `slipoff_count_after_click`        |
| —                                           | `click`                            |

```
!pip install pandas pyarrow

import pandas as pd


click_df = pd.read_parquet("clicks.parquet", columns=["query", "url_md5", "click"])
annotation_df = pd.read_parquet("annotations.parquet")
```
