from typing import Any, Callable, Coroutine, TypeAlias

UserId: TypeAlias = int
Balance: TypeAlias = int
DecoratorWithArgumentsForCoroutine: TypeAlias = Callable[
    [Callable[..., Any]], Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]
]
