import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator

BEARINGS = [0, 10, 20, 30, 40, 90, 120, 180]
SPEED = [0, 0, 0, 0, 4, 5, 3, 2.5]
# SPEED_SPLINE = CubicSpline(BEARINGS, SPEED)
SPEED_SPLINE = PchipInterpolator(BEARINGS, SPEED)


COURSE_SPEED_DATA_ALEX = [
    (0, 0.1),
    (10, 0.1),
    (20, 0.1),
    (30, 0.1),
    (40, 4.5),
    (50, 5),
    (60, 5),
    (70, 5.5),
    (80, 6),
    (90, 6),
    (100, 5.5),
    (110, 5),
    (120, 4.5),
    (130, 4),
    (140, 4),
    (150, 3.5),
    (160, 3.5),
    (170, 3.5),
    (180, 3.5),
    # (190, 3.5),
    # (200, 3.5),
    # (210, 3.5),
    # (220, 4),
    # (230, 4),
    # (240, 4.5),
    # (250, 5),
    # (260, 5.5),
    # (270, 6),
    # (280, 6),
    # (290, 5.5),
    # (300, 5),
    # (310, 5),
    # (320, 4.5),
    # (330, 0.1),
    # (340, 0.1),
    # (350, 0.1),
    # (360, 0.1)
]
BEARINGS_ALEX = [s[0] for s in COURSE_SPEED_DATA_ALEX]
SPEED_ALEX = [s[1] for s in COURSE_SPEED_DATA_ALEX]
SPEED_SPLINE_ALEX = PchipInterpolator(BEARINGS_ALEX, SPEED_ALEX)


def calculate_pointing_angle(coarse: float, wind_direction: float) -> float:
    
    assert 0 <= wind_direction < 360, "wind direction must be in [0, 360)"

    pointing_angle = np.abs(-np.abs((coarse - wind_direction) - 180) + 180)
    pointing_angle = -np.abs(-(pointing_angle - 180)) + 180

    return pointing_angle


MODELS = {'alex': SPEED_SPLINE_ALEX, 
          "dima": SPEED_SPLINE}


def get_speed(coarse: float, wind_direction: float, model="alex") -> float:
    """Calculate SOG for given coarse and wind.

    Wind direction is where the wind is coming from.
    Pointing angle - angle of the wind wrt boat coarse.
    (0 = upwind, 180 = downwind)

    TODO: add non-zero speed when going upwind. In this case, beating gives
    non-zero speed, although smaller than @ close-haul.

    """
    spline = MODELS[model]
    pointing_angle = calculate_pointing_angle(coarse, wind_direction)

    speed = spline(pointing_angle)
    return speed


def plot_pointing_angle_profile(wind=0):
    plt.figure()

    coarse = np.linspace(0, 360)
    plt.plot(coarse, calculate_pointing_angle(coarse, wind))
    plt.xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360])
    plt.grid(True)
    plt.xlabel("Coarse")
    plt.ylabel(f"Pointing angle (0 = upwind, 180 = downwind). Wind is {wind}")


def plot_speed_profile():
    plt.figure()

    wind = 0

    coarse = np.linspace(0, 360, 360)
    
    plt.plot(coarse, get_speed(coarse, wind, model="alex"), label="alex")
    plt.plot(BEARINGS_ALEX, SPEED_ALEX, ".", label="alex_data")
    plt.plot(coarse, get_speed(coarse, wind, model="dima"), label="dima")
    plt.plot(BEARINGS, SPEED, ".", label="dima_data")
    
    plt.xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360])
    plt.grid(True)
    # plt.xlabel("Coarse. Pointing angle (0 = upwind, 180 = downwind)")
    plt.xlabel(f"Coarse. Wind is {wind}")
    plt.ylabel("Speed, knots")


def main():
    plt.close("all")
    plot_speed_profile()
    plot_pointing_angle_profile(340)


if __name__ == "__main__":
    main()
