from numbers import Number
from typing import Iterable

def hex_to_rgb(hex_color: str) -> tuple:
    if (not isinstance(hex_color, Iterable)):
        raise TypeError()

    if (hex_color.startswith('#')):
        hex_color = hex_color[1:]

    hex_color: str = hex_color.lower()
    temp_hex_color: str = hex_color.replace('a', '').replace('b', '').replace('c', '') \
        .replace('d', '').replace('e', '').replace('f', '')

    if (not temp_hex_color.isnumeric() and temp_hex_color != ''):
        raise (BaseException())

    if (len(hex_color) > 6):
        raise (ValueError())
    if (len(hex_color) < 6):
        hex_color += '0' * (6 - len(hex_color))

    return ((int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)))

def hex_to_rgba(hex_color: str) -> tuple:
    if (not isinstance(hex_color, Iterable)):
        raise TypeError()

    if (hex_color.startswith('#')):
        hex_color = hex_color[1:]

    hex_color: str = hex_color.lower()
    temp_hex_color: str = hex_color.replace('a', '').replace('b', '').replace('c', '') \
        .replace('d', '').replace('e', '').replace('f', '')

    if (not temp_hex_color.isnumeric() and temp_hex_color != ''):
        raise (BaseException())

    if (len(hex_color) > 8):
        raise (ValueError())
    if (len(hex_color) < 8):
        hex_color += '0' * (8 - len(hex_color))

    return ((int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16), int(hex_color[6:8], 16)))

def rgb_to_hex(r: int = 0, g: int = 0, b: int = 0, upper: bool = False, add_hashtag: bool = True) -> str:
    if (not isinstance(r, Number) or not isinstance(g, Number) or not isinstance(b, Number)):
        raise (TypeError())
    
    result = '#' if add_hashtag else ''
    result += hex(r).replace('0x', '').zfill(2)
    result += hex(g).replace('0x', '').zfill(2)
    result += hex(b).replace('0x', '').zfill(2)

    return (result.upper() if upper else result)

def rgba_to_hex(r: int = 0, g: int = 0, b: int = 0, a: int = 0, upper: bool = False, add_hashtag: bool = True) -> str:
    if (not isinstance(r, Number) or not isinstance(g, Number) or not isinstance(b, Number) or not isinstance(a, Number)):
        raise (TypeError())
    
    result = '#' if add_hashtag else ''
    result += hex(r).replace('0x', '').zfill(2)
    result += hex(g).replace('0x', '').zfill(2)
    result += hex(b).replace('0x', '').zfill(2)
    result += hex(a).replace('0x', '').zfill(2)

    return (result.upper() if upper else result)

def rgb_to_endian(r: int = 0, g: int = 0, b: int = 0) -> int:
    if (not isinstance(r, Number) or not isinstance(g, Number) or not isinstance(b, Number)):
        raise (TypeError())

    return ((((r << 8) + g) << 8) + b)

def rgba_to_endian(r: int = 0, g: int = 0, b: int = 0, a: int = 0) -> int:
    if (not isinstance(r, Number) or not isinstance(g, Number) or not isinstance(b, Number) or not isinstance(a, Number)):
        raise (TypeError())

    return ((((((r << 8) + g) << 8) + b) << 8) + a)

def endian_to_rgb(color: int) -> tuple:
    if (not isinstance(color, Number)):
        raise (TypeError())

    red: int = (color >> 16)
    green: int = (color >> 8) & 0xFF
    blue: int = color & 0xFF

    return (red, green, blue)

def endian_to_rgba(color: int) -> tuple:
    if (not isinstance(color, Number)):
        raise (TypeError())

    red: int = (color >> 24)
    green: int = (color >> 16) & 0xFF
    blue: int = (color >> 8) & 0xFF
    alpha: int = color & 0xFF

    return (red, green, blue, alpha)

def rgb_to_gray(r: int, g: int, b: int, wheighted: bool = True) -> tuple:
    if (not wheighted):
        return (((r + g + b) / 3,) * 3)
    else:
        return ((0.299 * r + 0.587 * g + 0.114 * b,) * 3)

def rgb_to_sepia(r: int, g: int, b: int):
    return (
        min((r * 0.393) + (g * 0.769) + (b * 0.189), 255),
        min((r * 0.349) + (g * 0.686) + (b * 0.168), 255),
        min((r * 0.272) + (g * 0.534) + (b * 0.131), 255)
    )

def hue_to_rgb(p: float, q: float, t: float) -> int:
    if (t < 0):
        t += 1
    if (t > 1):
        t -= 1
    if (t < 1 / 6):
        return (p + (q - p) * 6 * t)
    if (t < 1 / 2):
        return (q)
    if (t < 2 / 3):
        return (p + (q - p) * (2 / 3 - t) * 6)
    return (p)

def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    r, g, b = [i / 255.0 for i in (r, g, b)]

    max_val: int = max(r, g, b)
    min_val: int = min(r, g, b)
    delta: int = max_val - min_val

    if (delta == 0):
        h: int = 0
    elif (max_val == r):
        h: float = ((g - b) / delta) % 6
    elif (max_val == g):
        h: float = ((b - r) / delta + 2)
    else:
        h: float = ((r - g) / delta + 4)

    h *= 60
    l: float = (max_val + min_val) / 2
    s: float = 0 if delta == 0 else delta / (1 - abs(2 * l - 1))

    return (h, s * 100, l * 100)

def hsl_to_rgb(h: int, s: int, l: int) -> tuple:
    h /= 360.0
    s /= 100.0
    l /= 100.0

    if s == 0:
        r, g, b = l, l, l
    else:
        q: float = l * (1 + s) if l < 0.5 else l + s - l * s
        p: float = 2 * l - q

        r: float = hue_to_rgb(p, q, h + 1 / 3)
        g: float = hue_to_rgb(p, q, h)
        b: float = hue_to_rgb(p, q, h - 1 / 3)

    return (r * 255, g * 255, b * 255)

def rgb_to_hsv(r: int, g: int, b: int) -> tuple:
    r, g, b = [i / 255.0 for i in (r, g, b)]

    max_val: int = max(r, g, b)
    min_val: int = min(r, g, b)
    delta: int = max_val - min_val

    if (delta == 0):
        h: int = 0
    elif (max_val == r):
        h: float = ((g - b) / delta) % 6
    elif (max_val == g):
        h: float = ((b - r) / delta + 2)
    else:
        h: float = ((r - g) / delta + 4)

    h *= 60
    v: float = max_val
    s: float = 0 if max_val == 0 else delta / max_val

    return (h, s * 100, v * 100)

def hsv_to_rgb(h: int, s: int, v: int) -> tuple:
    h /= 60.0
    s /= 100.0
    v /= 100.0

    i: int = int(h)
    f: float = h - i

    p: float = v * (1 - s)
    q: float = v * (1 - s * f)
    t: float = v * (1 - s * (1 - f))

    if (i == 0):
        r, g, b = v, t, p
    elif (i == 1):
        r, g, b = q, v, p
    elif (i == 2):
        r, g, b = p, v, t
    elif (i == 3):
        r, g, b = p, q, v
    elif (i == 4):
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q

    return (r * 255, g * 255, b * 255)

def rgb_to_cmyk(r: int, g: int, b: int) -> tuple:
    r, g, b = [i / 255.0 for i in (r, g, b)]

    k: int = 1 - max(r, g, b)
    c: float = (1 - r - k) / (1 - k) if k < 1 else 0
    m: float = (1 - g - k) / (1 - k) if k < 1 else 0
    y: float = (1 - b - k) / (1 - k) if k < 1 else 0

    return (c * 100, m * 100, y * 100, k * 100)

def cmyk_to_rgb(c: int, m: int, y: int, k: int) -> tuple:
    c, m, y, k = [i / 100.0 for i in (c, m, y, k)]

    r: float = (1 - c) * (1 - k)
    g: float = (1 - m) * (1 - k)
    b: float = (1 - y) * (1 - k)

    return (r * 255, g * 255, b * 255)
