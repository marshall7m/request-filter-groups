from validator import Validator
from jsonpath_ng import parse
import logging
from flask import request, abort
from functools import wraps

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class ValidationError(Exception):
    """Wraps around request validation errors"""


class RequestFilter(object):
    def __init__(self):
        pass

    def validate(self, data, filter_groups):
        """ """
        for group in filter_groups:
            log.debug(f"Filter group:\n{group}")
            results = {}
            for path, rule in group.items():
                try:
                    results[path] = [match.value for match in parse(path).find(data)][0]
                except IndexError:
                    request[path] = ""
            log.debug(f"Request mapping:\n{results}")

            val = Validator(results, group)
            is_valid = val.validate()

            log.debug(f"Validated data:\n{val.get_validated_data()}")
            errors = val.get_errors()
            log.debug(f"Validation errors: {errors}")

            if is_valid:
                return True

        raise ValidationError(errors)

    def request_filter_groups(self, filter_groups, flask=False):
        """ """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if flask:
                    data = request.json
                else:
                    data = args[0]
                try:
                    self.validate(data, filter_groups)
                except ValidationError as e:
                    log.error(e, exc_info=True)
                    if flask:
                        abort(422, e)
                    else:
                        return {"statusCode": 422, "body": e}

                return func(*args, **kwargs)

            return wrapper

        return decorator
