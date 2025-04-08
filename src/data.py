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


def parse_clicks(path: Path, filter_queries: Set[str] = None):
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
                query_id = columns[QueryColumns.QID].decode("utf-8")
                query = parse_tokens(columns[QueryColumns.QUERY])
                query_reformulation = parse_tokens(columns[QueryColumns.QUERY_REFORMULATION])
            elif len(filter_queries) == 0 or query in filter_queries:
                # Content features:
                title = parse_tokens(columns[ClickColumns.TITLE])
                abstract = parse_tokens(columns[ClickColumns.ABSTRACT])
                url = columns[ClickColumns.URL_MD5].decode("utf-8")

                # Display features:
                position = int(columns[ClickColumns.POS])
                media_type = columns[ClickColumns.MULTIMEDIA_TYPE]
                media_type = int(media_type) if media_type != b"-" else 0
                serp_height = int(columns[ClickColumns.SERP_HEIGHT])
                serp_to_top = int(columns[ClickColumns.SERP_TO_TOP])

                # User feedback:
                click = int(columns[ClickColumns.CLICK])
                first_click = int(columns[ClickColumns.FIRST_CLICK])
                last_click = int(columns[ClickColumns.LAST_CLICK])
                final_click = int(columns[ClickColumns.FINAL_CLICK])

                skip = int(columns[ClickColumns.SKIP])
                slipoff = int(columns[ClickColumns.SLIPOFF_COUNT])
                slipoff_after_click = int(columns[ClickColumns.SLIPOFF_COUNT_AFTER_CLICK])

                displayed_count = int(columns[ClickColumns.DISPLAYED_COUNT])
                displayed_count_top = int(columns[ClickColumns.DISPLAYED_COUNT_TOP])
                displayed_count_middle = int(columns[ClickColumns.DISPLAYED_COUNT_MIDDLE])
                displayed_count_bottom = int(columns[ClickColumns.DISPLAYED_COUNT_BOTTOM])
                reverse_displayed_count = int(columns[ClickColumns.REVERSE_DISPLAY_COUNT])

                displayed_time = float(columns[ClickColumns.DISPLAYED_TIME])
                displayed_time_top = float(columns[ClickColumns.DISPLAYED_TIME_TOP])
                displayed_time_middle = float(columns[ClickColumns.DISPLAYED_TIME_MIDDLE])
                displayed_time_bottom = float(columns[ClickColumns.DISPLAYED_TIME_BOTTOM])
                dwelling_time = float(columns[ClickColumns.DWELLING_TIME])

                rows.append(
                    {
                        "query_no": query_no,
                        "query_id": query_id,
                        "url_md5": url,
                        "query": query,
                        "query_reformulation": query_reformulation,
                        "title": title,
                        "abstract": abstract,
                        "position": position,
                        "media_type": media_type,
                        "serp_height": serp_height,
                        "serp_to_top": serp_to_top,
                        "click": click,
                        "first_click": first_click,
                        "last_click": last_click,
                        "final_click": final_click,
                        "skip": skip,
                        "slipoff": slipoff,
                        "slipoff_after_click": slipoff_after_click,
                        "displayed_count": displayed_count,
                        "displayed_count_top": displayed_count_top,
                        "displayed_count_middle": displayed_count_middle,
                        "displayed_count_bottom": displayed_count_bottom,
                        "reverse_displayed_count": reverse_displayed_count,
                        "displayed_time": displayed_time,
                        "displayed_time_top": displayed_time_top,
                        "displayed_time_middle": displayed_time_middle,
                        "displayed_time_bottom": displayed_time_bottom,
                        "dwelling_time": dwelling_time,
                    }
                )

        return pd.DataFrame(rows)
