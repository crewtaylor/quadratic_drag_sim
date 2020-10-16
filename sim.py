import matplotlib.pyplot as plt
import math
import scipy.integrate as integrate
from past.builtins import xrange


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def main():
    # Surface area formulas obtained from https://mathworld.wolfram.com/topics/SurfacesofRevolution.html
    args = []
    args = [
        {
            "csection": "sphere",
            "radius": 1.75,
            "mass": 549054,
            "density": 1.274,
            "starting_velocity": 1000,
            "notes": "Earth Falcon 9 Sphere",
            "g": 9.8

        },
        {
            "csection": "sphere",
            "radius": 1.75,
            "mass": 549054,
            "density": .02,
            "starting_velocity": 1000,
            "notes": "Mars Falcon 9 Sphere",
            "g": 3.7

        },
        {
            "csection": "sphere",
            "radius": 1.75,
            "mass": 549054,
            "density": 65,
            "starting_velocity": 1000,
            "notes": "Venus Falcon 9 Sphere",
            "g": 8.9
        },
        {
            "csection": "paraboloid",
            "radius": 1.75,
            "height": 70,
            "mass": 549054,
            "density": 1.274,
            "starting_velocity": 1000,
            "notes": "Earth Falcon 9 Paraboloid",
            "g": 9.8

        },
        {
            "csection": "paraboloid",
            "radius": 1.75,
            "height": 70,
            "mass": 549054,
            "density": .02,
            "starting_velocity": 1000,
            "notes": "Mars Falcon 9 Paraboloid",
            "g": 3.7

        },
        {
            "csection": "paraboloid",
            "radius": 1.75,
            "height": 70,
            "mass": 549054,
            "density": 65,
            "starting_velocity": 1000,
            "notes": "Venus Falcon 9 Paraboloid",
            "g": 8.9
        },
        {
            "csection": "elipsoid",
            "radius": 1.75,
            "mass": 549054,
            "density": 1.274,
            "starting_velocity": 1000,
            "notes": "Earth Falcon 9 Elipsoid",
            "g": 9.8

        },
        {
            "csection": "elipsoid",
            "radius": 1.75,
            "mass": 549054,
            "density": .02,
            "starting_velocity": 1000,
            "notes": "Mars Falcon 9 Elipsoid",
            "g": 3.7

        },
        {
            "csection": "elipsoid",
            "radius": 1.75,
            "mass": 549054,
            "density": 65,
            "starting_velocity": 1000,
            "notes": "Venus Falcon 9 Elipsoid",
            "g": 8.9
        },
        {
            "csection": "sphere",
            "radius": 3.75,
            "mass": 50000,
            "density": 1.274,
            "starting_velocity": 200,
            "notes": "Sea Level Boeing 737-900 Sphere",
            "g": 9.807

        },
        {
            "csection": "sphere",
            "radius": 3.75,
            "mass": 50000,
            "density": .7364,
            "starting_velocity": 200,
            "notes": "5000 m Boeing 737-900 Sphere",
            "g": 9.791

        },
        {
            "csection": "sphere",
            "radius": 3.75,
            "mass": 50000,
            "density": .4135,
            "starting_velocity": 200,
            "notes": "2000 m Boeing 737-900 Sphere",
            "g": 9.776
        },
        {
            "csection": "paraboloid",
            "radius": 3.75,
            "height": 40,
            "mass": 50000,
            "density": 1.274,
            "starting_velocity": 200,
            "notes": "Sea Level Boeing 737-900 Paraboloid",
            "g": 9.807

        },
        {
            "csection": "paraboloid",
            "radius": 3.75,
            "height": 40,
            "mass": 50000,
            "density": .7364,
            "starting_velocity": 200,
            "notes": "5000 m Boeing 737-900 Paraboloid",
            "g": 9.791

        },
        {
            "csection": "paraboloid",
            "radius": 3.75,
            "height": 40,
            "mass": 50000,
            "density": .4135,
            "starting_velocity": 200,
            "notes": "2000 m Boeing 737-900 Paraboloid",
            "g": 9.776
        },
        {
            "csection": "elipsoid",
            "radius": 3.75,
            "mass": 50000,
            "density": 1.274,
            "starting_velocity": 200,
            "notes": "Sea Level Boeing 737-900 Elipsoid",
            "g": 9.807

        },
        {
            "csection": "elipsoid",
            "radius": 3.75,
            "mass": 50000,
            "density": .7364,
            "starting_velocity": 200,
            "notes": "5000 m Boeing 737-900 Elipsoid",
            "g": 9.791

        },
        {
            "csection": "elipsoid",
            "radius": 3.75,
            "mass": 50000,
            "density": .4135,
            "starting_velocity": 200,
            "notes": "10000 m Boeing 737-900 Elipsoid",
            "g": 9.776
        },
    ]
    for idx, x in enumerate(args):
        print(idx)
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
            print(alpha / m * 100)
            beta.append(alpha / m * 100)
            altitude.append(h)
        # Calculate air density END
        ALL_beta.append(beta)
        ALL_altitude.append(altitude)

        # FALCON 9 START

        # Initial conditions
        # X0 = 1.0
        # Y0 = 0.0

        # # Time steps
        # steps = 1000
        # t_HIT = 2.0*Vy0/g
        # dt = t_HIT / steps

        # # No drag
        # X_ND = list()
        # Y_ND = list()

        # for i in range(steps+1):
        #     X_ND.append(X0 + Vx0 * dt * i)
        #     Y_ND.append(Y0 + Vy0 * dt * i - 0.5 * g * pow(dt * i, 2.0))

        # # With drag
        # X_WD = list()
        # Y_WD = list()
        # Vx_WD = list()
        # Vy_WD = list()

        # for i in range(steps+1):
        #     X_ND.append(X0 + Vx0 * dt * i)
        #     Y_ND.append(Y0 + Vy0 * dt * i - 0.5 * g * pow(dt * i, 2.0))

        # # With drag
        # X_WD = list()
        # Y_WD = list()
        # Vx_WD = list()
        # Vy_WD = list()

        # X_WD.append(X0)
        # Y_WD.append(Y0)
        # Vx_WD.append(Vx0)
        # Vy_WD.append(Vy0)

        # stop = 0
        # for i in range(1, steps+1):
        #     if stop != 1:
        #         speed = pow(pow(Vx_WD[i-1], 2.0)+pow(Vy_WD[i-1], 2.0), 0.5)

        #         # First calculate velocity
        #         Vx_WD.append(Vx_WD[i-1] * (1.0 - beta * speed * dt))
        #         Vy_WD.append(
        #             Vy_WD[i-1] + (- g - beta * Vy_WD[i-1] * speed) * dt)

        #         # Now calculate position
        #         X_WD.append(X_WD[i-1] + Vx_WD[i-1] * dt)
        #         Y_WD.append(Y_WD[i-1] + Vy_WD[i-1] * dt)
        #         # Stop if hits ground
        #         if Y_WD[i] <= 0.0:
        #             stop = 1
        # # Plot results
        # X_ALL.append(X_WD)
        # Y_ALL.append(Y_WD)
        # plt.plot(X_ND, Y_ND, label="No Drag")
        # plt.plot(X_WD, Y_WD, label="With Drag")
        # plt.legend(bbox_to_anchor=(1.0, .5))
        # axes = plt.gca()
        # width = axes.get_xlim()
        # height = axes.get_ylim()
        # plt.xlim([0, width[1] * 1.5])
        # plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - height[1] / 13,
        #          str(arg.notes), fontsize=12)
        # plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - 2 *
        #          height[1] / 13, "Shape = " + arg.csection, fontsize=9)
        # plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - 3 *
        #          height[1] / 13, "Mass = " + str(arg.mass) + " kg", fontsize=9)
        # plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - 4 * height[1] /
        #          13, "Fluid Density = " + str(arg.density) + "kg/m^3", fontsize=9)
        # plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - 5 * height[1] / 13,
        #          "Initial Velocity = " + str(arg.starting_velocity) + " m/s", fontsize=9)
        # plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - 5 * height[1] / 13,
        #          "Gravitational Accel. = " + str(arg.g) + " m/s^2", fontsize=9)
        # plt.xlabel('X', fontsize=12)
        # plt.ylabel('Y', fontsize=12)
        # plt.savefig(arg.notes + '.png')
        # plt.clf()
        # FALCON 9 END

    # BOEING 737-900 START
    plt.plot(ALL_altitude[9], ALL_beta[9], label="Sphere")
    print(ALL_beta[9][-1:])
    plt.plot(ALL_altitude[12], ALL_beta[12], label="Paraboloid")
    print(ALL_beta[12][-1:])
    plt.plot(ALL_altitude[15], ALL_beta[15], label="Ellipsoid")
    print(ALL_beta[15][-1:])
    print(max(ALL_altitude[9]))
    print(max(ALL_altitude[12]))
    print(max(ALL_altitude[15]))
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
