from cmu_112_graphics import *
from Canvas import * # Layer functions, LayerObj Class
from UI import *

def appStarted(app):
    app.mouseMovedDelay = 1
    UI.initializeUIVariables(app)
    AppCanvas.initializeLayers(app)
    # current tool is app.topBar.optionSelected
    app.brushSize = 5
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

def mousePressed(app, event):
    selectedMenu = UI.menuClicked(app, event.x, event.y)
    print(selectedMenu)
    # only set app.draw to something if u click on canvasContainer
    if selectedMenu == app.canvasContainer:
        toModify = app.layers[app.currentLayer].image
        app.draw = ImageDraw.Draw(toModify)
    elif selectedMenu == app.topBar:
        # Find out if the selection was valid
        app.topBar.changeOption(app, event.x, event.y)
        print("heehee not implemented yet")

def mouseDragged(app, event):
    if app.draw == None:
        return
    if app.topBar.optionSelected == "brush":
        app.draw.ellipse((event.x - app.canvasX - app.brushSize,
                            event.y - app.canvasY - app.brushSize,
                            event.x - app.canvasX + app.brushSize,
                            event.y - app.canvasY + app.brushSize), fill=app.currentColor)
        pass
    if app.topBar.optionSelected == "eraser":
        app.draw.ellipse((event.x - app.canvasX - app.brushSize,
                    event.y - app.canvasY - app.brushSize,
                    event.x - app.canvasX + app.brushSize,
                    event.y - app.canvasY + app.brushSize), fill=(255,255,255,0))

def mouseReleased(app, event):
    del app.draw
    app.draw = None

def redrawAll(app, canvas):
    UI.drawCanvasContainer(app, canvas)
    AppCanvas.drawLayers(app, canvas)
    UI.drawTopAndSideBar(app, canvas)
    canvas.create_text(app.width, 0, text=f"Current Layer: {app.currentLayer} ",
                    anchor="ne")

def main():
    runApp(width = 800, height = 500)

if __name__ == "__main__":
    main()