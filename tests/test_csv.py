import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import csv
import pytest
from fetchers.csv_reader import (
    extract_column_names,
    heuristic_fallback,
    extract_csv_data_as_nested_json,
    extract_csv_data_as_flat_json,
    get_csv_column_names,
)


csv_file_path = r"E:\ETL\multi-source-ingestion\Articles.csv"

def test_extract_column_names():
    columns = extract_column_names(csv_file_path)
    assert isinstance(columns, list)
    assert len(columns) > 0

def test_heuristic_fallback():
    columns = extract_column_names(csv_file_path)
    title, content = heuristic_fallback(columns)
    # Either None or a valid column name
    assert title is None or title in columns
    assert content is None or content in columns

def test_get_csv_column_names():
    result = get_csv_column_names(csv_file_path)
    assert "title_column" in result
    assert "content_column" in result
    # Columns must exist or be None
    columns = extract_column_names(csv_file_path)
    if result["title_column"]:
        assert result["title_column"] in columns
    if result["content_column"]:
        assert result["content_column"] in columns

def test_extract_csv_data_as_nested_json():
    columns = get_csv_column_names(csv_file_path)
    title_col = columns.get("title_column")
    content_col = columns.get("content_column")
    if title_col and content_col:
        data = extract_csv_data_as_nested_json(csv_file_path, title_col, content_col)
        assert isinstance(data, list)
        if data:
            assert "title" in data[0]
            assert "content" in data[0]

def test_extract_csv_data_as_flat_json():
    data = extract_csv_data_as_flat_json(csv_file_path)
    assert isinstance(data, list)
    if data:
        assert "title" in data[0]
        assert "content" in data[0]