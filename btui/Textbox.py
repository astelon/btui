from blessed import Terminal

class Textbox :
    """ A Text Field that can be edited with vim key bindings.
        - x            (int)      x position
        - y            (int)      y position
        - width        (int)      width of the box
        - height       (int)      height of the box
        - text         (string)   the text in the box
        - style        (string)   the basic style to be used when not edited or focused
        - edit_style   (string)   The style to be used on edit mode
        - focus_style  (string)   The style to be used on focus
        - cursor_style (string)   The style for the cursor
        - border       (bool)     true/false
        - multiline    (bool)     Whether the textbox can accept many lines or not
        - terminal     (Terminal) Terminal object from blessed.
    """
    attributes = {}
    cursorX = 0
    cursorY = 0
    focused  = False
    editting = False

    def __init__(self, **kwargs):
        self.attributes = kwargs
        self.cursorX = len(kwargs.get('text',''))

    def moveFwd(self):
        if self.focused and self.cursorX < self.attributes.get('width')-1:
            self.cursorX += 1

    def moveBwd(self):
        if self.focused and self.cursorX > 0:
            self.cursorX -= 1

    def moveUp(self):
        if self.focused and self.cursorY > 0:
            self.cursorY -= 1

    def moveDown(self):
        if self.focused and self.cursorY < self.attributes.get('height',0)-1:
            self.cursorY += 1

    def draw(self) :
        buffer = ''
        term = self.attributes.get('terminal',None)
        if term is None:
            print("No terminal has been detected!!")
        x = self.attributes.get('x',0)
        y = self.attributes.get('y',0)
        text = self.attributes.get('text','')
        buffer = term.move_xy(x, y)
        style = ''
        if self.focused:
            style = self.attributes.get('focus_style', self.attributes.get('style', ''))
        else:
            style = self.attributes.get('style', self.attributes.get('focus_style', ''))

        if self.editting:
            style = self.attributes.get('edit_style', self.attributes.get('focus_style', ''))

        buffer += style
        text += ' ' * (self.attributes.get('width') - len(text))

        if self.focused or self.editting:
            buffer += text[:self.cursorX] + self.attributes.get('cursor_style','') + text[self.cursorX] + style
            if self.cursorX < len(text)-1:
                buffer += text[self.cursorX+1:]
        else:
            buffer += text
        print(buffer, end='')

    def text(self):
        return self.attributes.get('text','')

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False

    def start_edit(self):
        self.editting = True

    def end_edit(self):
        self.editting = False

    def replace(self, char):
        pass

    def insert(self, char):
        if not self.editing:
            return
        if self.cursorX >= self.attributes.get('width',0):
            return
        text = self.attributes.get('text','')
        self.attributes['text'] = text[:self.cursorx] + char + text[self.cursorX+1:]
        self.cursorX +=1

    def append(self, char):
        pass


if __name__ == '__main__':
    term = Terminal()
    result = ''

    with term.fullscreen(), term.cbreak():
        tb = Textbox(
                x     = 15,
                y     = 5,
                width = 30,
                height = 1,
                style = term.black_on_white,
                edit_style   = term.underline + term.black_on_lightgreen,
                focus_style  = term.underline + term.black_on_white,
                cursor_style = term.white_on_blue,
                text     = 'Hello Box',
                terminal = term,
                )
        val = ''
        callbacks_no_args = {
            'i' : tb.start_edit,
            'f' : tb.focus,
            'h' : tb.moveBwd,
            'l' : tb.moveFwd,
            'u' : tb.unfocus,
            'k' : tb.moveUp,
            'j' : tb.moveDown,
        }
        itr = 0
        while val.lower() != 'q':
            print(term.white_on_black)
            term.clear()
            print(term.move_xy(0,1) + f'Iteration {itr}', end='')
            print(term.move_xy(15,0) + f'Read {val}')
            tb.draw()
            itr += 1
            val = term.inkey()
            print(term.white_on_black)
            func = callbacks_no_args.get(val,None)
            if func:
                func()
            term.clear()
            tb.draw()


        ############### TEARDOWN ################
        print(term.whitei_on_black)
        result = tb.text()

    print(f'Text read: {result}')

