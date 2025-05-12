from collections.abc import Callable, Mapping
from importlib.abc import Traversable


def preprocess_files[T](
    traversable: Traversable, preprocessor: Callable[[str], T]
) -> Mapping[str, T]:
    return {
        traversable.name: preprocessor(traversable.open().read())
        for traversable in traversable.iterdir()
    }
