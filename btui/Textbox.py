import blessed
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
    replacing = False
    appending = False
    focus_hint = None

    callbacks_normal = {}
    callbacks_editing = {}

    def moveFwd(self):
        if self.focused and self.cursorX < self.attributes.get('width')-1 and self.cursorX < len(self.attributes.get('text',''))-1:
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

        if self.focus_hint:
            buffer += self.focus_hint

        buffer += style
        text += ' ' * (self.attributes.get('width') - len(text))

        if self.focus_hint:
            text = text[2:]

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
        self.replacing = False
        self.appending = False

    def start_replace(self):
        self.replacing = True
        self.start_edit()

    def start_append(self):
        self.appending = True
        self.start_edit()

    def insert(self, char):
        text = self.attributes.get('text','')
        width = self.attributes.get('width',0)
        if self.cursorX >= width or self.cursorX >= len(text):
            return 
        if len(text) >= self.attributes.get('width',0) and not self.replacing:
            return
        if self.replacing:
            self.attributes['text'] = text[:self.cursorX] + char + text[self.cursorX+1:]
        elif self.appending:
            self.attributes['text'] = text[:self.cursorX+1] + char + text[self.cursorX+1:]
        else:
            self.attributes['text'] = text[:self.cursorX] + char + text[self.cursorX:]
        self.cursorX +=1

    def set_focus_hint(self,text):
        self.focus_hint = text

    def delete_char(self):
        text = self.attributes.get('text','')
        self.attributes['text'] = text[:self.cursorX] + text[self.cursorX+1:]
        if self.cursorX >= len(text) - 1:
            self.cursorX -= 1

    def __init__(self, **kwargs):
        self.attributes = kwargs
        self.cursorX = len(kwargs.get('text',''))-1
        #Define normal mode callbacks:
        self.callbacks_normal = {
            'a' : self.start_append,
            'i' : self.start_edit,
            'r' : self.start_replace,
            'f' : self.focus,
            'h' : self.moveBwd,
            'l' : self.moveFwd,
            'u' : self.unfocus,
            'k' : self.moveUp,
            'j' : self.moveDown,
            'x' : self.delete_char,
        }
        self.callbacks_editing = {
            'KEY_ESCAPE' : self.end_edit,
        }

    def inject_key(self,key):
        val= ''
        if key.is_sequence:
            val = key.name
        else:
            val = key

        func = None
        if not self.editting:
            func = self.callbacks_normal.get(val, None)
            if func:
                func()
        else:
            func = self.callbacks_editing.get(val, None)
            if func:
                func()
            else:
                if not key.is_sequence:
                    self.insert(key)


if __name__ == '__main__':
    term = Terminal()
    result = ''
    import Label

    print(term.white_on_black)
    with term.fullscreen(), term.cbreak():
        print(term.white_on_black)
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
        lb = Label.Label(
            x = 0,
            y = term.height-2,
            text = ''
        )
        val = ''
        itr = 0
        while val.lower() != 'q':
            print(term.white_on_black)
            term.clear()
            print(term.move_xy(0,1) + f'Iteration {itr}', end='')
            print(term.move_xy(15,0) + f'Read {val}')
            tb.draw()
            lb.print(term)
            itr += 1
            val = term.inkey()
            print(term.white_on_black)
            if val == 'f':
                tb.set_focus_hint(term.bold + term.steelblue4_on_white + "gi" + term.normal)
                val = term.inkey()
                if val == 'g': 
                    tb.set_focus_hint(term.bold + term.darkgray_on_white + "g" + term.steelblue4_on_white  + "i" + term.normal)
                    tb.draw()

            else:
                tb.set_focus_hint(None)
                tb.inject_key(val)
            if tb.replacing:
                lb.setText('REPLACE' + term.white_on_black)
            elif tb.appending:
                lb.setText('APPEND-' + term.white_on_black)
            elif tb.editting:
                lb.setText('INSERT-' + term.white_on_black)
            else:
                lb.setText('NORMAL-' + term.white_on_black)

            term.clear()
            tb.draw()
            lb.print(term)


        ############### TEARDOWN ################
        print(term.white_on_black)
        result = tb.text()

    print(f'Text read: {result}')

