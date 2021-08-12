from cmu_112_graphics import *
from Canvas import *
from UI import *

class Drawing:
    def initializeDrawingVariables(app):
        app.brushSize = 5
        app.optionSelected = "brush"
        app.ImageDraw = None
        app.currentColor = (0,0,0)
        app.prevx = None
        app.prevy = None

    def toFileCoords(app, x, y):        
        return (x - app.canvasX, y - app.canvasY)

    # Draw when the cursor location is in the canvasContainer 
    def drawCursor(app, canvas):
        if not Drawing.isValidCoord(app, *Drawing.toFileCoords(app, app.mouseX, app.mouseY)):
            return
        if UI.menuClicked(app, app.mouseX, app.mouseY) != app.canvasContainer:
            return
        if app.optionSelected == "brush" or app.optionSelected == "eraser":
            cursorSize = app.brushSize/2.5
            canvas.create_oval(app.mouseX - cursorSize, app.mouseY - cursorSize,
                            app.mouseX + cursorSize, app.mouseY + cursorSize,
                            outline = "gray60")
        # Paint bucket sprite comes from MSPaint
        if app.optionSelected == "fill":
            sprite = Image.open("icons/paintbucket.png")
            sprite = sprite.resize((10,10))
            canvas.create_image(app.mouseX, app.mouseY, image=ImageTk.PhotoImage(sprite))

    # Physical drawing functions
    def drawStroke(app, event, color):
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
    
    def fill(app, event, color):
        tofill = []
        clickx, clicky = Drawing.toFileCoords(app, event.x, event.y)
        findColor = app.Image.getpixel((clickx,clicky))
        catch, topy = Drawing.findBorder(app, "up", findColor, clickx, clicky)
        catch, bottomy = Drawing.findBorder(app, "down", findColor, clickx, clicky)
        for yval in range(topy, bottomy+1):
            leftx, catch = Drawing.findBorder(app, "left", findColor, clickx, yval)
            rightx, catch = Drawing.findBorder(app, "right", findColor, clickx, yval)
            domain = [(x, yval) for x in range(leftx, rightx + 1)]
            tofill.extend(domain)
        for coord in tofill:
            app.Image.putpixel(coord, color)

    # fill helper functions
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

    def eyedropper(app, event):
        print(f"original color: {app.currentColor}")
        app.currentColor = app.Image.getpixel(Drawing.toFileCoords(app, event.x, event.y))
        print(f"new color: {app.currentColor}")

    # Events that happen before mouseDragged -- called by mousePressed(app, event)
    # Creates the ImageDraw object of the current File
    def createImgDraw(app):
        app.Image = app.files[app.currentFile].image
        app.ImageDraw = ImageDraw.Draw(app.Image)

    def setPrevCoords(app, event):
        app.prevx = event.x
        app.prevy = event.y

    # Actually what gets called in the mouseDragged function, just many times
    def preUseTool(app, event, tool):
        if tool == "brush":
            Drawing.drawStroke(app, event, app.currentColor)
        elif tool == "eraser":
            Drawing.drawStroke(app, event, (255,255,255))
        elif tool == "fill":
            Drawing.fill(app, event, app.currentColor)
        elif tool == "eyedropper":
            Drawing.eyedropper(app, event)
        # Pretty important for lines
        Drawing.setPrevCoords(app, event)

    def useTool(app, event, tool):
        if tool == "fill" or tool == "eyedropper":
            return
        Drawing.preUseTool(app, event, tool)
