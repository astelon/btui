from blessed import Terminal

class Textbox :
    """ A Text Field that can be edited with vim key bindings.
        - x           (int)     x position
        - y           (int)     y position
        - width       (int)     width of the box
        - height      (int)     height of the box
        - text        (string)  the text in the box
        - style       (string)  the FG color 
        - focus_style (string)
        - border      (bool)    true/false
        - multiline   (bool)    Whether the textbox can accept many lines or not
        - 
    """
    attributes = {}
    cursorX = 0
    cursorY = 0
    focused = False

    def __init__(self, attr):
        self.attributes = attr

    def focus(self): pass

    def moveFwd(self):
        self.cursorX += 1

    def moveBwd(self):
        self.cursorX -= 1

    def moveUp(self):
        self.cursorY -= 1

    def moveDown(self):
        self.cursorY += 1

    def draw(self,term) :
        text = self.attributes.get('text')
        print(term.move_xy(self.attributes.get('x'), self.attributes.get('y')))

        if self.focused:
            print(self.attributes.get('focus_style', self.attributes.get('style', '')))
        else:
            print(self.attributes.get('style', self.attributes.get('focus_style', '')))

        text + = ' ' * (self.attributes.get('width') - len(text))
        print(text)
        print(term.move_xy(self.cursorX, self.cursorY))

if __name__ == '__main__':
    term = Terminal()
    tb = Textbox({  })
