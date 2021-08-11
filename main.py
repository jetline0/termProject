from cmu_112_graphics import *
import random
from Canvas import * # File functions, File Class
from UI import *
from Drawing import *

def appStarted(app):
    app.mouseMovedDelay = 1
    app.timerDelay = 2000
    # current tool is app.topBar.optionSelected
    UI.initializeUIVariables(app)
    AppCanvas.initializeFiles(app)
    Drawing.initializeDrawingVariables(app)

def keyPressed(app, event):
    if event.key == "r":
        appStarted(app)
    # Change file
    if event.key == "Up":
        app.currentFile += 1
        if app.currentFile == len(app.files):
            app.currentFile -= 1
    if event.key == "Down":
        app.currentFile -= 1
        if app.currentFile < 0:
            app.currentFile = 0
    if event.key == "c":
        app.currentColor = random.choice([(0,255,0), (0,0,255), (255,0,255)])

def mousePressed(app, event):
    app.selectedMenu = UI.menuClicked(app, event.x, event.y)
    if app.selectedMenu == app.canvasContainer:
        Drawing.createImgDraw(app)
        Drawing.setPrev(app, event)
        Drawing.preUseTool(app, event, app.topBar.optionSelected)
    else:
        app.selectedMenu.changeOption(app, event.x, event.y)

def mouseDragged(app, event):
    if app.selectedMenu != app.canvasContainer: # you are NOT dragging in the right place 
        return
    Drawing.useTool(app, event, app.topBar.optionSelected)

def mouseReleased(app, event):
    del app.ImageDraw 
    app.ImageDraw = None

def redrawAll(app, canvas):
    UI.drawCanvasContainer(app, canvas)
    AppCanvas.drawFile(app, canvas)
    UI.drawTopAndSideBar(app, canvas)
    Drawing.drawCursorVisualization(app, canvas)
    canvas.create_text(app.width, 0, text=f"Current File: {app.currentFile} ",
                    anchor="ne")

runApp(width = 800, height = 500)
