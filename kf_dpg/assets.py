import os
from pathlib import Path
from typing import Final, final


class Assets:
    # paths

    app_path: Final = Path(os.getcwd())

    assets_dir: Final = app_path / "assets"

    fonts_dir: Final = assets_dir / "fonts"

    def __new__(cls):
        raise TypeError
