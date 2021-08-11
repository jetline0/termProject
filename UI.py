from cmu_112_graphics import *
from Drawing import *
from Canvas import *

class UI:
    # Initializes the variables that change how the UI is displayed
    def initializeUIVariables(app):
        # Top bar's left corner is always at (0,0)
        app.topBarWidth = app.width
        app.topBarHeight = 40
        app.topBarX = 0
        app.topBarY = 0
        # Side bar's left corner is always at (app.width - app.sideBarWidth, app.topBarHeight)
        sideBarWidth = 150
        sideBarHeight = app.height - app.topBarHeight
        sideBarX = app.width - sideBarWidth
        sideBarY = app.topBarHeight
        # The canvas container's left corner is always at (0, topBarHeight)
        app.canvasContainerWidth = app.width - sideBarWidth
        app.canvasContainerHeight = app.height - app.topBarHeight
        app.canvasContainerX = 0
        app.canvasContainerY = app.topBarHeight
        # Initialize menus
        app.topBar = TopBar("topBar",
                            app.topBarX, app.topBarY,
                            app.topBarWidth, app.topBarHeight,
                            "gray64")
        app.sideBar = SideBar("sideBar",
                            sideBarX, sideBarY,
                            sideBarWidth, sideBarHeight,
                            "light grey")
        app.canvasContainer = CanvasContainer("canvasContainer",
                            app.canvasContainerX, app.canvasContainerY,
                            app.canvasContainerWidth, app.canvasContainerHeight,
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
        app.sideBar.drawOptions(canvas)


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

    # Draws the menu
    def drawMenu(self, canvas):
        # Menu.getBounds(self) might not work...
        canvas.create_rectangle(Menu.getBounds(self), fill=self.color,
                                outline="")
    # Nicer print statement for debugging
    def __repr__(self):
        return self.name

class TopBar(Menu):
    def __init__(self, name, cornerx, cornery, width, height, color):
        super().__init__(name, cornerx, cornery, width, height, color)
        self.padding = 5 # Padding between buttons and edges of the menu
        self.options = ["brush", "eraser", "fill", "size"]
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
                    newSize = app.getUserInput("New size between 5 and 20 (inclusive):")
                    if newSize == None:
                        return
                    while newSize == "" or not (20 >= int(newSize) >= 5):
                        newSize = app.getUserInput("Please enter a new size between 5 and 20 (inclusive)!")                    
                    app.brushSize = int(newSize)
                    return
                self.optionSelected = self.options[i]
                return

class SideBar(Menu):
    # Displays files

    def __init__(self, name, cornerx, cornery, width, height, color):
        super().__init__(name, cornerx, cornery, width, height, color)
        self.padding = 5
        self.options = ["load", "save file"]
        # app.files is the list of File objects

    def getFileBounds(self, app, fileIndex):
        # Bounds of the bar    
        cellWidth = (self.width - 2 * self.padding)
        cellHeight = (self.height - 2 * self.padding) // len(app.files)
        x0 = self.cornerx + self.padding
        y0 = self.cornery + self.padding + cellHeight * fileIndex
        x1 = self.cornerx + self.padding + cellWidth
        y1 = self.cornery + self.padding + cellHeight * (fileIndex + 1)
        return x0, y0, x1, y1

    def drawFileThumbnails(self, canvas, filepos):
        pass

    def drawFileRectangles(self, canvas):
        # going to call drawFileThumbnails somewhere
        pass

    def getOptionBounds(self, optionIndex):
        catch, catch, self.rightcornerx, self.rightcornery = self.getBounds()
        cellWidth = (self.width - 2 * self.padding) // len(self.options)
        cellHeight = 20
        x0 = self.cornerx + self.padding + cellWidth * optionIndex
        y0 = self.rightcornery - self.padding - cellHeight
        x1 = self.cornerx + self.padding + cellWidth * (optionIndex + 1)
        y1 = self.rightcornery - self.padding
        return x0, y0, x1, y1

    def drawOptions(self, canvas):
        for i in range(len(self.options)):
            x0, y0, x1, y1 = SideBar.getOptionBounds(self, i)
            canvas.create_rectangle(x0, y0, x1, y1, fill="gray74")
            canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2,
                                    text=self.options[i])

    def changeOption(self, app, clickx, clicky):
        for i in range(len(self.options)):
            optx0, opty0, optx1, opty1 = SideBar.getOptionBounds(self, i)
            if ((optx0 <= clickx <= optx1) and (opty0 <= clicky <= opty1)):
                if self.options[i] == "load":
                    print("load")
                    newFile = app.loadImage()
                    newFileObject = File(app, len(app.files), newFile)
                    app.files.append(newFileObject)
                    print(f"pls open me now i am file {len(app.files)}")
                    return
                else:
                    path = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                            title='Select directory: ',
                            filetypes = (('png files','*.png'),
                                         ('all files','*.*')))
                    app.Image.save(path+".png")
                    print(f"saved at {path + '.png'}")
                    

class CanvasContainer(Menu):
    pass