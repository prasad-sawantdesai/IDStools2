import logging
from urllib.parse import urlsplit, urlunsplit

logger = logging.getLogger(f"module.{__name__}")


def add_query_to_uri(uri: str, *, backend: str, query: str):
    """Append a query pair when the URI uses the selected backend."""
    uri_parts = urlsplit(uri)
    uri_backend = uri_parts.path.rsplit("/", 1)[-1]
    if uri_backend != backend:
        return uri

    updated_query = f"{uri_parts.query};{query}"
    return urlunsplit(uri_parts._replace(query=updated_query))


def add_default_uda_cache_mode(uri: str):
    """Append ``cache_mode=none`` to UDA URIs."""
    return add_query_to_uri(uri, backend="uda", query="cache_mode=none")


def get_slice_from_array(arr, slice_str):
    if ":" not in slice_str:
        index = int(slice_str)
        try:
            return [arr[index]]
        except IndexError:
            logger.error(f"Index {index} out of bounds for array of size {len(arr)}")
            return None

    parts = slice_str.split(":")

    start = int(parts[0]) if parts[0] else None
    stop = int(parts[1]) if len(parts) > 1 and parts[1] else None
    step = int(parts[2]) if len(parts) > 2 and parts[2] else None

    slice_obj = slice(start, stop, step)

    return arr[slice_obj]
