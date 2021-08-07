from cmu_112_graphics import *
from Layer import *
from UI import *

def appStarted(app):
    # size of every layer
    app.canvasWidth = 700
    app.canvasHeight = 300
    # start off with 3 layers
    app.layers = [LayerObj(app, pos) for pos in range(3)]
    app.currentLayer = 1 # 0 is background, 1 goes up

    # debugging
    draw = ImageDraw.Draw(app.layers[1].image)
    draw.line((0, 0, app.canvasWidth, app.canvasHeight), width=10, fill=(255, 0, 0, 255))
    draw.line((0, app.canvasHeight, app.canvasWidth, 0), width=10, fill=(0, 0, 255, 25))

def redrawAll(app, canvas):
    UI.drawLayerControl(app, canvas)
    Layer.drawLayers(app, canvas)

def keyPressed(app, event):
    # Change layer
    if event.key == "0":
        app.currentLayer = 0
    if event.key == "1":
        app.currentLayer = 1
    if event.key == "2":
        app.currentLayer = 2
    # Change transparency
    if event.key == "Down":
        layer = app.layers[app.currentLayer].image
        alpha = layer.split()[-1]
        print(alpha)
        layer.putalpha(alpha)
    if event.key == "Up":
        layer = app.layers[app.currentLayer].image
        alpha = layer.split()[-1]
        layer.putalpha(alpha + 50)

def main():
    runApp(width = 800, height = 500)

if __name__ == "__main__":
    main()