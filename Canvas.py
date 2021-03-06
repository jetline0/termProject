from cmu_112_graphics import *

class AppCanvas:
    # Initializes layers - OKAY!
    def initializeFiles(app):
        app.fileWidth = 500
        app.fileHeight = 300
        app.canvasX = 40
        app.canvasY = 80
        app.files = [File(app, pos) for pos in range(3)]
        app.currentFile = 0

    # Draws file - OKAY!
    def drawCurrentFile(app, canvas):
        im = ImageTk.PhotoImage(app.files[app.currentFile].image)
        canvas.create_image(app.canvasX, app.canvasY, anchor="nw", image=im)

    # Gets dimensions of current file
    def getDimensions(app):
        app.Image = app.files[app.currentFile].image
        return app.Image.size

    def clearCurrentFile(app):
        # original dimensions:
        original = app.files[app.currentFile].image
        dimen = original.size
        app.files[app.currentFile].image = Image.new("RGB", dimen, (255,255,255))


# A File object is just a wrapper for one Image object
class File(object):
    def __init__(self, app, pos, img=None):
        self.pos = pos
        self.fill = (255,255,255)
        if img == None:
            self.image = Image.new("RGB", (app.fileWidth, app.fileHeight),
                                    self.fill)
        else:
            self.image = img