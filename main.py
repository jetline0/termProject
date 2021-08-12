from cmu_112_graphics import *
import random
from UI import *
from Canvas import * # File functions, File Class
from Drawing import *
from Colorpicker import *

def appStarted(app):
    app.mouseMovedDelay = 1
    app.timerDelay = 2000
    # current tool is app.optionSelected
    UI.initializeUIVariables(app)
    UI.initializeMenus(app)
    AppCanvas.initializeFiles(app)
    Drawing.initializeDrawingVariables(app)
    Colorpicker.initializeColorpicker(app)
    app.mode = "drawingMode"

def drawingMode_mouseMoved(app, event):
    app.mouseX, app.mouseY = event.x, event.y

def drawingMode_keyPressed(app, event):
    if event.key == "R":
        appStarted(app)
    # Change file
    if event.key == "Up":
        app.currentFile -= 1
        if app.currentFile < 0:
            app.currentFile = 0
    if event.key == "Down":
        app.currentFile += 1
        if app.currentFile == len(app.files):
            app.currentFile -= 1
    if event.key == "c":
        app.currentColor = random.choice([(0,255,0), (0,0,255), (255,0,255)])

def drawingMode_mousePressed(app, event):
    app.selectedMenu = UI.menuClicked(app, event.x, event.y)
    if app.selectedMenu == app.canvasContainer:
        if not Drawing.isValidCoord(app, *Drawing.toFileCoords(app, event.x, event.y)):
            return
        Drawing.createImgDraw(app)
        Drawing.setPrevCoords(app, event)
        Drawing.preUseTool(app, event, app.optionSelected)
    else:
        if app.selectedMenu == app.sideBar:
            if app.sideBar.currentColorClicked(app, event):
                app.mode = "colorpickerMode"
            app.sideBar.fileRectangleClicked(app, event)
        app.selectedMenu.changeOption(app, event.x, event.y)

def drawingMode_mouseDragged(app, event):
    app.mouseX, app.mouseY = event.x, event.y
    if app.selectedMenu != app.canvasContainer: # you are NOT dragging in the right place 
        return
    if not Drawing.isValidCoord(app, *Drawing.toFileCoords(app, event.x, event.y)):
        return
    if app.ImageDraw != None:
        Drawing.useTool(app, event, app.optionSelected)

def drawingMode_mouseReleased(app, event):
    del app.ImageDraw 
    app.ImageDraw = None

def drawingMode_redrawAll(app, canvas):
    UI.drawCanvasContainer(app, canvas)
    AppCanvas.drawCurrentFile(app, canvas)
    UI.drawTopAndSideBar(app, canvas)
    Drawing.drawCursor(app, canvas)

def drawingMode_sizeChanged(app):
    UI.initializeUIVariables(app)
    UI.initializeMenus(app)

#########################################################
# colorpicker mode - activated when the option is pressed
#########################################################

def colorpickerMode_keyPressed(app, event):
    if event.key == "b":
        app.mode = "drawingMode"

def colorpickerMode_redrawAll(app, canvas):
    # canvas.create_rectangle(0,0,app.width,app.height, fill="gainsboro")
    # canvas.create_text(app.width / 2, app.height / 3,
    #                     text="press b to return to the canvas")
    Colorpicker.drawSquare(app, canvas)
    Colorpicker.drawBar(app, canvas)

def colorpickerMode_mousePressed(app, event):
    Colorpicker.handleClick(app, event)

runApp(width = 1000, height = 500)
