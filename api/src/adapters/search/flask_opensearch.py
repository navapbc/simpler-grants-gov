from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TypeVar

from flask import Flask, current_app

from src.adapters.search import SearchClient

_SEARCH_CLIENT_KEY = "search-client"


def register_search_client(search_client: SearchClient, app: Flask) -> None:
    app.extensions[_SEARCH_CLIENT_KEY] = search_client


def get_search_client(app: Flask) -> SearchClient:
    return app.extensions[_SEARCH_CLIENT_KEY]


P = ParamSpec("P")
T = TypeVar("T")


def with_search_client() -> Callable[[Callable[Concatenate[SearchClient, P], T]], Callable[P, T]]:
    # TODO docs

    def decorator(f: Callable[Concatenate[SearchClient, P], T]) -> Callable[P, T]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return f(get_search_client(current_app), *args, **kwargs)

        return wrapper

    return decorator
