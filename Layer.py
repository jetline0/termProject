from cmu_112_graphics import *

class Layer:
    # when displaying the image, display it like normal. have putalpha handle
    # the image's transparency will be modified
    def drawLayers(app, canvas):
        layers = app.layers
        for layer in layers:
            # 0,0 will be top left corner of layers
            canvas.create_image(0,0, anchor="nw", pilImage=(layer.image))



# A Layer object is just a wrapper for one Image object

class LayerObj(object):
    def __init__(self, app, pos):
        self.pos = pos
        self.fill = None
        if pos == 0:
            self.fill = (0, 0, 0, 255)
        self.image = Image.new("RGBA", (app.canvasWidth, app.canvasHeight), self.fill)