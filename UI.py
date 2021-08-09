from cmu_112_graphics import *

class UI:
    # Initializes the variables that change how the UI is displayed
    def initializeUIVariables(app):
        # NOTE: Not using app.varName for the dimensions of each menu because
        # they end up as app level variables  
        # Top bar's left corner is always at (0,0)
        topBarWidth = app.width
        topBarHeight = 40
        topBarX = 0
        topBarY = 0
        # Side bar's left corner is always at (app.width - app.sideBarWidth, app.topBarHeight)
        sideBarWidth = 150
        sideBarHeight = app.height - topBarHeight
        sideBarX = app.width - sideBarWidth
        sideBarY = topBarHeight
        # The canvas container's left corner is always at (0, topBarHeight)
        canvasContainerWidth = app.width - sideBarWidth
        canvasContainerHeight = app.height - topBarHeight
        canvasContainerX = 0
        canvasContainerY = topBarHeight
        # Initialize menus
        app.topBar = TopBar("topBar",
                            topBarX, topBarY,
                            topBarWidth, topBarHeight,
                            "gray64")
        app.sideBar = SideBar("sideBar",
                            sideBarX, sideBarY,
                            sideBarWidth, sideBarHeight,
                            "light grey")
        app.canvasContainer = CanvasContainer("canvasContainer",
                            canvasContainerX, canvasContainerY,
                            canvasContainerWidth, canvasContainerHeight,
                            "gainsboro")
        app.menus = [app.topBar, app.sideBar, app.canvasContainer]

    # Returns the menu object that was clicked on
    def menuClicked(app, clickx, clicky):
        for menu in app.menus:
            x0, y0, x1, y1 = menu.getBounds()
            if (x0 <= clickx <= x1) and (y0 <= clicky <= y1):
                return menu


    # Drawing the menus
    def drawCanvasContainer(app, canvas):
        app.canvasContainer.drawMenu(canvas)

    def drawTopAndSideBar(app, canvas):
        app.topBar.drawMenu(canvas)
        app.topBar.drawOptions(canvas)
        app.sideBar.drawMenu(canvas)


# Contains variables and methods that initalize and draw the menu/bars 
    # each menu should have a way to check and handle clicks
    # the actual contents of the menus should be determined by the subclass
    # the canvas object is considered to be a menu!
class Menu(object):
    def __init__(self, name, cornerx, cornery, width, height, color):
        self.name = name
        self.cornerx = cornerx
        self.cornery = cornery
        self.width = width
        self.height = height
        self.color = color

    # Returns x0, y0, x1, y1 of menu
    def getBounds(self):
        return (self.cornerx, self.cornery,
                self.cornerx + self.width, self.cornery + self.height)

    def drawMenu(self, canvas):
        # Menu.getBounds(self) might not work...
        canvas.create_rectangle(Menu.getBounds(self), fill=self.color,
                                outline="")

    def __repr__(self):
        return self.name

class TopBar(Menu):
    def __init__(self, name, cornerx, cornery, width, height, color):
        super().__init__(name, cornerx, cornery, width, height, color)
        self.padding = 5
        self.options = ["brush", "eraser", "size"]
        self.optionSelected = "brush"

    def getOptionBounds(self, optionIndex):
        # Bounds of the bar    
        cellWidth = (self.width - 2 * self.padding) // len(self.options)
        cellHeight = self.height - 2 * self.padding
        x0 = self.cornerx + self.padding + cellWidth * optionIndex
        y0 = self.cornery + self.padding
        x1 = self.cornerx + self.padding + cellWidth * (optionIndex + 1)
        y1 = self.cornery + self.padding + cellHeight
        return x0, y0, x1, y1

    def drawOptions(self, canvas):
        for i in range(len(self.options)):
            fill=""
            if self.options[i] == self.optionSelected:
                fill = "gray55"
            x0, y0, x1, y1 = TopBar.getOptionBounds(self, i)
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
            canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2,
                                    text=self.options[i])

    def changeOption(self, app, clickx, clicky):
        for i in range(len(self.options)):
            optx0, opty0, optx1, opty1 = TopBar.getOptionBounds(self, i)
            if ((optx0 <= clickx <= optx1) and (opty0 <= clicky <= opty1)):
                if self.options[i] == "size":
                    newSize = app.getUserInput("New size (px):")
                    if int(newSize) > 0:
                        app.brushSize = int(newSize)
                    return
                self.optionSelected = self.options[i]

class SideBar(Menu):
    pass
class CanvasContainer(Menu):
    pass