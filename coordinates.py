import numpy as np


def convert_coordinate(c: str) -> float:
    """Convert coordinate string to float.

    Input format: "52°30,0000' N"
    """
    new = (
        c.replace("°", " ")
        .replace("'", " ")
        .replace('"', " ")
        .replace(",", ".")
    )
    try:
        deg, minutes, direction = new.split()
    except Exception as e:
        print(new)
        raise e
    return int(deg) + float(minutes) / 60.0


def get_direction(dx: float, dy: float) -> float:
    """Return bearing from 0 to 360 degree.

    dx and dy are corrdinate differences, end_point - start_point.

    0 is when the second point is to the north, i.e. dy > 0, dx == 0
    90 is when the second point is to the east, i.e. dy == 0, dx > 0,
    etc.
    """
    return ((np.arctan2(dx, dy) / np.pi * 180) + 360) % 360


def main():
    pass


if __name__ == "__main__":
    main()
