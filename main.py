from cmu_112_graphics import *
import random
from Canvas import * # File functions, File Class
from UI import *
from Drawing import *

def appStarted(app):
    app.mouseMovedDelay = 1
    app.timerDelay = 2000
    # current tool is app.optionSelected
    UI.initializeUIVariables(app)
    UI.initializeMenus(app)
    AppCanvas.initializeFiles(app)
    Drawing.initializeDrawingVariables(app)

def mouseMoved(app, event):
    app.mouseX, app.mouseY = event.x, event.y

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
        if not Drawing.isValidCoord(app, *Drawing.toFileCoords(app, event.x, event.y)):
            return
        Drawing.createImgDraw(app)
        Drawing.setPrevCoords(app, event)
        Drawing.preUseTool(app, event, app.optionSelected)
    else:
        app.selectedMenu.changeOption(app, event.x, event.y)

def mouseDragged(app, event):
    app.mouseX, app.mouseY = event.x, event.y
    if app.selectedMenu != app.canvasContainer: # you are NOT dragging in the right place 
        return
    if not Drawing.isValidCoord(app, *Drawing.toFileCoords(app, event.x, event.y)):
        return
    if app.ImageDraw != None:
        Drawing.useTool(app, event, app.optionSelected)

def mouseReleased(app, event):
    del app.ImageDraw 
    app.ImageDraw = None

def redrawAll(app, canvas):
    UI.drawCanvasContainer(app, canvas)
    AppCanvas.drawCurrentFile(app, canvas)
    UI.drawTopAndSideBar(app, canvas)
    Drawing.drawCursor(app, canvas)
    canvas.create_text(app.width, 100, text=f"Current File: {app.currentFile} ",
                    anchor="ne")

def sizeChanged(app):
    UI.initializeUIVariables(app)
    UI.initializeMenus(app)



runApp(width = 800, height = 500)
