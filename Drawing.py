from cmu_112_graphics import *

class Drawing:
    def initializeDrawingVariables(app):
        app.brushSize = 5
        app.ImageDraw = None
        app.currentColor = (0,0,0)
        app.prevx = None
        app.prevy = None

    # Events that happen before mouseDragged -- called by mousePressed(app, event)
    # Creates the ImageDraw object of the current File
    def createImgDraw(app):
        app.Image = app.files[app.currentFile].image
        app.ImageDraw = ImageDraw.Draw(app.Image)

    def setPrev(app, event):
        app.prevx = event.x
        app.prevy = event.y

    def toFileCoords(app, x, y):
        # get the current file's dimensions and subtract
        return (x - app.canvasX, y - app.canvasY)

    # Actually what gets called in the mouseDragged function, just many times
    def preUseTool(app, event, tool):
        # app.currentFile = app.files[app.currentFile].image
    # The coordinates that correspond to the file itself, rather than the app
        if tool == "brush":
            # took inspiration from https://stackoverflow.com/questions/45172116/fix-pil-imagedraw-draw-line-with-wide-lines
            app.ImageDraw.line(Drawing.toFileCoords(app, app.prevx, app.prevy) + 
                                Drawing.toFileCoords(app, event.x, event.y),
                                fill = app.currentColor,
                                width = app.brushSize)
            app.ImageDraw.ellipse((event.x - app.canvasX - app.brushSize/2.5,
                                event.y - app.canvasY - app.brushSize/2.5,
                                event.x - app.canvasX + app.brushSize/2.5,
                                event.y - app.canvasY + app.brushSize/2.5),
                                fill = app.currentColor)
        elif tool == "eraser":
            app.ImageDraw.line(Drawing.toFileCoords(app, app.prevx, app.prevy) + 
                                Drawing.toFileCoords(app, event.x, event.y),
                                fill=(255,255,255),
                                width = app.brushSize)
            app.ImageDraw.ellipse((event.x - app.canvasX - app.brushSize,
                        event.y - app.canvasY - app.brushSize,
                        event.x - app.canvasX + app.brushSize,
                        event.y - app.canvasY + app.brushSize), fill=(255,255,255))
        elif tool == "fill":
            ImageDraw.floodfill(app.Image,
                                Drawing.toFileCoords(app, event.x, event.y), 
                                app.currentColor)
        Drawing.setPrev(app, event)

    def useTool(app, event, tool):
        if tool == "fill":
            return
        Drawing.preUseTool(app, event, tool)

    # tools!
    # Create a brush stroke at previous location and new location
    # def 