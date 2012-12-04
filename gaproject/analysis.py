
"Module to analyze the result we've got. Eg: plot it."


def plot(individual, data):
    "Uses Matplotib to plot the nodes positions."

    positions = [data.positions[i] for i in individual]

    import matplotlib.pyplot as plt

    x_axis = [pos[0] for pos in positions]
    y_axis = [pos[1] for pos in positions]

    plt.plot(x_axis, y_axis, 'ro-')
    plt.show()
