# UI
# top toolbar
    # brushes, eraser, brush size, zoom, selection
    # save, open, export
# right layer control and colors
# left canvas
# every "pane" should have scrolling if the window can't fit them all




# implementation steps
# 1. handle canvas layers / transparency and opacity n stuff
# 2. handle drawing with a basic brush
# 3. brush sizes, erasing, zoom, other shapes n stuff
# 4. basic ui
# 5. selection
# 6. saving, exporting


from cmu_112_graphics import *


class Dot(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy


def appStarted(app): 
    app.timerDelay = 1
    app.mouseMovedDelay = 1
    app.dots = []   



def mouseDragged(app, event):
    newDot = Dot(event.x, event.y)
    app.dots.append(newDot)


def redrawAll(app, canvas):
    for dot in app.dots:
        canvas.create_oval(dot.cx - 5, dot.cy - 5, dot.cx + 5, dot.cy + 5,
                            fill="blue")


runApp(width=600, height=600)



# Goals for 8/9:
# before 3pm:
#   *have all menus functional and accessible
#   *fix drawing and erasing
#   *brushing and erasing controlled by buttons 
#   on menu 
#   *change size of brush with a slider
#   *have TP1 done

# after 6pm:
#   *fill tool
#   *shapes tool




# Draw canvas container first, then canvas, then 
# side and top bars

























