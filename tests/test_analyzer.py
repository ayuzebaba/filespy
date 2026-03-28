import pytest
import os
from filespy.analyzer import count_lines, count_words, get_file_size, get_extension


# ============================================
# FIXTURES — reusable test setup
# ============================================

@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary test file for testing."""
    file = tmp_path / "test.txt"
    file.write_text("Hello world\nThis is line two\nAnd line three")
    return str(file)


@pytest.fixture
def empty_file(tmp_path):
    """Create a temporary empty file for testing."""
    file = tmp_path / "empty.txt"
    file.write_text("")
    return str(file)


# ============================================
# count_lines TESTS
# ============================================

def test_count_lines_normal_file(sample_file):
    """Test line counting on a normal file."""
    assert count_lines(sample_file) == 3


def test_count_lines_empty_file(empty_file):
    """Test line counting on an empty file."""
    assert count_lines(empty_file) == 0


def test_count_lines_file_not_found():
    """Test that missing file raises an error."""
    with pytest.raises(FileNotFoundError):
        count_lines("this_file_does_not_exist.txt")


# ============================================
# count_words TESTS
# ============================================

def test_count_words_normal_file(sample_file):
    """Test word counting on a normal file."""
    assert count_words(sample_file) == 9


def test_count_words_empty_file(empty_file):
    """Test word counting on an empty file."""
    assert count_words(empty_file) == 0


# ============================================
# get_file_size TESTS
# ============================================

def test_get_file_size_normal_file(sample_file):
    """Test that file size is a positive number."""
    size = get_file_size(sample_file)
    assert size > 0


def test_get_file_size_empty_file(empty_file):
    """Test that empty file has zero size."""
    size = get_file_size(empty_file)
    assert size == 0.0


def test_get_file_size_missing_file():
    """Test that missing file returns None."""
    size = get_file_size("missing_file.txt")
    assert size is None


# ============================================
# get_extension TESTS
# ============================================

def test_get_extension_txt_file(sample_file):
    """Test extension detection for .txt file."""
    assert get_extension(sample_file) == ".txt"


def test_get_extension_no_extension(tmp_path):
    """Test extension detection for file with no extension."""
    file = tmp_path / "noextension"
    file.write_text("some content")
    assert get_extension(str(file)) == "no extension"


def test_get_extension_python_file(tmp_path):
    """Test extension detection for .py file."""
    file = tmp_path / "script.py"
    file.write_text("print('hello')")
    assert get_extension(str(file)) == ".py"