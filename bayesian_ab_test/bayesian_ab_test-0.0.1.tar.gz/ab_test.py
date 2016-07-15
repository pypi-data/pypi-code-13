from numpy.random import beta as beta_dist
import numpy


def get_samples(success, population, alpha, beta, sample_size):
    return beta_dist(success+alpha, population-success+beta, sample_size)


def probability_relative_effect(
        a_population, a_success, b_population, b_success,
        alpha, beta, sample_size, relative_effect_size):
    a_samples = get_samples(a_success, a_population, alpha, beta, sample_size)
    b_samples = get_samples(b_success, b_population, alpha, beta, sample_size)
    return numpy.mean((a_samples - b_samples)/b_samples > relative_effect_size)


def probability_absolute_effect(
        a_population, a_success, b_population, b_success,
        alpha, beta, sample_size, absolute_effect_size):
    a_samples = get_samples(a_success, a_population, alpha, beta, sample_size)
    b_samples = get_samples(b_success, b_population, alpha, beta, sample_size)
    return numpy.mean((a_samples - b_samples) > absolute_effect_size)
