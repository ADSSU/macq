from typing import Iterable, Iterator, Sized, Any


try:
    from tqdm import tqdm, trange

    TQDM = True

except ModuleNotFoundError:
    TQDM = False


def tqdm_progress(iterable=None, *args, **kwargs) -> Any:
    if isinstance(iterable, range):
        return trange(iterable.start, iterable.stop, iterable.step, *args, **kwargs)
    return tqdm(iterable, *args, **kwargs)


class vanilla_progress:
    iterable: Iterable

    def __init__(self, iterable, *args, **kwargs):
        self.iterable = iterable
        self.args = args
        self.kwargs = kwargs

    def __iter__(self) -> Iterator[Any]:
        if isinstance(self.iterable, range):
            start = self.iterable.start
            stop = self.iterable.stop
            step = self.iterable.step
            total = (stop - start) / step
        elif isinstance(self.iterable, Sized):
            total = len(self.iterable)
        else:
            total = None

        prev = 0
        it = 1
        for i in self.iterable:
            yield i
            if total is not None:
                new = int(str(it / total)[2])
                if new != prev:
                    prev = new
                    if new == 0:
                        print("100%")
                    else:
                        print(f"{new}0% ...")
            it += 1


progress = tqdm_progress if TQDM else vanilla_progress
