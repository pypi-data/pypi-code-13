from bokeh.sampledata.iris import flowers
from bokeh.plotting import figure, show

colormap = {'setosa': 'orange', 'versicolor': 'blue', 'virginica': 'green'}

flowers['color'] = flowers['species'].map(lambda x: colormap[x])

p = figure(title="Iris Morphology")
p.xaxis.axis_label = "Petal Lenght"
p.yaxis.axis_label = "Petal Width"


p.circle(flowers["petal_length"], flowers["petal_width"], color=flowers["color"], fill_alpha=0.2, size=20)


