from blessed import Terminal

class Label:
    """A simple Label class
       Attributes:
            - x (int)       : X position
            - y (int)       : Y position
            - text (String) : Text to be printed
    """
    attributes = {}
    def __init__(self, attr):
        self.attributes = attr

    def print(self, term):
        print(term.move_y(self.attributes.get('y')) + term.move_x(self.attributes.get('x')) + self.attributes.get('text'))


if __name__ == '__main__':
    term = Terminal()
    with term.fullscreen(), term.cbreak():
        lbl = Label({                                                 \
            'x' : 5,                                                        \
            'y' : 5,                                                        \
            'text' : term.bold + term.bright_white_on_black + "Hello " + term.normal + term.underline + term.black_on_yellow + "World!"  \
        })
        lbl.print(term)
        term.inkey()
        print(term.on_black)

