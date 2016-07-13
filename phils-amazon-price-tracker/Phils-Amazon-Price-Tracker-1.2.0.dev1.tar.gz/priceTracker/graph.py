import plotly.plotly as py
import plotly.graph_objs as go
from PIL import Image
import datetime
def graph(e,w,s,stars,path,pri):
    # Generate the figure
    x = []
    y=[]
    print("starting to search for matching entries: "+ str(len(pri.productList)))
    for i in range(len(pri.productList)):
        if str(pri.productList[i].title) == e:
            try:
                x.append(pri.productList[i].Time)
                y.append(float(pri.productList[i].price))
            except ValueError:
                pass
    x.append(str(datetime.datetime.now()))
    y.append(y[-1])
    data = [
        go.Scatter(
            x=x,
            y=y,
            text=y,
            textposition="top",
            mode='lines+markers+text',
    name='Lines, Markers and Text',
    textfont=dict(
        family='sans serif',
        size=15,
        color='black'
    )
    )]
    layout = go.Layout(
        title='Price Tracker of: ' + e[0:30] + "<br>" + s + "<br>" + stars + " in: " + path,
        yaxis=dict(
            title='Price in ' + w
    ),
    xaxis=dict(
    title="Time"
    ))
    fig = go.Figure(data=data,layout=layout)
    if e[0] == " ":
        e=e[1:]
    filen = ("" + pri.outputfile + "/" + path + "/" + e[0:20] + ".png").replace(" ", "_")
    py.image.save_as(fig, filen)
pass
def openImage(filen):
    img = Image.open(filen)
    img.show()
    print("opened chart: " + filen)
pass
