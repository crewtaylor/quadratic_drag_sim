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

        alpha = rho * Cd * A / 2.0 * math.pow(arg.starting_velocity, 2)
        beta = alpha / m

        # FALCON 9 START

        # Initial conditions
        X0 = 1.0
        Y0 = 0.0
        Vx0 = arg.starting_velocity
        Vy0 = arg.starting_velocity

        # Time steps
        steps = 1000
        t_HIT = 2.0*Vy0/g
        dt = t_HIT / steps

        # No drag
        X_ND = list()
        Y_ND = list()

        for i in range(steps+1):
            X_ND.append(X0 + Vx0 * dt * i)
            Y_ND.append(Y0 + Vy0 * dt * i - 0.5 * g * pow(dt * i, 2.0))

        # With drag
        X_WD = list()
        Y_WD = list()
        Vx_WD = list()
        Vy_WD = list()

        for i in range(steps+1):
            X_ND.append(X0 + Vx0 * dt * i)
            Y_ND.append(Y0 + Vy0 * dt * i - 0.5 * g * pow(dt * i, 2.0))

        # With drag
        X_WD = list()
        Y_WD = list()
        Vx_WD = list()
        Vy_WD = list()

        X_WD.append(X0)
        Y_WD.append(Y0)
        Vx_WD.append(Vx0)
        Vy_WD.append(Vy0)

        stop = 0
        for i in range(1, steps+1):
            if stop != 1:
                speed = pow(pow(Vx_WD[i-1], 2.0)+pow(Vy_WD[i-1], 2.0), 0.5)

                # First calculate velocity
                Vx_WD.append(Vx_WD[i-1] * (1.0 - beta * speed * dt))
                Vy_WD.append(
                    Vy_WD[i-1] + (- g - beta * Vy_WD[i-1] * speed) * dt)

                # Now calculate position
                X_WD.append(X_WD[i-1] + Vx_WD[i-1] * dt)
                Y_WD.append(Y_WD[i-1] + Vy_WD[i-1] * dt)
                # Stop if hits ground
                if Y_WD[i] <= 0.0:
                    stop = 1
        # Plot results
        X_ALL.append(X_WD)
        Y_ALL.append(Y_WD)
        plt.plot(X_ND, Y_ND, label="No Drag")
        plt.plot(X_WD, Y_WD, label="With Drag")
        plt.legend(bbox_to_anchor=(1.0, .5))
        axes = plt.gca()
        width = axes.get_xlim()
        height = axes.get_ylim()
        plt.xlim([0, width[1] * 1.5])
        plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - height[1] / 13,
                 str(arg.notes), fontsize=12)
        plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - 2 *
                 height[1] / 13, "Shape = " + arg.csection, fontsize=9)
        plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - 3 *
                 height[1] / 13, "Mass = " + str(arg.mass) + " kg", fontsize=9)
        plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - 4 * height[1] /
                 13, "Fluid Density = " + str(arg.density) + "kg/m^3", fontsize=9)
        plt.text(width[1] * 1.5 - width[1]/1.5, height[1] - 5 * height[1] / 13,
                 "Initial Velocity = " + str(arg.starting_velocity) + " m/s", fontsize=9)
        plt.xlabel('X', fontsize=12)
        plt.ylabel('Y', fontsize=12)
        plt.savefig(arg.notes + '.png')
        plt.clf()
        # FALCON 9 END


if __name__ == '__main__':
    main()
