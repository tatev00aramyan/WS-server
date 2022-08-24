import calculations as clc
from periodics import longitude_periodic_coef, longitude_periodic_arguments,\
                latitude_periodic_coef, latitude_periodic_arguments


def get_needed_values():
    julian_date = clc.date_to_j_day()
    t = clc.calc_j_time_centuries(julian_date)  # T
    mean_elongation = clc.calc_moon_elongation(t)    # D
    sun_anomaly = clc.calc_sun_anomaly(t)  # Ms
    moon_anomaly = clc.calc_moon_anomaly(t)  # M'm
    dist_from_asc_node = clc.calc_dist_from_asc_node(t)  # F
    sun_mean_long = clc.calc_sun_mean_longitude(t)  # L
    moon_mean_long = clc.calc_moon_mean_longitude(t)  # L'
    effect_by_sun = clc.calc_effect_by_sun(t)  # E
    a1, a2, a3 = clc.calc_arguments(t)  # A1 A2 A3
    epsilon = clc.calc_nutation_in_obliquity(t, sun_mean_long, moon_mean_long)

    return t, mean_elongation, sun_anomaly, moon_anomaly, dist_from_asc_node,\
        moon_mean_long, effect_by_sun, a1, a2, a3, epsilon, sun_mean_long


def run():
    t, mean_elongation, sun_anomaly,\
        moon_anomaly, dist_from_asc_node,\
        moon_mean_long, effect_by_sun, \
        a1, a2, a3, epsilon, sun_mean_long \
        = get_needed_values()

    sum_latitude = clc.calc_periodic_terms_sum(latitude_periodic_coef,
                                               latitude_periodic_arguments,
                                               mean_elongation,
                                               sun_anomaly,
                                               moon_anomaly,
                                               dist_from_asc_node,
                                               effect_by_sun) \
        + clc.calc_adds_to_eclp_lat(moon_mean_long,
                                    moon_anomaly,
                                    dist_from_asc_node,
                                    a1, a3)
    sum_longitude = clc.calc_periodic_terms_sum(longitude_periodic_coef,
                                                longitude_periodic_arguments,
                                                mean_elongation,
                                                sun_anomaly,
                                                moon_anomaly,
                                                dist_from_asc_node,
                                                effect_by_sun) \
        + clc.calc_adds_to_eclp_long(moon_mean_long,
                                     dist_from_asc_node,
                                     a1, a2)

    ecliptic_long = clc.calc_ecliptic_longitude(moon_mean_long, sum_longitude)
    ecliptic_lat = clc.calc_ecliptic_latitude(sum_latitude)
    delta_psi = clc.calc_nutation_in_longitude(t, sun_mean_long, moon_mean_long)
    ecliptic_long += delta_psi
    ra, dec = clc.calc_ra_dec(ecliptic_long, ecliptic_lat, epsilon)

    return clc.format_ra(clc.adjust_ra_borders(ra)), clc.format_dec(dec)
