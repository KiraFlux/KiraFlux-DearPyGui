import colorsys
from dataclasses import dataclass
from typing import ClassVar, Self


@dataclass(frozen=True)
class Color:
    """Цвет"""

    _rgba_8888_max: ClassVar = 255
    """Максимальное значение канала в формате RGB888"""

    _luma_r: ClassVar = 0.2126
    _luma_g: ClassVar = 0.7152
    _luma_b: ClassVar = 0.0722

    red: float
    """Компонента красного [0;1]"""
    green: float
    """Компонента зеленого [0;1]"""
    blue: float
    """Компонента синего [0;1]"""
    alpha: float
    """Компонента прозрачности [0;1]"""

    def __post_init__(self) -> None:
        assert 0.0 <= self.red <= 1.0
        assert 0.0 <= self.green <= 1.0
        assert 0.0 <= self.blue <= 1.0
        assert 0.0 <= self.alpha <= 1.0

    # factory

    @classmethod
    def none(cls) -> Self:
        """Прозрачный"""
        return cls(0, 0, 0, 0)

    @classmethod
    def white(cls) -> Self:
        """Белый"""
        return cls.from_hex('#ffffff')

    @classmethod
    def black(cls) -> Self:
        """Черный"""
        return cls.from_hex("#000000")

    @classmethod
    def gray(cls, grayness: float) -> Self:
        """
        Создать серый
        :param grayness Значение серого [0;1]
        """
        return cls(grayness, grayness, grayness, 1.0)

    # discord

    @classmethod
    def discord_gray(cls) -> Self:
        """Discord Grey"""
        return cls.from_hex("#99AAB5")

    @classmethod
    def discord_nitro(cls) -> Self:
        """Discord Nitro"""
        return cls.from_hex("#FF73FA")

    @classmethod
    def discord_online(cls) -> Self:
        """Discord Online"""
        return cls.from_hex("#43B581")

    @classmethod
    def discord_primary(cls) -> Self:
        """Discord Primary Button (Blurple)"""
        return cls.from_hex("#5865F2")

    @classmethod
    def discord_secondary(cls) -> Self:
        """Discord Secondary Button (Grey)"""
        return cls.from_hex("#4F545C")

    @classmethod
    def discord_success(cls) -> Self:
        """Discord Success Button (Green)"""
        return cls.from_hex("#57F287")

    @classmethod
    def discord_danger(cls) -> Self:
        """Discord Danger Button (Red)"""
        return cls.from_hex("#ED4245")

    @classmethod
    def discord_warning(cls) -> Self:
        """Discord Warning Button (Yellow)"""
        return cls.from_hex("#FEE75C")

    # from

    @classmethod
    def from_hex(cls, _hex: str) -> Self:
        """Создать цвет на основе HEX строки"""
        assert len(_hex) == 7
        assert _hex[0] == '#'

        r = int(_hex[1:3], 16)
        g = int(_hex[3:5], 16)
        b = int(_hex[5:7], 16)

        return cls.from_rgb888(r, g, b)

    @classmethod
    def from_rgb888(cls, r: int, g: int, b: int) -> Self:
        """Создать из формата RGB888"""
        return cls.from_rgba8888(r, g, b, cls._rgba_8888_max)

    @classmethod
    def from_rgba8888(cls, r: int, g: int, b: int, a: int) -> Self:
        """Создать из формата RGBA888"""
        return cls(
            r / cls._rgba_8888_max,
            g / cls._rgba_8888_max,
            b / cls._rgba_8888_max,
            a / cls._rgba_8888_max,
        )

    @classmethod
    def from_hsl(cls, hue: float, saturation: float, lightness: float) -> Self:
        """Создать из формата HSL
        :param hue: от 0 до 360
        :param saturation: [0;1]
        :param lightness:  [0;1]
        :return:
        """

        c = (1 - abs(2 * lightness - 1)) * saturation
        x = c * (1 - abs((hue / 60) % 2 - 1))
        m = lightness - c / 2

        index = int(hue // 60) % 6

        table = (
            (c, x, 0),
            (x, c, 0),
            (0, c, x),
            (0, x, c),
            (x, 0, c),
            (c, 0, x),
        )

        r, g, b = table[index]
        return cls(r + m, g + m, b + m, 1.0)

    # to

    def to_rgb888(self) -> tuple[int, int, int]:
        """Преобразовать в формат RGB888"""
        return (
            int(self.red * self._rgba_8888_max),
            int(self.green * self._rgba_8888_max),
            int(self.blue * self._rgba_8888_max)
        )

    def to_rgba8888(self) -> tuple[int, int, int, int]:
        """Преобразовать в формат RGBA8888"""
        return (
            int(self.red * self._rgba_8888_max),
            int(self.green * self._rgba_8888_max),
            int(self.blue * self._rgba_8888_max),
            int(self.alpha * self._rgba_8888_max)
        )

    def to_hsl(self) -> tuple[float, float, float]:
        """Преобразует цвет в формат HSL"""
        h, l, s = colorsys.rgb_to_hls(self.red, self.green, self.blue)
        return h * 360, s, l

    # methods

    def to_hex(self) -> str:
        """Преобразовать в HEX представление"""
        r, g, b = self.to_rgb888()
        return f"#{r:02x}{g:02x}{b:02x}"

    def brightness(self) -> float:
        """Вычислить нормализованную яркость"""
        return self._luma_r * self.red + self._luma_g * self.green + self._luma_b * self.blue

    def darker(self, k: float) -> Self:
        """Возвращает более темный цвет.
        :param k: Коэффициент затемнения [0;1]
        """
        assert 0.0 <= k <= 1.0
        h, s, l = self.to_hsl()
        new_l = l * (1 - k)

        return Color.from_hsl(h, s, new_l).with_alpha(self.alpha)

    def lighter(self, k: float) -> Self:
        """Возвращает более светлый цвет.
        :param k: Коэффициент осветления [0;1]
        """

        assert 0.0 <= k <= 1.0

        h, s, l = self.to_hsl()
        new_l = l + (1 - l) * k

        return Color.from_hsl(h, s, new_l).with_alpha(self.alpha)

    def saturated(self, k: float) -> Self:
        """Увеличивает насыщенность цвета.

        :param k: Коэффициент увеличения насыщенности [0;1]
        """
        assert 0.0 <= k <= 1.0

        h, s, l = self.to_hsl()
        new_s = s + (1 - s) * k

        return Color.from_hsl(h, new_s, l).with_alpha(self.alpha)

    def desaturated(self, k: float) -> Self:
        """Уменьшает насыщенность цвета (делает блеклым).

        :param k: Коэффициент уменьшения насыщенности [0;1]
        """
        assert 0.0 <= k <= 1.0

        h, s, l = self.to_hsl()
        new_s = s * (1 - k)

        return Color.from_hsl(h, new_s, l).with_alpha(self.alpha)

    def with_alpha(self, alpha: float) -> Self:
        """Возвращает копию цвета с новой прозрачностью.

        :param alpha: Новое значение прозрачности [0;1]
        """
        return Color(self.red, self.green, self.blue, alpha)
