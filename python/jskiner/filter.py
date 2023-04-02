import os
import pickle
import subprocess
import typing
import math


class FileFilter:
    """
    Filter out file which has already been captured in the downstream pipeline.
    Args:
        - set_size: approximate number of element in the set.
        - dump_file_path: the path to store the index set status information.
        - error_rate: the error rate of identifying an non-existing item in the set.
        - verbose: whether to print the progress.
    """

    def __init__(
        self,
        set_size=10000000,
        dump_file_path="cuckoo.pickle",
        error_rate: float = 0.01,
        verbose=False,
    ):
        self._dump_file_path = dump_file_path
        self._verbose = verbose
        if os.path.exists(self._dump_file_path):
            self._cuckoo = self.load()
        else:
            if self._verbose:
                print("building cuckoo filter...")
            assert error_rate <= 1.0 and error_rate > 0.0
            bucket_size = round(-math.log10(error_rate)) + 1
            # fingerprint_size = int(math.ceil(math.log(1.0 / error_rate, 2) + math.log(2 * bucket_size, 2)))
            if bucket_size == 1:
                alpha = 0.5
            elif bucket_size >= 2 and bucket_size < 4:
                alpha = 0.84
            elif bucket_size >= 4 and bucket_size < 8:
                alpha = 0.95
            elif bucket_size >= 8:
                alpha = 0.98
            capacity = round(set_size / alpha)
            if self._verbose:
                print("capacity:", capacity)
                print("false positive rate:", error_rate)
                print("bucket size:", bucket_size)
            try:
                from cuckoo.filter import CuckooFilter
            except ImportError:
                subprocess.run(["pip", "install", "scalable-cuckoo-filter"])
                from cuckoo.filter import CuckooFilter
            self._cuckoo = CuckooFilter(
                capacity=capacity, error_rate=error_rate, bucket_size=bucket_size
            )

    def remove(self, file_name: str):
        self._cuckoo.delete(file_name)

    def insert(self, file_name: str):
        self._cuckoo.insert(file_name)

    def connect(self, fn_generator: typing.Iterable):
        for fn in fn_generator:
            if not self._cuckoo.contains(fn):
                yield fn

    def load(self):
        with open(self._dump_file_path, "rb") as handle:
            result = pickle.load(handle)
        if self._verbose:
            print(f"{self._dump_file_path} Loaded")
        return result

    def save(self):
        with open(self._dump_file_path, "wb") as handle:
            pickle.dump(self._cuckoo, handle, protocol=pickle.HIGHEST_PROTOCOL)
        if self._verbose:
            print(f"{self._dump_file_path} Saved")