from atlas.runtime.result import Result


def test_success():

    result = Result.ok(42)

    assert result.is_success
    assert result.value == 42

def test_failure():

    result = Result.fail("Oops")

    assert result.is_failure
    assert result.error == "Oops"