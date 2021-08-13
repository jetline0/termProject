from cmu_112_graphics import *
import decimal


# credit to https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter/51592104
def fromrgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb   


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

def findRelativeCoords(app, clickx, clicky, x0, y0):
    return clickx - x0, clicky - y0


class Colorpicker:
    def initializeColorpickerVars(app):
        app.squareWidth = app.width // 2
        app.squareHeight = app.height // 2
        app.barHeight = 20
        app.barWidth = app.squareWidth
        # lower the count of calculations 
        app.scale = 5
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


    def generateSquare(app):
        square = Image.new("RGB", (app.squareWidth // app.scale, app.squareHeight // app.scale))
        data = square.load()
        for x in range(square.size[0]):
            for y in range(square.size[1]):
                width = square.size[0]
                height = square.size[1]
                data[x,y] = roundthruple(HSVtoRGB((app.barSelect / app.scale) * 360 / width,
                                                    x / width,
                                                    1 - y / height))
        app.square = square.resize((app.squareWidth, app.squareHeight))
        app.squareImage = ImageTk.PhotoImage(app.square)

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
            Colorpicker.changeBarSelection(app, event)
            Colorpicker.generateSquare(app)
            Colorpicker.changeCurrentColor(app)
            return
        x0, y0, x1, y1 = Colorpicker.getBoundsSquare(app)
        if x0 <= event.x <= x1 and y0 <= event.y <= y1:
            Colorpicker.changeSquareSelection(app, event)
            Colorpicker.changeCurrentColor(app)

    def changeBarSelection(app, event):
        x0, y0, x1, y1 = Colorpicker.getBoundsBar(app)
        relx, rely = findRelativeCoords(app, event.x, event.y, x0, y0)
        app.barSelect = relx

    def changeSquareSelection(app, event, changeX=True, changeY=True):
        x0, y0, x1, y1 = Colorpicker.getBoundsSquare(app)
        relx, rely = findRelativeCoords(app, event.x, event.y, x0, y0)
        if changeX:
            app.squareSelectX = relx
        if changeY:
            app.squareSelectY = rely

    def changeCurrentColor(app):
        # really cheap dirty solution, but basically x of 500 or y of 250 crashes
        # because that pixel index doesn't exist
        try:
            app.currentColor = app.square.getpixel((app.squareSelectX, app.squareSelectY))
        except:
            return

    def drawBar(app, canvas):
        canvas.create_image(app.width/2, app.height/2 + app.squareHeight/2 + app.barHeight/2,
                             image=app.barImage)

    def drawSquare(app, canvas):
        canvas.create_image(app.width/2, app.height/2,
                             image=app.squareImage)

    def drawBarSelection(app, canvas):
        x0, y0, x1, y1 = Colorpicker.getBoundsBar(app)
        ovalcx = x0 + app.barSelect
        ovalcy = (y0 + y1) / 2
        outline = fromrgb((255-app.currentColor[0], 255-app.currentColor[1], 255-app.currentColor[2]))
        canvas.create_oval(ovalcx - 5, ovalcy - 5, ovalcx + 5, ovalcy + 5,
                            outline=outline)

    def drawSquareSelection(app, canvas):
        x0, y0, x1, y1 = Colorpicker.getBoundsSquare(app)
        ovalcx = x0 + app.squareSelectX
        ovalcy = y0 + app.squareSelectY
        outline = fromrgb((255-app.currentColor[0], 255-app.currentColor[1], 255-app.currentColor[2]))
        canvas.create_oval(ovalcx - 5, ovalcy - 5, ovalcx + 5, ovalcy + 5,
                            fill=fromrgb(app.currentColor), outline=outline)

    def drawCurrentColor(app, canvas):
        x0,y0,x1,y1 = Colorpicker.getBoundsBar(app)
        canvas.create_rectangle(x0,y1,x1,y1+app.barHeight, fill=fromrgb(app.currentColor),
                                outline="")
        canvas.create_text((x0+x1)/2, y1+app.barHeight/2, text="Current color",
                fill=fromrgb((255-app.currentColor[0], 255-app.currentColor[1], 255-app.currentColor[2])))
        canvas.create_text((x0+x1)/2, y1+app.barHeight*3/2, text="Press 'b' to return to the canvas.")


    def changePoints(app):
        Colorpicker.HSVtoPoints(app, *Colorpicker.fromCurrentColorToHSV(app))
        
    def fromCurrentColorToHSV(app):
        # RGB to HSV
        return Colorpicker.RGBtoHSV(*app.currentColor)

    # based off of this: https://www.rapidtables.com/convert/color/rgb-to-hsv.html
    def RGBtoHSV(r,g,b):
        rprime, gprime, bprime = r/255, g/255, b/255
        rgb = {"rprime": rprime, "gprime": gprime, "bprime": bprime}
        cmax = max(rgb)
        cmin = min(rgb)
        d = rgb[cmax] - rgb[cmin]
        # get hue
        if d == 0:
            h = 0
        elif cmax == "rprime":
            h = 60 * ((gprime - bprime)/d % 6)
        elif cmax == "gprime":
            h = 60 * ((bprime - rprime)/d + 2)
        elif cmax == "bprime":
            h = 60 * ((rprime - gprime)/d + 4)
        # get saturation
        if rgb[cmax] == 0:
            s = 0
        else:
            s = d/rgb[cmax]
        # get val
        v = rgb[cmax]
        return (h,s,v)

    def HSVtoPoints(app, h, s, v):
        # h = new barSelect * 360 / width of bar
        # s = new x / width 
        # v = new y / height
        app.barSelect = h * app.barWidth / 360
        app.squareSelectX = s * app.squareWidth
        app.squareSelectY = v * app.squareHeight
    