# Language:     Colored CSS Color Preview
# Author:       Max Vasiliev <vim@skammer.name>
# Modified By:  Eiichi Sato <sato.eiichi@gmail.com>
# Last Change:  2011 Jul 31
# Licence:      No Warranties. WTFPL. But please tell me!
# Version:      0.7.1

class memoized(object): # {{{
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            return self.func(*args)
# }}}
class CSSColor(object): # {{{
    @staticmethod
    def code_to_rgb(code):
        def conv(s):
            try: return int(s, 16)
            except ValueError: return 0
        return conv(code[1:3]), conv(code[3:5]), conv(code[5:7])

    @staticmethod
    def percentage_to_rgb(p):
        def conv(s):
            if s[-1] == '%':
                return int(int(s[:-1])/100.0*255)
            else: return int(s)
        return tuple(conv(c) for c in p)

    @staticmethod
    def rgb_to_code(rgb):
        def conv(value):
            return max(min(value, 255), 0)
        return '#{0:02X}{1:02X}{2:02X}'.format(*[conv(v) for v in rgb])

    @staticmethod
    def calc_fg(rgb):
        if rgb[0]*30 + rgb[1]*59 + rgb[2]*11 > 12000:
            return (0, 0, 0)
        else:
            return (255, 255, 255)

    def index_to_rgb(index):
        # 16 basic colors
        basic16 = [
            [0x00, 0x00, 0x00], [0xCD, 0x00, 0x00],
            [0x00, 0xCD, 0x00], [0xCD, 0xCD, 0x00],
            [0x00, 0x00, 0xEE], [0xCD, 0x00, 0xCD],
            [0x00, 0xCD, 0xCD], [0xE5, 0xE5, 0xE5],
            [0x7F, 0x7F, 0x7F], [0xFF, 0x00, 0x00],
            [0x00, 0xFF, 0x00], [0xFF, 0xFF, 0x00],
            [0x5C, 0x5C, 0xFF], [0xFF, 0x00, 0xFF],
            [0x00, 0xFF, 0xFF], [0xFF, 0xFF, 0xFF],
        ]

        # the 6 value iterations in the xterm color cube
        values = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]

        if index < 16:
            return basic16[index]
        elif 16 <= index < 233:
            index -= 16
            return [values[(index//36)%6], values[(index//6)%6], values[index%6]]
        elif 233 <= index < 254:
            return [8+(index-232)*0x0A]*3

    colortable = [index_to_rgb(color) for color in range(0, 254)]

    @staticmethod
    def diff(rgb1, rgb2):
        return sum(pow(a-b,2) for a, b in zip(rgb1, rgb2))

    @staticmethod
    @memoized
    def rgb_to_index(rgb):
        index, rgb_best = min(((i, c) for i, c in enumerate(CSSColor.colortable)), key=lambda x: CSSColor.diff(x[1], rgb))
        return index
# }}}

import vim

class VimCSSColor(object):

    @staticmethod
    def percentage_to_code(r, g, b):
        result = CSSColor.rgb_to_code(CSSColor.percentage_to_rgb((r, g, b)))
        vim.command("return '%s'" % result)

    @staticmethod
    def add_highlight(group, color):
        bgrgb = CSSColor.code_to_rgb(color)
        fgrgb = CSSColor.calc_fg(bgrgb)
        command = 'hi {group} guifg={guifg} guibg={guibg} ctermfg={ctermfg} ctermbg={ctermbg}'
        command = command.format(group=group,
                                 guibg=color,
                                 guifg=CSSColor.rgb_to_code(fgrgb),
                                 ctermbg=CSSColor.rgb_to_index(bgrgb),
                                 ctermfg=CSSColor.rgb_to_index(fgrgb))
        vim.command(command)

