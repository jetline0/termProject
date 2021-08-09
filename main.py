from cmu_112_graphics import *
from Canvas import * # Layer functions, LayerObj Class
from UI import *

def appStarted(app):
    # app.timerDelay = 1
    app.mouseMovedDelay = 1
    UI.initializeUIVariables(app)
    AppCanvas.initializeLayers(app)
    # current tool
    app.currentTool = "brush" # can be eraser
    app.draw = None
    app.currentColor = (0,0,255,255)

import random
def keyPressed(app, event):
    if event.key == "r":
        appStarted(app)
    # Change layer
    if event.key == "0":
        app.currentLayer = 0
    if event.key == "1":
        app.currentLayer = 1
    if event.key == "2":
        app.currentLayer = 2
    if event.key == "c":
        app.currentColor = random.choice(["green", "black", "purple"])
    if event.key == "e":
        app.currentTool = "eraser"
    if event.key == "b":
        app.currentTool = "brush"

def mousePressed(app, event):
    print(UI.menuClicked(app, event.x, event.y))
    # only set app.draw to something if u click on canvasContainer
    if UI.menuClicked(app, event.x, event.y) == app.canvasContainer:
        toModify = app.layers[app.currentLayer].image
        app.draw = ImageDraw.Draw(toModify)
    else:
        print("heehee not implemented yet")

def mouseDragged(app, event):
    # HUGE PROBLEM: CIRCLES ARE NOT BEING DRAWN FREQUENTLY ENOUGH
    print(event.x, event.y)
    if app.currentTool == "brush":
        app.draw.ellipse((event.x - app.canvasX - 5,
                            event.y - app.canvasY - 5,
                            event.x - app.canvasX + 5,
                            event.y - app.canvasY + 5), fill=app.currentColor)
    if app.currentTool == "eraser":
        app.draw.ellipse((event.x - app.canvasX - 5,
                    event.y - app.canvasY - 5,
                    event.x - app.canvasX + 5,
                    event.y - app.canvasY + 5), fill=(255,255,255,0))

def mouseReleased(app, event):
    del app.draw
    app.draw = None

def redrawAll(app, canvas):
    UI.drawCanvasContainer(app, canvas)
    AppCanvas.drawLayers(app, canvas)
    UI.drawTopAndSideBar(app, canvas)
    canvas.create_text(app.width, 0, text=f"Current Layer: {app.currentLayer}  ", anchor="ne")



def main():
    runApp(width = 800, height = 500)

if __name__ == "__main__":
    main()