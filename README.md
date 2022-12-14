# Request Filter Groups

## Description
A Python wrapper and utility function for validating requests. 

The funtions takes a list of dictionaries containing JSON paths keys to search for the attribute to validate and filter rule values to validate the attributes with. Under the hood, the validation process uses [Validator](https://github.com/CSenshi/Validator) to validate the JSON path values with the Validator rules. If atleast one filter group is validated, then the funcion returns True. List of possible Validator rules can be found [here](https://github.com/CSenshi/Validator/blob/master/RULES.md):

## Examples

Decorator:

Succeeded Validation

```
r = RequestFilter()

@r.request_filter_groups([
    {
        "A.B": "regex:foo",
        "C": "required|min:3"
    }
])
def func(data):
    # <response logic>
    return {"statusCode": 200}

request_data = {
    "A": {"B": "foo"},
    "C": [1, 2, 3]
},

response = func(data)
```
Returns dummy `func()` return value:
```
{"statusCode": 200}
```

Failed Validation

```
r = RequestFilter()

@r.request_filter_groups([
    {
        "A.B": "regex:foo",
        "C": "required|min:10"
    }
])
def func(data):
    # <response logic>
    return {"statusCode": 200}

request_data = {
    "A": {"B": "foo"},
    "C": [1, 2, 3]
},

response = func(data)
```
Returns `validate()` return value
```
{'statusCode': 422, 'body': ValidationError({'C': {'Min': 'Expected Maximum: 10, Got: 3'}})}
```

## Installation
Package can be found on [PyPI]()

```
pip install request-filter-groups
```

## TODO:
- Add Flask-related tests