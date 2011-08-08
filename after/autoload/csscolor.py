# Language:     Colored CSS Color Preview
# Author:       Max Vasiliev <vim@skammer.name>
# Modified By:  Eiichi Sato <sato.eiichi@gmail.com>
# Last Change:  2011 Jul 31
# Licence:      No Warranties. WTFPL. But please tell me!
# Version:      0.7.1

from itertools import chain

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

    colortable = list(enumerate(map(index_to_rgb, range(0, 254))))

    @staticmethod
    @memoized
    def rgb_to_index(rgb):
        def diff(color):
            r = color[1][0]-rgb[0]
            g = color[1][1]-rgb[1]
            b = color[1][2]-rgb[2]
            return r*r + g*g + b*b
        best = min((color for color in CSSColor.colortable), key=diff)
        return best[0]
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

    @staticmethod
    def add_syntax_keyword(color, name):
        group = 'cssColor' + color[1:]
        vim.command('syntax keyword {group} {pattern} contained'.format(group=group, pattern=name))
        vim.command('syntax cluster cssColors add={group}'.format(group=group))
        VimCSSColor.add_highlight(group, color)

    w3c_colors = [
        ('#800000', 'maroon'),
        ('#FF0000', 'red'),
        ('#FFA500', 'orange'),
        ('#FFFF00', 'yellow'),
        ('#808000', 'olive'),
        ('#800080', 'purple'),
        ('#FF00FF', 'fuchsia'),
        ('#FFFFFF', 'white'),
        ('#00FF00', 'lime'),
        ('#008000', 'green'),
        ('#000080', 'navy'),
        ('#0000FF', 'blue'),
        ('#00FFFF', 'aqua'),
        ('#008080', 'teal'),
        ('#000000', 'black'),
        ('#C0C0C0', 'silver'),
        ('#808080', 'gray'),
    ]

    named_colors = [
        ('#F0F8FF', 'AliceBlue'),
        ('#FAEBD7', 'AntiqueWhite'),
        ('#7FFFD4', 'Aquamarine'),
        ('#F0FFFF', 'Azure'),
        ('#F5F5DC', 'Beige'),
        ('#FFE4C4', 'Bisque'),
        ('#FFEBCD', 'BlanchedAlmond'),
        ('#8A2BE2', 'BlueViolet'),
        ('#A52A2A', 'Brown'),
        ('#DEB887', 'BurlyWood'),
        ('#5F9EA0', 'CadetBlue'),
        ('#7FFF00', 'Chartreuse'),
        ('#D2691E', 'Chocolate'),
        ('#FF7F50', 'Coral'),
        ('#6495ED', 'CornflowerBlue'),
        ('#FFF8DC', 'Cornsilk'),
        ('#DC143C', 'Crimson'),
        ('#00FFFF', 'Cyan'),
        ('#00008B', 'DarkBlue'),
        ('#008B8B', 'DarkCyan'),
        ('#B8860B', 'DarkGoldenRod'),
        ('#A9A9A9', 'DarkGray'),
        ('#A9A9A9', 'DarkGrey'),
        ('#006400', 'DarkGreen'),
        ('#BDB76B', 'DarkKhaki'),
        ('#8B008B', 'DarkMagenta'),
        ('#556B2F', 'DarkOliveGreen'),
        ('#FF8C00', 'Darkorange'),
        ('#9932CC', 'DarkOrchid'),
        ('#8B0000', 'DarkRed'),
        ('#E9967A', 'DarkSalmon'),
        ('#8FBC8F', 'DarkSeaGreen'),
        ('#483D8B', 'DarkSlateBlue'),
        ('#2F4F4F', 'DarkSlateGray'),
        ('#2F4F4F', 'DarkSlateGrey'),
        ('#00CED1', 'DarkTurquoise'),
        ('#9400D3', 'DarkViolet'),
        ('#FF1493', 'DeepPink'),
        ('#00BFFF', 'DeepSkyBlue'),
        ('#696969', 'DimGray'),
        ('#696969', 'DimGrey'),
        ('#1E90FF', 'DodgerBlue'),
        ('#B22222', 'FireBrick'),
        ('#FFFAF0', 'FloralWhite'),
        ('#228B22', 'ForestGreen'),
        ('#DCDCDC', 'Gainsboro'),
        ('#F8F8FF', 'GhostWhite'),
        ('#FFD700', 'Gold'),
        ('#DAA520', 'GoldenRod'),
        ('#808080', 'Grey'),
        ('#ADFF2F', 'GreenYellow'),
        ('#F0FFF0', 'HoneyDew'),
        ('#FF69B4', 'HotPink'),
        ('#CD5C5C', 'IndianRed'),
        ('#4B0082', 'Indigo'),
        ('#FFFFF0', 'Ivory'),
        ('#F0E68C', 'Khaki'),
        ('#E6E6FA', 'Lavender'),
        ('#FFF0F5', 'LavenderBlush'),
        ('#7CFC00', 'LawnGreen'),
        ('#FFFACD', 'LemonChiffon'),
        ('#ADD8E6', 'LightBlue'),
        ('#F08080', 'LightCoral'),
        ('#E0FFFF', 'LightCyan'),
        ('#FAFAD2', 'LightGoldenRodYellow'),
        ('#D3D3D3', 'LightGray'),
        ('#D3D3D3', 'LightGrey'),
        ('#90EE90', 'LightGreen'),
        ('#FFB6C1', 'LightPink'),
        ('#FFA07A', 'LightSalmon'),
        ('#20B2AA', 'LightSeaGreen'),
        ('#87CEFA', 'LightSkyBlue'),
        ('#778899', 'LightSlateGray'),
        ('#778899', 'LightSlateGrey'),
        ('#B0C4DE', 'LightSteelBlue'),
        ('#FFFFE0', 'LightYellow'),
        ('#32CD32', 'LimeGreen'),
        ('#FAF0E6', 'Linen'),
        ('#FF00FF', 'Magenta'),
        ('#66CDAA', 'MediumAquaMarine'),
        ('#0000CD', 'MediumBlue'),
        ('#BA55D3', 'MediumOrchid'),
        ('#9370D8', 'MediumPurple'),
        ('#3CB371', 'MediumSeaGreen'),
        ('#7B68EE', 'MediumSlateBlue'),
        ('#00FA9A', 'MediumSpringGreen'),
        ('#48D1CC', 'MediumTurquoise'),
        ('#C71585', 'MediumVioletRed'),
        ('#191970', 'MidnightBlue'),
        ('#F5FFFA', 'MintCream'),
        ('#FFE4E1', 'MistyRose'),
        ('#FFE4B5', 'Moccasin'),
        ('#FFDEAD', 'NavajoWhite'),
        ('#FDF5E6', 'OldLace'),
        ('#6B8E23', 'OliveDrab'),
        ('#FF4500', 'OrangeRed'),
        ('#DA70D6', 'Orchid'),
        ('#EEE8AA', 'PaleGoldenRod'),
        ('#98FB98', 'PaleGreen'),
        ('#AFEEEE', 'PaleTurquoise'),
        ('#D87093', 'PaleVioletRed'),
        ('#FFEFD5', 'PapayaWhip'),
        ('#FFDAB9', 'PeachPuff'),
        ('#CD853F', 'Peru'),
        ('#FFC0CB', 'Pink'),
        ('#DDA0DD', 'Plum'),
        ('#B0E0E6', 'PowderBlue'),
        ('#BC8F8F', 'RosyBrown'),
        ('#4169E1', 'RoyalBlue'),
        ('#8B4513', 'SaddleBrown'),
        ('#FA8072', 'Salmon'),
        ('#F4A460', 'SandyBrown'),
        ('#2E8B57', 'SeaGreen'),
        ('#FFF5EE', 'SeaShell'),
        ('#A0522D', 'Sienna'),
        ('#87CEEB', 'SkyBlue'),
        ('#6A5ACD', 'SlateBlue'),
        ('#708090', 'SlateGray'),
        ('#708090', 'SlateGrey'),
        ('#FFFAFA', 'Snow'),
        ('#00FF7F', 'SpringGreen'),
        ('#4682B4', 'SteelBlue'),
        ('#D2B48C', 'Tan'),
        ('#D8BFD8', 'Thistle'),
        ('#FF6347', 'Tomato'),
        ('#40E0D0', 'Turquoise'),
        ('#EE82EE', 'Violet'),
        ('#F5DEB3', 'Wheat'),
        ('#F5F5F5', 'WhiteSmoke'),
        ('#9ACD32', 'YellowGreen'),
    ]

    @staticmethod
    def define_named_colors():
        for color, name in chain(VimCSSColor.w3c_colors, VimCSSColor.named_colors):
            VimCSSColor.add_syntax_keyword(color, name)

