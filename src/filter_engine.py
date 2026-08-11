import importlib
import glob
import os

class FilterEngine:
    def __init__(self):
        self.filters = []
        self.current_index = 0
        self.intensity = 1.0
        self._load_filters()

    def _load_filters(self):
        # We'll just hardcode them for simplicity, or load them from filters package
        from filters.original import OriginalFilter
        from filters.grayscale import GrayscaleFilter
        from filters.sepia import SepiaFilter
        from filters.warm import WarmFilter
        from filters.cool import CoolFilter
        from filters.vintage import VintageFilter
        from filters.vivid import VividFilter
        from filters.negative import NegativeFilter
        from filters.cinematic import CinematicFilter

        self.filters = [
            OriginalFilter(),
            GrayscaleFilter(),
            SepiaFilter(),
            WarmFilter(),
            CoolFilter(),
            VintageFilter(),
            VividFilter(),
            NegativeFilter(),
            CinematicFilter()
        ]

    def next_filter(self):
        self.current_index = (self.current_index + 1) % len(self.filters)

    def previous_filter(self):
        self.current_index = (self.current_index - 1) % len(self.filters)

    def get_current_filter_name(self):
        if not self.filters:
            return "None"
        return self.filters[self.current_index].name

    def set_intensity(self, intensity):
        self.intensity = max(0.0, min(1.0, intensity))

    def apply(self, frame):
        if not self.filters:
            return frame
        return self.filters[self.current_index].apply(frame, self.intensity)
