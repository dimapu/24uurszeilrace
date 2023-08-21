import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator

BEARINGS = [0, 10, 20, 30, 40, 90, 120, 180]
SPEED = [0, 0, 0, 0, 4, 5, 3, 2.5]
# SPEED_SPLINE = CubicSpline(BEARINGS, SPEED)
SPEED_SPLINE = PchipInterpolator(BEARINGS, SPEED)


def get_speed(coarse: float, wind_direction: float) -> float:
    """Calculate SOG for given coarse and wind.

    Wind direction is where the wind is coming from.
    Pointing angle - angle of the wind wrt boat coarse.
    (0 = upwind, 180 = downwind)

    TODO: add non-zero speed when going upwind. In this case, beating gives
    non-zero speed, although smaller than @ close-haul.

    """
    pointing_angle = 180 - np.abs(180 - (wind_direction - coarse))

    speed = SPEED_SPLINE(pointing_angle)
    return speed


def plot_speed_profile():
    plt.figure()
    wind = np.linspace(0, 360)
    plt.plot(wind, get_speed(0, wind))
    plt.xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360])
    plt.grid(True)
    plt.xlabel("Pointing angle (0 = upwind, 180 = downwind)")
    plt.ylabel("Speed, knots")


def main():
    plt.close("all")
    plot_speed_profile()


if __name__ == "__main__":
    main()
