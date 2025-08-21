import secrets
import string

import svgwrite


class BaseDrawer:
    def __init__(self):
        self._frames = []
        self._fps = 60
        self._draw_group_name: str = "Group"
        self._id = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(5)
        )
        self._duration = 0
        self._key_times_str = ''
        self._frames_to_use = self._frames
        self._n_frames = 0

    def start_recording(self, fps: int = 60) -> None:
        self._frames = []
        self._fps = max(1, fps)

    def record_frame(self) -> None:
        raise NotImplementedError()

    def to_group(
            self,
            dwg: svgwrite.Drawing,
            frame_skip:int = 1
    ) -> svgwrite.Drawing:

        if not self._frames:
            raise RuntimeError("There is no frames to save")

        self._n_frames = len(self._frames)
        self._duration = self._n_frames / self._fps

        self._frames_to_use = self._frames[::frame_skip] if frame_skip > 1 \
            else self._frames

        if self._n_frames == 1:
            key_times = ["0", "1"]
        else:
            key_times = [
                f"{i / (len(self._frames_to_use) - 1):.6f}"
                for i in range(len(self._frames_to_use))
            ]
        self._key_times_str = ";".join(key_times)
        group = dwg.g(id=f"{self._draw_group_name}-{self._id}")
        self._n_frames = len(self._frames_to_use)
        return group
