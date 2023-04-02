import os
from jskiner.folder.filter import FileFilter


def test_connect():
    filter = FileFilter()
    filter.insert("a")
    filter.insert("b")
    assert list(filter.connect(["a", "b", "c"])) == ["c"]


def test_remove():
    filter = FileFilter()
    filter.insert("a")
    filter.insert("b")
    filter.remove("b")
    assert list(filter.connect(["a", "b", "c"])) == ["b", "c"]


def test_save():
    filter = FileFilter()
    filter.insert("a")
    filter.insert("b")
    filter.save()
    new_filter = FileFilter()
    assert list(new_filter.connect(["a", "b", "c"])) == ["c"]
    os.remove("cuckoo.pickle")

    filter = FileFilter(dump_file_path="tmp.pickle")
    filter.insert("a")
    filter.insert("b")
    filter.save()
    new_filter = FileFilter(dump_file_path="tmp.pickle")
    assert list(new_filter.connect(["a", "b", "c"])) == ["c"]
    os.remove("tmp.pickle")
