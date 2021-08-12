from cmu_112_graphics import *
import decimal

# taken from cs 15-112 basic helper functions 
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

# round values in a 3-tuple (thruple???)
def roundthruple(t):
    return (roundHalfUp(t[0]),
            roundHalfUp(t[1]),
            roundHalfUp(t[2]))

# https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB
# hue: 0 - 360, saturation: 0 - 1, value: 0 - 1 
def HSVtoRGB(h, s, v):
    # chroma = v * s
    c = v * s
    hprime = h / 60
    x = c * (1 - abs(hprime % 2 - 1))
    m = v - c
    if 0 <= hprime <= 1:
        return ((c + m)*255, (x + m)*255 , (0 + m)*255)
    if 1 < hprime <= 2:
        return ((x + m)*255, (c + m)*255 , (0 + m)*255)
    if 2 < hprime <= 3:
        return ((0 + m)*255, (c + m)*255 , (x + m)*255)
    if 3 < hprime <= 4:
        return ((0 + m)*255, (x + m)*255 , (c + m)*255)
    if 4 < hprime <= 5:
        return ((x + m)*255, (0 + m)*255 , (c + m)*255)
    if 5 < hprime <= 6:
        return ((c + m)*255, (0 + m)*255 , (x + m)*255)

class Colorpicker:
    def initializeColorpickerVars(app):
        app.squareWidth = app.width // 2
        app.squareHeight = app.height // 2
        app.barHeight = 20
        app.barWidth = app.squareWidth
        # store x of location app.barSelect * 360 / width is the actual hsv val
        app.barSelect = 0
        app.squareSelectX = app.squareWidth 
        app.squareSelectY = 0

    def initializeColorpicker(app):
        Colorpicker.initializeColorpickerVars(app)
        Colorpicker.generateBar(app)
        Colorpicker.generateSquare(app)


    # use HSV to generate the RGB strip
    def generateBar(app):
        bar = Image.new("RGB", (app.barWidth, app.barHeight))
        data = bar.load()
        # https://stackoverflow.com/questions/12062920/how-do-i-create-an-image-in-pil-using-a-list-of-rgb-tuples
        for x in range(bar.size[0]):
            for y in range(bar.size[1]):
                width = bar.size[0]
                data[x,y] = roundthruple(HSVtoRGB(x * 360 / width, 1, 1))
        app.barImage = ImageTk.PhotoImage(bar)
    # regenerate square on mouse dragged and pressed
    def generateSquare(app):
        square = Image.new("RGB", (app.squareWidth, app.squareHeight))
        data = square.load()
        for x in range(square.size[0]):
            for y in range(square.size[1]):
                width = square.size[0]
                height = square.size[1]
                data[x,y] = roundthruple(HSVtoRGB(app.barSelect * 360 / width,
                                                    x / width,
                                                    y / height))
        app.squareImage = ImageTk.PhotoImage(square)

    def getBoundsBar(app):
        centerx = app.width/2
        centery = app.height/2 + app.squareHeight/2 + app.barHeight/2
        x0 = centerx - app.barWidth / 2
        x1 = centerx + app.barWidth / 2
        y0 = centery - app.barHeight / 2
        y1 = centery + app.barHeight / 2
        return x0, y0, x1, y1

    def getBoundsSquare(app):
        centerx = app.width/2
        centery = app.height/2
        x0 = centerx - app.squareWidth / 2
        x1 = centerx + app.squareWidth / 2
        y0 = centery - app.squareHeight / 2
        y1 = centery + app.squareHeight / 2
        return x0, y0, x1, y1

    def handleClick(app, event):
        x0, y0, x1, y1 = Colorpicker.getBoundsBar(app)
        if x0 <= event.x <= x1 and y0 <= event.y <= y1:
            print("bar")
            return
        x0, y0, x1, y1 = Colorpicker.getBoundsSquare(app)
        if x0 <= event.x <= x1 and y0 <= event.y <= y1:
            print("square")
            return
        print("none")


    def findRelativeCoords(app, clickx, clicky):
        pass

    def changeSquareSelection(app, event):
        # turn event.x and event.y into relative x's and y's 
        pass

    def drawBar(app, canvas):
        canvas.create_image(app.width/2, app.height/2 + app.squareHeight/2 + app.barHeight/2,
                             image=app.barImage)

    def drawSquare(app, canvas):
        canvas.create_image(app.width/2, app.height/2,
                             image=app.squareImage)

    def drawBarSelection(app, canvas):
        canvas.create_oval()