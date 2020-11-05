import matplotlib.pyplot as plt
import math
import util


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def main():
    # Surface area formulas obtained from https://mathworld.wolfram.com/topics/SurfacesofRevolution.html
    args = util.args
    for idx, x in enumerate(args):
        args[idx] = dotdict(x)
    X_ALL = []
    Y_ALL = []
    ALL_beta = list()
    ALL_altitude = list()
    for arg in args:
        frontal_area = 0
        Cd = 1.0
        if arg.csection == 'sphere':
            frontal_area = math.pi * arg.radius**2 / 4
            Cd = 0.42
        elif arg.csection == 'paraboloid':
            # Cd equation is found at http://aerodesign.stanford.edu/aircraftdesign/drag/volumedrag.html
            frontal_area = (math.pi * arg.radius) / (6 * arg.height**2) * \
                ((arg.radius**2 + 4*arg.height**2)**(3/2) - arg.radius**3)
            Cd = 10.67/(arg.height/arg.radius * 2)**2
        elif arg.csection == 'elipsoid':
            frontal_area = math.pi * arg.radius**2 / 4
            Cd = 0.13
        elif arg.csection == 'cone':
            frontal_area = math.pi * arg.radius * \
                math.sqrt(arg.radius**2 + arg.height**2)
            Cd = 0.50
        elif arg.csection == 'cube':
            frontal_area = arg.width**2
            Cd = 1.02

        # Physical constants
        g = arg.g
        m = arg.mass
        rho = arg.density
        A = frontal_area
        ALL_alpha = list()
        beta = []
        altitude = []
        Vx0 = arg.starting_velocity
        Vy0 = arg.starting_velocity
        # Calculate air density based off of https://www.grc.nasa.gov/WWW/K-12/rocket/atmos.html START
        for h in range(1, 35000):
            T = 59 - .00356 * h
            p = 2116 * math.pow(((T + 459.7) / 518.6), 5.256)
            r = p / (1718 * (T + 459.7))
            r = r * 515.378818
            alpha = r * Cd * A / 2.0 * math.pow(arg.starting_velocity, 2)
            beta.append(alpha / m * 100)
            altitude.append(h)
        # Calculate air density END
        ALL_beta.append(beta)
        ALL_altitude.append(altitude)

        # FALCON 9 START

    # BOEING 737-900 START
    plt.plot(ALL_altitude[9], ALL_beta[9], label="Sphere")
    plt.plot(ALL_altitude[12], ALL_beta[12], label="Paraboloid")
    plt.plot(ALL_altitude[15], ALL_beta[15], label="Ellipsoid")
    axes = plt.gca()
    width = axes.get_xlim()
    height = axes.get_ylim()
    plt.text(width[1] * 1.25 - width[1]/1.5, height[1] - 5.5 * height[1] / 13,
             "Velocity = " + str(arg.starting_velocity) + " m/s", fontsize=9)
    plt.legend(bbox_to_anchor=(.85, .85))
    plt.xlabel('Altitude (ft.)', fontsize=12)
    plt.ylabel('Drag Force (N)', fontsize=12)
    plt.title("Boeing 737-900 Model with Surfaces of Revolution")
    plt.savefig('Drag Force vs Altitude Earth.png')
    plt.clf()
    # BOEING 737-900 END


if __name__ == '__main__':
    main()
