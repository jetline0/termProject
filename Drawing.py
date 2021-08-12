from cmu_112_graphics import *
from Canvas import *
from UI import *

stacks = []
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

    def isValidCoord(app, x, y):
        width, height = AppCanvas.getDimensions(app)
        return (0 <= x < width) and (0 <= y < height) 

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
    
    def preFill(app, event, replaceColor):
        # click coords on the canvas
        x, y = Drawing.toFileCoords(app, event.x, event.y)
        # Color to replace
        findColor = app.Image.getpixel((x,y))
        # turn the pixel color values of an image to a list
        # source: https://stackoverflow.com/questions/1109422/getting-list-of-pixel-values-from-pil
        pixels = list(app.Image.getdata())
        width, height = app.Image.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        Drawing.floodfill(pixels, y, x, findColor, replaceColor)
        data = Drawing.flatten(pixels)
        app.Image.putdata(data)

    def floodfill(L, startrow, startcol, toBeReplaced, replaceColor):
        # is the cell ur looking at the toBeReplacedColor?
        # base case, if it is, fill it in, check
        if L[startrow][startcol] == toBeReplaced:
            stacks.append((startrow, startcol))
        while len(stacks) > 0:
            stackMember = stacks.pop()
            L[stackMember[0]][stackMember[1]] = replaceColor
            stacks.extend(Drawing.findValidNeighbors(L, stackMember[0], stackMember[1], toBeReplaced))

    # fill helper functions
    # taken from https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
    def flatten(t):
        return [item for sublist in t for item in sublist]
    
    def findValidNeighbors(L, startrow, startcol, toBeReplaced):
        rows = len(L)
        cols = len(L[0])
        validNeighbors = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for drow, dcol in directions:
            if (0 <= startrow  + drow < rows and 0 <= startcol + dcol < cols and
                L[startrow + drow][startcol+ dcol] == toBeReplaced):
                validNeighbors.append((startrow + drow, startcol + dcol))
        return validNeighbors


    def eyedropper(app, event):
        # print(f"original color: {app.currentColor}")
        app.currentColor = app.Image.getpixel(Drawing.toFileCoords(app, event.x, event.y))
        # print(f"new color: {app.currentColor}")

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
            Drawing.preFill(app, event, app.currentColor)
        elif tool == "eyedropper":
            Drawing.eyedropper(app, event)
        # Pretty important for lines
        Drawing.setPrevCoords(app, event)

    def useTool(app, event, tool):
        if tool == "fill" or tool == "eyedropper":
            return
        Drawing.preUseTool(app, event, tool)
