import gzip
from pathlib import Path
from typing import Set

import pandas as pd
from tqdm import tqdm

from src.const import ClickColumns, QueryColumns
from src.utils import parse_tokens


def parse_annotations(path: Path):
    rows = []
    query_no = -1
    current_query = None

    with open(path, "rb") as f:
        for line in tqdm(f):
            columns = line.strip(b"\n").split(b"\t")
            query_id, query, title, abstract, label, frequency_bucket = columns

            if query != current_query:
                # As query_ids in the val set are not unique,
                # we differentiate queries based on text:
                current_query = query
                query_no += 1

            query = parse_tokens(query)
            title = parse_tokens(title)
            abstract = parse_tokens(abstract)

            rows.append(
                {
                    "query_no": query_no,
                    "query_id": int(query_id.decode()),
                    "query": query,
                    "title": title,
                    "abstract": abstract,
                    "label": int(label.decode()),
                    "frequency_bucket": int(frequency_bucket.decode()),
                }
            )

    return pd.DataFrame(rows)


def parse_clicks(path: Path, filter_queries: Set[bytes] = None):
    rows = []
    query_id = None
    query = None
    filter_queries = filter_queries if filter_queries is not None else set()

    with gzip.open(path, "rb") as f:
        query_no = -1

        for line in tqdm(f):
            columns = line.strip(b"\n").split(b"\t")
            is_query = len(columns) <= 3

            if is_query:
                query_no += 1
                query_id = columns[QueryColumns.QID]
                query = parse_tokens(columns[QueryColumns.QUERY])
            elif len(filter_queries) == 0 or query in filter_queries:
                title = parse_tokens(columns[ClickColumns.TITLE])
                abstract = parse_tokens(columns[ClickColumns.ABSTRACT])
                url = columns[ClickColumns.URL_MD5]
                position = int(columns[ClickColumns.POS])
                media_type = columns[ClickColumns.MULTIMEDIA_TYPE]
                media_type = int(media_type) if media_type != b"-" else 0
                displayed_time = float(columns[ClickColumns.DISPLAYED_TIME])
                serp_height = int(columns[ClickColumns.SERP_HEIGHT])
                slipoff = int(columns[ClickColumns.SLIPOFF_COUNT_AFTER_CLICK])
                click = int(columns[ClickColumns.CLICK])

                rows.append(
                    {
                        "query_no": query_no,
                        "query_id": query_id.decode("utf-8"),
                        "url_md5": url.decode("utf-8"),
                        "query": query,
                        "title": title,
                        "abstract": abstract,
                        "position": position,
                        "media_type": media_type,
                        "displayed_time": displayed_time,
                        "serp_height": serp_height,
                        "slipoff_count_after_click": slipoff,
                        "click": click,
                    }
                )

        return pd.DataFrame(rows)
