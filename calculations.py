from datetime import datetime, timedelta
from math import *


def angle_in_360(x: float) -> float:
    if 0 <= x <= 360:
        return x
    return x-(360*(x//360))


def date_to_j_day() -> float:
    day = timedelta(1)
    julian_epoch = datetime(2000, 1, 1, 12)
    j2000_jd = timedelta(2451545)
    dt = datetime.now()

    h = dt.hour - 4  # for Universal time. We are in GT+4 zone
    julian_day = (dt.replace(hour=h) - julian_epoch + j2000_jd) / day

    return julian_day


def calc_j_time_centuries(julian_date: float) -> float:
    return (julian_date - 2451545.0)/36525


def calc_moon_mean_longitude(t: float) -> float:
    mean_long = 218.3164477 + 481267.88123421*t - 0.0015786*(t**2) \
                + (t**3)/538841 - (t**4)/65194000
    return angle_in_360(mean_long)


def calc_sun_mean_longitude(t: float) -> float:
    mean_long = 280.46646 + 36000.76983*t + 0.0003032*t*t
    return angle_in_360(mean_long)


def calc_moon_elongation(t: float) -> float:
    moon_elongation = 297.8501921 + 445267.1114034*t - 0.0018819*(t**2) \
        + (t**3)/545868 - (t**4)/11306500
    return angle_in_360(moon_elongation)


def calc_sun_anomaly(t: float) -> float:
    sun_anomaly = 357.5291092 + 35999.0502909*t - 0.0001536*(t**2) \
                + (t**3)/24490000
    return angle_in_360(sun_anomaly)


def calc_moon_anomaly(t: float) -> float:
    moon_anomaly = 134.9633964 + 477198.8675055*t \
                    + 0.0087414*(t**2) + (t**3)/69699 - (t**4)/14712000
    return angle_in_360(moon_anomaly)


def calc_dist_from_asc_node(t: float) -> float:
    dist_asc_node = 93.2720950 + 483202.0175233*t - 0.0036539*(t**2)\
                    - (t**3)/3526000 + (t**4)/863310000
    return angle_in_360(dist_asc_node)


def calc_arguments(t: float) -> tuple:
    a1 = angle_in_360(119.75 + 131.849*t)
    a2 = angle_in_360(53.09 + 479264.290*t)
    a3 = angle_in_360(313.45 + 481266.484*t)

    return angle_in_360(a1), angle_in_360(a2), angle_in_360(a3)


def calc_effect_by_sun(t: float) -> float:
    effect_by_sun = 1 - 0.002516*t - 0.0000074*(t**2)
    return effect_by_sun


def calc_nutation_in_longitude(t: float, sun_mean_long: float,
                               moon_mean_long: float) -> float:
    sun_mean_long = radians(sun_mean_long)
    moon_mean_long = radians(moon_mean_long)
    omega = 125.04452 - 1934.136261*t + 0.0020708*t*t + (t**3)/450000
    omega = radians(omega)
    delta_psi = (-17.2/3600)*sin(omega) + (1.32/3600)*sin(2*sun_mean_long) \
        - (0.23/3600)*sin(2*moon_mean_long) + (0.21/3600)*sin(2*omega)

    return delta_psi


def calc_nutation_in_obliquity(t: float, sun_mean_long: float,
                               moon_mean_long: float) -> float:
    sun_mean_long = radians(sun_mean_long)
    moon_mean_long = radians(moon_mean_long)
    omega = radians(125.04452 - 1934.136261*t + 0.0020708*t*t + (t**3)/450000)
    delta_epsilon = (9.2/3600)*cos(omega) + (0.57/3600)*cos(2*sun_mean_long)\
        + (0.1/3600)*cos(2*moon_mean_long) - (0.09/3600)*cos(2*omega)
    epsilon0 = 23.4392911 - 0.0130041667 * t - (0.00059/3600) * (t ** 2) \
        + (0.001813/3600) * (t ** 3)
    epsilon = delta_epsilon + epsilon0

    return epsilon


def calc_periodic_terms_sum(coefficient_lst: list,
                            arg_lst: list,
                            mean_elong: float,
                            s_anomaly: float,
                            m_anomaly: float,
                            dist_asc_node: float,
                            sun_effect: float) -> float:
    idx = -1
    suum = 0
    for i in arg_lst:
        idx += 1
        val = sin(radians(
            i[0] * mean_elong + i[1] * s_anomaly
            + i[2] * m_anomaly + i[3] * dist_asc_node))
        if i[1] == 1 or i[1] == -1:
            suum += val * coefficient_lst[idx] * sun_effect
        if i[1] == 2 or i[1] == -2:
            suum += val * coefficient_lst[idx] * (sun_effect ** 2)
        else:
            suum += val * coefficient_lst[idx]

    return suum


def calc_ecliptic_longitude(mean_longitude: float, sum_longitude: float
                            ) -> float:
    return angle_in_360(mean_longitude + sum_longitude/1000000)


def calc_ecliptic_latitude(sum_latitude: float) -> float:
    return sum_latitude/1000000


def calc_adds_to_eclp_lat(mean_longitude: float,
                          moon_anomaly: float,
                          dist_asc_node, a1, a3) -> float:
    longitude = radians(mean_longitude)
    mm = radians(moon_anomaly)
    f = radians(dist_asc_node)
    a1 = radians(a1)
    a3 = radians(a3)
    return -2235 * sin(longitude) + 382 * sin(a3) + 175 * sin(a1 - f) \
        + 175 * sin(a1 + f) + 127 * sin(longitude - mm) - 115*sin(longitude+mm)


def calc_adds_to_eclp_long(mean_longitude: float,
                           dist_asc_node: float,
                           a1: float, a2: float) -> float:
    longitude = radians(mean_longitude)
    f = radians(dist_asc_node)
    a1 = radians(a1)
    a2 = radians(a2)
    return 3958*sin(a1) + 1962*sin(longitude-f) + 318*sin(a2)


def calc_ra_dec(ecliptic_longitude: float,
                ecliptic_latitude: float,
                epsilon: float) -> tuple:

    e_long = radians(ecliptic_longitude)
    e_lat = radians(ecliptic_latitude)
    epsilon = radians(epsilon)
    ra = degrees(atan(
        (sin(e_long)*cos(epsilon) - tan(e_lat)*sin(epsilon))/cos(e_long)
        ))
    dec = degrees(asin(
        sin(e_lat)*cos(epsilon) + cos(e_lat)*sin(epsilon)*sin(e_long)
            ))

    return ra, dec


def format_ra(deg: float) -> str:
    h = int(deg//15)
    m = (deg/15 - h) * 60
    s = (m - int(m)) * 60
    return f"{h}h {int(m)}m {s:.2f}s"


def format_dec(deg: float) -> str:
    degree = int(deg)
    minutes = (deg - degree) * 60
    sec = (minutes - int(minutes)) * 60
    return f"{degree}deg {int(minutes)}m {sec:.2f}s"


def adjust_ra_borders(ra: float):
    if ra > 360:
        ra = ra - (ra//360)*360

    if ra < 0:
        ra = abs(ra)
        ra = ra - (ra//180)*180
        ra = 180 - ra

    return ra
