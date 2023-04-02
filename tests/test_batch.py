from jskiner.batch import Batcher


def test_connect():
    batcher = Batcher(3)
    output_generator = batcher.connect([1, 2, 3, 4, 5, 6, 7])
    assert next(output_generator) == [1, 2, 3]
    assert next(output_generator) == [4, 5, 6]
    assert next(output_generator) == [7]
