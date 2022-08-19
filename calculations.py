from datetime import datetime, timedelta
from math import sin, cos


def date_to_j_day():
    day = timedelta(1)
    julian_epoch = datetime(2000, 1, 1, 12)
    j2000_jd = timedelta(2451545)  # julian epoch in julian dates
    dt = datetime.now()
    julian_day = (dt.replace(hour=12) - julian_epoch + j2000_jd) / day

    return julian_day


def j_time_centuries(jd):
    return (jd - 2451545.0)/36525


def calc_moon_mean_long_with_light_time_effect(t):
    mean_long = 218.3164477 + 481267.88123421*t - 0.0015786*(t**2) \
                + (t**3)/538841 - (t**4)/65194000
    return angle_in_360(mean_long)


def calc_moon_elongation(t):  # D
    moon_elongation = 297.8501921 + 445267.1114034*t - 0.0018819*(t**2) \
        +(t**3)/545868 - (t**4)/11306500
    return angle_in_360(moon_elongation)


def calc_sun_anomaly(t):   # M
    sun_anomaly = 357.5291092 + 35999.0502909*t -0.0001536*(t**2) \
                + (t**3)/24490000
    return angle_in_360(sun_anomaly)


def calc_moon_anomaly(t):  # M'
    moon_anomaly = 134.9633964 + 477198.8675055*t \
                    + 0.0087414*(t**2) + (t**3)/69699 - (t**4)/14712000
    return angle_in_360(moon_anomaly)


def calc_dist_from_asc_node(t):  # F
    f = 93.2720950 + 483202.0175233*t -0.0036539*(t**2) - (t**3)/3526000 \
                    + (t**4)/863310000
    return angle_in_360(f)


def calc_arguments(t):  # A
    a1 = angle_in_360(119.75 + 131.849*t)
    a2 = angle_in_360(53.09 + 479264.290*t)
    a3 = angle_in_360(313.45 + 481266.484*t)

    return a1, a2, a3


def angle_in_360(x):
    if 0 <= x <= 360:
        return x

    return x-(360*(x//360))


def effect_by_sun(t):   # E
    e = 1 - 0.002516*t - 0.0000074*(t**2)
    return e


def run():
    # Not finished yet
    t = j_time_centuries(date_to_j_day())
    d = calc_moon_elongation(t)
    ms = calc_sun_anomaly(t)
    mm = calc_moon_anomaly(t)
    f = calc_dist_from_asc_node(t)
    l = calc_moon_mean_long_with_light_time_effect(t)
    temp_list = []
    e = effect_by_sun(t)
    a1, a2, a3 = calc_arguments(t)

    dmmf = (d, ms, mm, f)

    return


if __name__ == "__main__":

    run()

    '''Not finished yet'''