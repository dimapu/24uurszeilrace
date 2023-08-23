import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator

BEARINGS = [0, 10, 20, 30, 40, 90, 120, 180]
SPEED = [0, 0, 0, 0, 4, 5, 3, 2.5]
# SPEED_SPLINE = CubicSpline(BEARINGS, SPEED)
SPEED_SPLINE = PchipInterpolator(BEARINGS, SPEED)


def calculate_pointing_angle(coarse: float, wind_direction: float) -> float:
    assert 0 <= wind_direction < 360, "wind direction must be in [0, 360)" 
    
    pointing_angle =  np.abs(- np.abs((coarse - wind_direction) - 180) + 180)
    pointing_angle = -np.abs(-(pointing_angle - 180)) + 180
    
    return pointing_angle


def get_speed(coarse: float, wind_direction: float) -> float:
    """Calculate SOG for given coarse and wind.

    Wind direction is where the wind is coming from.
    Pointing angle - angle of the wind wrt boat coarse.
    (0 = upwind, 180 = downwind)

    TODO: add non-zero speed when going upwind. In this case, beating gives
    non-zero speed, although smaller than @ close-haul.

    """
    pointing_angle = calculate_pointing_angle(coarse, wind_direction)

    speed = SPEED_SPLINE(pointing_angle)
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
    
    wind = 90
    
    coarse = np.linspace(0, 360, 360)
    plt.plot(coarse, get_speed(coarse, wind))
    plt.xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360])
    plt.grid(True)
    # plt.xlabel("Coarse. Pointing angle (0 = upwind, 180 = downwind)")
    plt.xlabel(f"Coarse. Wind is {wind}")
    plt.ylabel("Speed, knots")


def main():
    plt.close("all")
    # plot_speed_profile()
    plot_pointing_angle_profile(340)


if __name__ == "__main__":
    main()
