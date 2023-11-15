import logging
import time
from functools import wraps

log = logging.getLogger(__name__)


def retry_on_false(tries=3, delay=5):
    """Retry decorated function until its return result is resolved to True.

    :param tries: count of tries.
    :param delay: delay between tries.
    :return: value returned by decorated function or None if function call raised exception at all tries.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_result = None
            for i in range(1, tries + 1):
                if i > 1:
                    time.sleep(delay)
                try:
                    func_result = func(*args, **kwargs)
                    if func_result:
                        return func_result
                    else:
                        log.warning(f"Result of '{func.__name__}' function was not resolved to True "
                                    f"at attempt {i}: '{func_result}'.")
                except Exception as ex:
                    log.error(f"Error '{type(ex)}' appeared: {ex}.")
            return func_result

        return wrapper

    return decorator


def retry_until_condition(predicate, tries=3, delay=5):
    """Retry decorated function until predicate function, applied to result of wrapped function, returns True.

    :param predicate: predicate function to be applied to return result of wrapped function.
    :param tries: count of tries.
    :param delay: delay between tries.
    :return: value returned by decorated function or None if function call raised exception at all tries.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_result = None
            for i in range(1, tries + 1):
                if i > 1:
                    time.sleep(delay)
                try:
                    func_result = func(*args, **kwargs)
                    if predicate(func_result):
                        return func_result
                    else:
                        log.warning(f"Result of predicate was not resolved to True "
                                    f"at attempt {i}: '{func_result}'.")
                except Exception as ex:
                    log.error(f"Error '{type(ex)}' appeared: {ex}.")
            return func_result

        return wrapper

    return decorator
