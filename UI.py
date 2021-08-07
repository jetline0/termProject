from cmu_112_graphics import *

class UI:
    def drawLayerControl(app, canvas):
        canvas.create_text(app.width, 0, text=f"Current Layer: {app.currentLayer}  ", anchor="ne")
