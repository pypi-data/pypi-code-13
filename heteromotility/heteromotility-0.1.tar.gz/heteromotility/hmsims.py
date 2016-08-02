from __future__ import division
import random
from hmstats import GeneralFeatures, RWFeatures, MSDFeatures
from hmtrack import CellPaths
from hmtools import dictofdict2array, tripledict2array, merge_flat_lists


'''
#---------------------------
# MODULE CONTENTS
#---------------------------
Classes to generate simulated data sets for analysis, including
1. Random walk simulations
2. Biased random walk simulations

#---------------------------
# To Do
#---------------------------

3. Levy flight simulations
4. Fractal brownian motion simulations


'''


class RWSims:
    def __init__(self, obj = 100, length = 100):
        self.rw_paths = self.rwsim(obj, length)
        self.brw_paths = self.biased_rwsim(obj, length)

    def random_walk(self, N, speed_mu = 7.0, speed_sigma = None, origin = (0,0)):
        import numpy as np
        '''
        Models random walk given an origin, length N, step size : rate
        abbreviated from implementation in hmstats.RWFeatures

        Parameters
        -------------
        origin : origin point, default = (0,0)
        N : length of walk to model
        rate : step size to model

        Returns
        -------------
        model_path : list containing sequential tuples of XY coordinates

        Notes
        -------------
        step_size = rate = c = sqrt(x_step^2 + y_step^2) = sqrt(2*step^2)
        x_step = y_step = rate/sqrt(2)
        (Random Walks in Biology, 1992, Howard C. Berg)
        '''

        model_path = [ origin ]
        if speed_sigma == None:
            speed_sigma = 0.2*speed_mu
        i = 0
        while i < N:
            rate = round(np.random.normal(speed_mu, speed_sigma), 3)
            vectors = [ (0, rate), (0, -rate), (rate, 0), (-rate, 0) ]
            walk = np.random.random()
            if 0 <= walk < 0.25:
                step = vectors[0]
            elif 0.25 <= walk < 0.50:
                step = vectors[1]
            elif 0.50 <= walk < 0.75:
                step = vectors[2]
            else:
                step = vectors[3]
            new_x = model_path[-1][0] + step[0]
            new_y = model_path[-1][1] + step[1]
            model_path.append( (new_x, new_y) )

            i += 1

        return model_path

    def rwsim(self, obj, length, speed_range = range(5, 16)):
        '''
        Generates simulated object paths using an unbiased random walk model

        Parameters
        ------------
        obj : integer specifying the number of object paths to be simulated
        length : integer specifying the length of each path to be simulated
        speed_range : tuple containing integers of step sizes to use when
        building models

        Returns
        ------------
        rw_paths : dict keyed by speed, containing dicts keyed by obj id,
        containing lists of tuples, each tuple
        specifying the XY position of a simulated object at a given timepoint
            rw_paths =
            {
            speed_i : {0: [ (x1,y1), (x2,y2)...(x_n, y_n) ]
                        1: [ (x1,y1), (x2,y2)...(x_n, y_n) ]
                        ...},
            speed_i+1 : ...,
            ...
            }
        '''

        rw_paths = {}

        for speed in speed_range:
            rw_paths[speed] = {}
            i = 0
            while i < obj:
                model_path = self.random_walk(N = length, speed_mu = speed, origin = (0,0))
                rw_paths[speed][i] = model_path
                i += 1

        return rw_paths

    def biased_random_walk(self, N, speed_mu = 7.0, speed_sigma = None, bias_prop = 0.5 , origin = (0,0)):
        import numpy as np
        '''
        * Models a set of random walks biased to move in one direction
        * Randomly selects in which direction to bias movement
        * Object will move in the direction of bias a proportion of the time
        specified in bias_prop

        Parameters
        ------------
        N : length of walk to be modeled
        rate : step size to be modeled
        bias : proportion of the time an object moves in the direction of bias
        origin : origin point for the start of the walk to be modeled

        Returns
        ------------
        model_path : list of tuples, each containing an XY point

        '''
        model_path = [origin]
        if speed_sigma == None:
            speed_sigma = 0.2*speed_mu
        bias_choice = random.randrange(start = 0, stop = 4, step = 1)
        i = 0
        while i < N:
            walk = np.random.random()
            rate = round(np.random.normal(speed_mu, speed_sigma), 3)
            vectors = [ (0, rate), (0, -rate), (rate, 0), (-rate, 0) ]
            bias = vectors[bias_choice]
            vectors.pop(bias_choice)
            unbiased_prop = 1-bias_prop
            break1 = bias_prop + (unbiased_prop/3)
            break2 = bias_prop + 2*(unbiased_prop/3)
            if walk <= bias_prop:
                step = bias
            elif bias_prop < walk <= break1:
                step = vectors[0]
            elif break1 < walk <= break2:
                step = vectors[1]
            else:
                step = vectors[2]

            new_x = model_path[-1][0] + step[0]
            new_y = model_path[-1][1] + step[1]
            model_path.append( (new_x, new_y) )
            i += 1

        return model_path

    def biased_rwsim(self, obj, length, speed_range = range(5,16)):
        '''
        Generates simulated object paths using a biased random walk model

        Parameters
        ------------
        obj : integer specifying the number of object paths to be simulated
        length : integer specifying the length of each path to be simulated

        Returns
        ------------
        brw_paths : dict keyed by obj id, containing lists of tuples, each tuple
        specifying the XY position of a simulated object at a given timepoint
            rw_paths = {
            0: [ (x1,y1), (x2,y2)...(x_n, y_n) ]
            1: [ (x1,y1), (x2,y2)...(x_n, y_n) ]
            ...
            }
        '''

        brw_paths = {}

        for speed in speed_range:
            brw_paths[speed] = {}
            i = 0
            while i < obj:
                model_path = self.biased_random_walk(N = length, speed_mu = speed, bias_prop = 0.5, origin = (0,0))
                brw_paths[speed][i] = model_path
                i += 1

        return brw_paths

class LevySims:
    def __init__(self, obj = 100, length = 100):
        self.power_paths = self.power_sim(obj, length)
        self.levy_paths = self.levy_sim(obj, length)
        self.fly = levy_flier(N = 100)

    def power_flier( self, N, x_min = 0.1, alpha = 2.000, scale_coeff=50, origin = (0,0) ):
        '''
        Defines a levy flight path beginning at the origin, taking N steps,
        with step sizes pulled from a power law distribution

        Directions are chosen randomly, as in a random walk
        Step sizes however are chosen according to the distribution:

            P(l_j) ~ l_j**(-a)
            where a is a parameter in the range 1 < u <= 3

        Defaults to a = 2 as the optimal parameter for foraging behavior
        see : Viswanathan 1999, Nature

        Obtaining Levy distributed random variables
        -------------
        To transform uniformly distributed random variable
        into another distribution, use inverse cum. dist. func. (CDF)

        if F is CDF corresponding to probability density of variable f and u
        is a uniformly distributed random variable on [0,1]

        x = F^-1(u)
        for pure power law distribution P(l) = l**-a
        F(x) = 1 - ( x / x_min )
        where x_min is a lower bound on the random variable

        F^-1(u) = x_min(1 - u)^(-1/a)

        See: (Devroye 1986, Non-uniform random variable generation)

        or

        X = F^-1(U) = c / ( phi^-1(1-U/2) )**2 + mu

        c : scaling parameter
        Phi(x) : CDF of Gaussian distribution
        mu : location

        for a pure Levy distribution

        see http://www.math.uah.edu/stat/special/Levy.html

        Parameters
        -------------
        N : number of steps in the flight
        step_min : integer value, minimum step size
        origin : initial site of walk
        u = parameter for probability distribution of step sizes

        Returns
        -------------
        model_path : a list containing tuples of XY coordinates
        '''

        model_path = [ origin ]
        i = 0
        while i < N:
            rate = ( x_min*( 1-random.random() )**(-1/alpha) ) * scale_coeff
            vectors = [ (0, rate), (0, -rate), (rate, 0), (-rate, 0) ]
            walk = random.random()
            if 0 <= walk < 0.25:
                step = vectors[0]
            elif 0.25 <= walk < 0.50:
                step = vectors[1]
            elif 0.50 <= walk < 0.75:
                step = vectors[2]
            else:
                step = vectors[3]

            new_x = model_path[-1][0] + step[0]
            new_y = model_path[-1][1] + step[1]
            model_path.append( (new_x, new_y) )
            i += 1

        return model_path

    def power_sim(self, obj, length, scale_range = range(40,60)):
        '''
        Generates simulated object paths using a levy flight model with
        a power law distribution of displacements

        Parameters
        ------------
        obj : integer specifying the number of object paths to be simulated
        length : integer specifying the length of each path to be simulated

        Returns
        ------------
        levy_paths : dict keyed by obj id, containing lists of tuples, each tuple
        specifying the XY position of a simulated object at a given timepoint
            levy_paths = {
            0: [ (x1,y1), (x2,y2)...(x_n, y_n) ]
            1: [ (x1,y1), (x2,y2)...(x_n, y_n) ]
            ...
            }
        '''

        power_paths = {}

        for scale in scale_range:
            power_paths[scale] = {}
            i = 0
            while i < obj:
                model_path = self.power_flier(N = length, scale_coeff=scale)
                power_paths[scale][i] = model_path
                i += 1

        return power_paths

    def levy_flier(self, N, scale_coeff = 1, origin = (0,0)):
        '''
        Defines a levy flight path beginning at the origin, taking N steps,
        with step sizes pulled from a true Levy distribution

        scale = 2, median disp = 4.4
        scale = ~2.3 has a median displacement of 5 units

        Directions are chosen randomly, as in a random walk
        Step sizes however are chosen according to the distribution:

            P(l_j) ~ l_j**(-a)
            where a is a parameter in the range 1 < u <= 3

        Defaults to a = 2 as the optimal parameter for foraging behavior
        see : Viswanathan 1999, Nature

        Obtaining Levy distributed random variables
        -------------
        To transform uniformly distributed random variable
        into another distribution, use inverse cum. dist. func. (CDF)

        if F is CDF corresponding to probability density of variable f and u
        is a uniformly distributed random variable on [0,1]

        x = F^-1(u)
        for pure power law distribution P(l) = l**-a
        F(x) = 1 - ( x / x_min )
        where x_min is a lower bound on the random variable

        F^-1(u) = x_min(1 - u)^(-1/a)

        See: (Devroye 1986, Non-uniform random variable generation)

        or

        X = F^-1(U) = c / ( phi^-1(1-U/2) )**2 + mu

        c : scaling parameter
        Phi(x) : CDF of Gaussian distribution
        mu : location

        for a pure Levy distribution

        see http://www.math.uah.edu/stat/special/Levy.html

        Parameters
        -------------
        N : number of steps in the flight
        step_min : integer value, minimum step size
        origin : initial site of walk
        u = parameter for probability distribution of step sizes

        Returns
        -------------
        model_path : a list containing tuples of XY coordinates
        '''
        from scipy import stats.levy

        model_path = [ origin ]
        i = 0
        while i < N:
            rate = levy.rvs(scale=scale_coeff)
            vectors = [ (0, rate), (0, -rate), (rate, 0), (-rate, 0) ]
            walk = random.random()
            if 0 <= walk < 0.25:
                step = vectors[0]
            elif 0.25 <= walk < 0.50:
                step = vectors[1]
            elif 0.50 <= walk < 0.75:
                step = vectors[2]
            else:
                step = vectors[3]

            new_x = model_path[-1][0] + step[0]
            new_y = model_path[-1][1] + step[1]
            model_path.append( (new_x, new_y) )
            i += 1

        return model_path

    def levy_sim(self, obj, length, scale_range = range(1,10)):
        '''
        Generates simulated object paths using a levy flight model with a true
        Levy distribution of displacements

        Parameters
        ------------
        obj : integer specifying the number of object paths to be simulated
        length : integer specifying the length of each path to be simulated

        Returns
        ------------
        levy_paths : dict keyed by obj id, containing lists of tuples, each tuple
        specifying the XY position of a simulated object at a given timepoint
            levy_paths = {
            0: [ (x1,y1), (x2,y2)...(x_n, y_n) ]
            1: [ (x1,y1), (x2,y2)...(x_n, y_n) ]
            ...
            }
        '''

        levy_paths = {}

        for scale in scale_range:
            power_paths[scale] = {}
            i = 0
            while i < obj:
                model_path = self.levy_flier(N = length, scale_coeff=scale)
                power_paths[scale][i] = model_path
                i += 1

        return levy_paths

'''
class fBmsims:
    def __init__(self, obj = 100, length = 100):
        self.fbm_paths = self.fbm_sim(obj, length)

    def fractal_brownian( self, N, T, H = 0.5, origin = (0,0) ):
        if H > 1 or H < 0:
            return None

        r = np.zeros((n + 1, 1))
        r[0] = 1
        for i in range(1,n):
            r[i] = 0.5 * ( (i+1)**(2*H) - (2*i)**(2*H) + (i-1)**(2*H))
            r =
'''
#---------------------------
# Export Simulated Data
#---------------------------
'''
rws = RWSims(obj = 1000, length = 100)
lfs = LevySims(obj = 1000, length = 100)

for sim in [rws, lfs]:
    cp = CellPaths(cell_ids = rws)
    gf = GeneralFeatures(cell_ids = cp.cell_ids)
    msdf = MSDFeatures(cell_ids = cp.cell_ids)
    rwf = RWFeatures(cell_ids = cp.cell_ids, gf = gf)

    ind_outputs = single_outputs_list(cp.cell_ids, gf = gf, rwf = rwf, msdf = msdf, 'sim_output')
    diff_kurtosis_array = dictofdict2array(rwf.diff_kurtosis)
    avg_moving_speed_array = dictofdict2array( gf.avg_moving_speed )
    time_moving_array = dictofdict2array( gf.time_moving )
    turn_list = tripledict2array(gf.turn_stats)
    theta_list = tripledict2array(gf.theta_stats)
    merged_list = merge_flat_lists([ind_outputs, diff_kurtosis_array, avg_moving_speed_array, time_moving_array, turn_list, theta_list])
'''
