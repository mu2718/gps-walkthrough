import numpy as np


class SdrWave:
    """Recorded radio wave."""

    def __init__(self, samples: np.ndarray, sampling_dt: int) -> None:
        """
        Arguments:
        - amplitudes: array of samples of the radio wave, i.e. in general complex-valued amplitudes
        - sampling_dt: sampling "delta time", i.e. time step per sample
        """
        self.samples = samples
        self.sampling_dt = sampling_dt

    def duration(self) -> int:
        """Duration of wave in units of seconds."""
        return len(self.samples) * self.sampling_dt
    
    def get_interval(self, from_time: float = None, to_time: float = None):
        """Returns SdrWave with specified time interval."""
        if from_time:
            from_sample = int(from_time / self.sampling_dt)
        else:
            from_sample = 0

        if to_time:
            to_sample = int(to_time / self.sampling_dt)
        else:
            to_sample = len(self.samples)

        return SdrWave(self.samples[from_sample:to_sample], self.sampling_dt)

    @staticmethod
    def from_raw_file(filename, sampling_rate, dtype='byte', max_samples=-1):
        """
        Read component-interleaved complex signal from raw file.

        Arguments:
        - sampling_rate: samples per second [S/s]
        - dtype:  Data type, use 'byte' for `hackrf_transfer` output
                  and 'float32' for GNU Radio 'gr_complex' / complex float format.
        """

        sampling_dt = 1 / sampling_rate  # [s/S], time step per sample

        data = np.fromfile(filename, dtype=dtype, count=max_samples)
        amplitudes = data[0::2] + 1j * data[1::2]  # de-interleave to get complex

        return SdrWave(amplitudes, sampling_dt)