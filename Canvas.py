from cmu_112_graphics import *

class AppCanvas:
    # when displaying the image, display it like normal. have putalpha handle
    # the image's transparency will be modified
    def initializeLayers(app):
        app.canvasWidth = 500
        app.canvasHeight = 300
        app.canvasX = 40
        app.canvasY = 80
        app.layers = [Layer(app, pos) for pos in range(3)]
        app.currentLayer = 1 # 0 is background, 1 goes up

    def drawLayers(app, canvas):
        layers = app.layers
        for layer in layers:
            # app.canvasX,app.canvasY will be top left corner of layers
            canvas.create_image(app.canvasX,app.canvasY, 
                    anchor="nw", pilImage=(layer.image))

# A Layer object is just a wrapper for one Image object
class Layer(object):
    def __init__(self, app, pos):
        self.pos = pos
        self.fill = None
        if pos == 0:
            self.fill = (255, 255, 255, 255)
        self.image = Image.new("RGBA", (app.canvasWidth, app.canvasHeight), self.fill)