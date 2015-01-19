from kivy.properties import (
    ObjectProperty,
    StringProperty
)
from kivy.lang import Builder
from kivy.uix.codeinput import CodeInput
from kivy.uix.boxlayout import BoxLayout
from pygments.lexers import Python3Lexer


class ELiDECodeInput(CodeInput):
    lexer = ObjectProperty(Python3Lexer())


class ELiDEFunctionInput(BoxLayout):
    header = StringProperty('')


kv = """
<ELiDEFunctionInput>:
    orientation: 'vertical'
    ELiDECodeInput:
        id: signature
        text: root.header
        disabled: True
        height: self.line_height + self.font_size
        background_disabled_normal: ''
        disabled_foreground_color: self.foreground_color
        size_hint_y: None
    BoxLayout:
        orientation: 'horizontal'
        Label:
            canvas:
                Color:
                    rgba: signature.background_color
                Rectangle:
                    pos: self.pos
                    size: self.size
                Color:
                    rgba: [1., 1., 1., 1.]
            # PEP8 standard indentation width is 4 spaces
            text: ' ' * 4
            size_hint_x: None
            width: self.texture_size[0]
        ELiDECodeInput:
            id: code
"""
Builder.load_string(kv)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(ELiDEFunctionInput(header='def foo(bar, bas):'))
