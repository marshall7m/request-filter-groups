import pytest
from contextlib import nullcontext as does_not_raise
from request_filter_groups.filter_groups import RequestFilter, ValidationError
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


r = RequestFilter()
params = [
    {
        "data": {"A": {"B": "foo"}, "C": [1, 2, 3]},
        "filter_groups": [{"A.B": "regex:foo", "C": "required|min:3"}],
        "error": does_not_raise(),
        "status_code": 200,
    },
    {
        "data": {"A": {"B": "foo"}, "C": [1, 2, 3]},
        "filter_groups": [{"A.B": "regex:foo", "C": "required|min:10"}],
        "error": pytest.raises(ValidationError),
        "status_code": 422,
    },
]


@pytest.mark.parametrize(
    "data,filter_groups,expected",
    [(p["data"], p["filter_groups"], p["error"]) for p in params],
)
def test_validate(data, filter_groups, expected):
    """
    Assert function raises the validation exception if not validated and no
    exception if validated
    """
    with expected:
        r.validate(data, filter_groups)


@pytest.mark.parametrize(
    "data,filter_groups,expected",
    [(p["data"], p["filter_groups"], p["status_code"]) for p in params],
)
def test_decorator(data, filter_groups, expected):
    """
    Assert decorator returns the dummy function's return status code if validated
    or the validation error status code if not validated
    """
    @r.request_filter_groups(filter_groups)
    def func(data):
        return {"statusCode": 200}

    response = func(data)
    log.debug(f"Response:\n{response}")

    assert response["statusCode"] == expected
