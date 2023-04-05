from app.tasks import get_lines_of_code


def test_lines_of_code_api():
    """Test that API for getting the total lines of code works well"""
    print("Testing API for getting the total lines of code...")
    status, result = get_lines_of_code()

    assert isinstance(status, bool)
    assert isinstance(result, int)
