from cmu_112_graphics import *

class AppCanvas:
    # Initializes layers - OKAY!
    def initializeFiles(app):
        app.fileWidth = 500
        app.fileHeight = 300
        app.canvasX = 40
        app.canvasY = 80
        app.files = [File(app, 0)]
        app.currentFile = 0

    # Draws file - OKAY!
    def drawFile(app, canvas):
        im = ImageTk.PhotoImage(app.files[app.currentFile].image)
        canvas.create_image(app.canvasX, app.canvasY, anchor="nw", image=im)

# A File object is just a wrapper for one Image object
class File(object):
    def __init__(self, app, pos, filepath=""):
        self.pos = pos
        self.fill = None
        if pos == 0:
            self.fill = (255, 255, 255)
        if filepath == "":
            self.image = Image.new("RGB", (app.fileWidth, app.fileHeight),
                                    self.fill)
        else:
            #not 100% confirmed functional rn
            self.image = Image.open(filepath)