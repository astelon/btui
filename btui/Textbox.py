from blessed import Terminal

class Textbox :
    """ A Text Field that can be edited with vim key bindings.
        - x           (int)     x position
        - y           (int)     y position
        - width       (int)     width of the box
        - height      (int)     height of the box
        - text        (string)  the text in the box
        - style       (string)  the basic style to be used when not edited or focused
        - edit_style  (string)  The style to be used on edit mode
        - focus_style (string)  The style to be used on focus
        - border      (bool)    true/false
        - multiline   (bool)    Whether the textbox can accept many lines or not
    """
    attributes = {}
    cursorX = 0
    cursorY = 0
    focused  = False
    editting = False

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
        x = self.attributes.get('x',0)
        y = self.attributes.get('y',0)
        text = self.attributes.get('text')
        print(term.move_xy(x, y))
        if self.focused:
            print(self.attributes.get('focus_style', self.attributes.get('style', '')))
        else:
            print(self.attributes.get('style', self.attributes.get('focus_style', '')))

        if self.editting:
            print(self.attributes.get('edit_style', self.attributes.get('focus_style', '')))

        text += ' ' * (self.attributes.get('width') - len(text))
        print(text)
        if self.focused or self.editting:
            print(term.move_xy(self.cursorX + x, self.cursorY + y))

    def text(self):
        return self.attributes.get('text','')

    def setFocused(self, focus):
        self.focused = focus

    def edit(self, term):
        self.editting = True

        self.editting = False


if __name__ == '__main__':
    term = Terminal()
    result = ''
    with term.fullscreen(), term.cbreak():
        tb = Textbox({
                'x'     : 15,
                'y'     : 5,
                'width' : 30,
                'style' : term.black_on_white,
                'edit_style'  : term.underline + term.black_on_lightgreen,
                'focus_style' : term.underline + term.black_on_white,
                'text'  : 'Hello Box'
                })

        tb.draw(term)
        term.inkey()

        ############### TEARDOWN ################
        print(term.on_black)
        result = tb.text()

    print(f'Text read: {result}')

