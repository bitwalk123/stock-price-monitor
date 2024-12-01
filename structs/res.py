from dataclasses import dataclass


@dataclass(frozen=True)
class AppRes:
    path_image = 'images'

    def getImagePath(self) -> str:
        return self.path_image
