from cmu_112_graphics import *
from Canvas import *

class Drawing:
    def initializeDrawingVariables(app):
        app.brushSize = 5
        app.ImageDraw = None
        app.currentColor = (0,0,0)
        app.prevx = None
        app.prevy = None

    def toFileCoords(app, x, y):
        return (x - app.canvasX, y - app.canvasY)

    def drawCursorVisualization(app, canvas):
        pass

    # Physical drawing functions
    def drawstroke(app, event, color):
        # took inspiration from https://stackoverflow.com/questions/45172116/fix-pil-imagedraw-draw-line-with-wide-lines
        app.ImageDraw.line(Drawing.toFileCoords(app, app.prevx, app.prevy) + 
                            Drawing.toFileCoords(app, event.x, event.y),
                            fill = color,
                            width = app.brushSize)
        app.ImageDraw.ellipse((event.x - app.canvasX - app.brushSize/2.5,
                            event.y - app.canvasY - app.brushSize/2.5,
                            event.x - app.canvasX + app.brushSize/2.5,
                            event.y - app.canvasY + app.brushSize/2.5),
                            fill = color)

    def isValidCoord(app, x, y):
        width, height = AppCanvas.getDimensions(app)
        return (0 <= x < width) and (0 <= y < height) 


    def findBorder(app, dir, findcolor, startx, starty):
        directions = ["up", "down", "left", "right"]
        delta = [(0,-1), (0,1), (-1,0), (1,0)]
        dx, dy = delta[directions.index(dir)]
        newx, newy = startx + dx, starty + dy 
        while Drawing.isValidCoord(app, newx, newy): #and valid bounds:
            # get color at (newx, newy)
            foundcolor = app.Image.getpixel((newx, newy))
            # if that color isn't equal to findcolor, return (newx - dx, newy - dy)
            if foundcolor != findcolor:
                return (newx - dx, newy - dy)
            # increment newx and newy by dx and dy
            newx += dx
            newy += dy
        return newx - dx, newy - dy



    def fill(app, event, color):
        tofill = []
        clickCoordinates = Drawing.toFileCoords(app, event.x, event.y)
        findColor = app.Image.getpixel(clickCoordinates)
        catch, topy = Drawing.findBorder(app, "up", findColor, clickCoordinates[0], clickCoordinates[1])
        catch, bottomy = Drawing.findBorder(app, "down", findColor, clickCoordinates[0], clickCoordinates[1])
        for yval in range(topy, bottomy+1):
            leftx, catch = Drawing.findBorder(app, "left", findColor, clickCoordinates[0], yval)
            rightx, catch = Drawing.findBorder(app, "right", findColor, clickCoordinates[0], yval)
            domain = [(x, yval) for x in range(leftx, rightx + 1)]
            tofill.extend(domain)
        for coord in tofill:
            app.Image.putpixel(coord, color)



    # Events that happen before mouseDragged -- called by mousePressed(app, event)
    # Creates the ImageDraw object of the current File
    def createImgDraw(app):
        app.Image = app.files[app.currentFile].image
        app.ImageDraw = ImageDraw.Draw(app.Image)

    def setPrev(app, event):
        app.prevx = event.x
        app.prevy = event.y

    # Actually what gets called in the mouseDragged function, just many times
    def preUseTool(app, event, tool):
        if tool == "brush":
            Drawing.drawstroke(app, event, app.currentColor)
        elif tool == "eraser":
            Drawing.drawstroke(app, event, (255,255,255))
        elif tool == "fill":
            Drawing.fill(app, event, app.currentColor)
            # ImageDraw.floodfill(app.Image,
            #                     Drawing.toFileCoords(app, event.x, event.y), 
            #                     app.currentColor)
        # Pretty important for lines
        Drawing.setPrev(app, event)

    def useTool(app, event, tool):
        if tool == "fill":
            return
        Drawing.preUseTool(app, event, tool)
