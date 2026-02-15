from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
import math
from datetime import datetime
import os

class FractionInput(RelativeLayout):
    """Widget interactivo para fracciones con numerador y denominador editables"""
    def __init__(self, num_text='1', den_text='2', **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(70), dp(80))
        
        # Numerador
        self.numerador = TextInput(
            text=num_text,
            font_size=dp(18),
            multiline=False,
            halign='center',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            size_hint=(0.8, 0.35),
            pos_hint={'center_x': 0.5, 'top': 0.9}
        )
        
        # Denominador
        self.denominador = TextInput(
            text=den_text,
            font_size=dp(18),
            multiline=False,
            halign='center',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            size_hint=(0.8, 0.35),
            pos_hint={'center_x': 0.5, 'y': 0.1}
        )
        
        self.add_widget(self.numerador)
        self.add_widget(self.denominador)
        
        # Línea de fracción
        with self.canvas.after:
            Color(0, 0, 0, 1)
            self.linea = Line(points=[0, 0, 0, 0], width=2)
        
        self.bind(pos=self.actualizar_linea, size=self.actualizar_linea)
        self.numerador.bind(text=self.on_valor_cambiado)
        self.denominador.bind(text=self.on_valor_cambiado)
    
    def on_valor_cambiado(self, instance, value):
        if self.parent and hasattr(self.parent, 'actualizar_resultado'):
            Clock.unschedule(self.parent.actualizar_resultado)
            Clock.schedule_once(self.parent.actualizar_resultado, 0.1)
    
    def actualizar_linea(self, *args):
        if hasattr(self, 'linea'):
            centro_y = self.y + self.height * 0.5
            self.linea.points = [
                self.x + dp(8), 
                centro_y,
                self.x + self.width - dp(8), 
                centro_y
            ]
    
    def get_valores(self):
        try:
            num = int(self.numerador.text) if self.numerador.text else 0
            den = int(self.denominador.text) if self.denominador.text else 1
            return num, den
        except:
            return 0, 1

class FractionVisual(RelativeLayout):
    """Widget para mostrar fracciones en formato libro (solo lectura)"""
    def __init__(self, num='?', den='?', **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(70), dp(80))
        
        # Numerador
        self.num_label = Label(
            text=str(num),
            font_size=dp(20),
            color=(0, 0, 0, 1),
            bold=True,
            size_hint=(0.8, 0.35),
            pos_hint={'center_x': 0.5, 'top': 0.9}
        )
        
        # Denominador
        self.den_label = Label(
            text=str(den),
            font_size=dp(20),
            color=(0, 0, 0, 1),
            bold=True,
            size_hint=(0.8, 0.35),
            pos_hint={'center_x': 0.5, 'y': 0.1}
        )
        
        self.add_widget(self.num_label)
        self.add_widget(self.den_label)
        
        # Línea de fracción
        with self.canvas:
            Color(0, 0, 0, 1)
            self.linea = Line(points=[0, 0, 0, 0], width=2)
        
        self.bind(pos=self.actualizar_linea, size=self.actualizar_linea)
    
    def actualizar_linea(self, *args):
        if hasattr(self, 'linea'):
            centro_y = self.y + self.height * 0.5
            self.linea.points = [
                self.x + dp(8), 
                centro_y,
                self.x + self.width - dp(8), 
                centro_y
            ]
    
    def set_valores(self, num, den):
        self.num_label.text = str(num)
        self.den_label.text = str(den)
        self.actualizar_linea()

class FraccionesLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(15)
        
        # Título
        titulo = Label(
            text='OPERACIONES CON FRACCIONES',
            size_hint=(1, 0.1),
            color=get_color_from_hex('#f39c12'),
            font_size=dp(16),
            bold=True,
            halign='center'
        )
        self.add_widget(titulo)
        
        # Contenedor principal de la expresión
        expresion_container = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.35),
            spacing=dp(5)
        )
        
        # Fondo gris para el área de expresión
        with expresion_container.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.bg_rect = Rectangle(pos=expresion_container.pos, size=expresion_container.size)
        expresion_container.bind(pos=self.actualizar_fondo, size=self.actualizar_fondo)
        
        # Espaciador izquierdo
        expresion_container.add_widget(Widget(size_hint_x=0.1))
        
        # Fracción 1
        self.fraccion1 = FractionInput('1', '5')
        expresion_container.add_widget(self.fraccion1)
        
        # Operador - Centrado perfectamente con la línea de fracción
        operador_box = BoxLayout(
            orientation='vertical',
            size_hint=(None, 1),
            width=dp(40)
        )
        # Espaciador superior para centrar el operador
        operador_box.add_widget(Widget(size_hint_y=0.45))
        self.operador_label = Label(
            text='+',
            font_size=dp(28),
            color=get_color_from_hex('#f39c12'),
            size_hint_y=0.1,
            bold=True
        )
        operador_box.add_widget(self.operador_label)
        operador_box.add_widget(Widget(size_hint_y=0.45))
        expresion_container.add_widget(operador_box)
        
        # Fracción 2
        self.fraccion2 = FractionInput('5', '6')
        expresion_container.add_widget(self.fraccion2)
        
        # Signo igual - Centrado perfectamente
        igual_box = BoxLayout(
            orientation='vertical',
            size_hint=(None, 1),
            width=dp(40)
        )
        igual_box.add_widget(Widget(size_hint_y=0.45))
        self.igual_label = Label(
            text='=',
            font_size=dp(28),
            color=get_color_from_hex('#f39c12'),
            size_hint_y=0.1,
            bold=True
        )
        igual_box.add_widget(self.igual_label)
        igual_box.add_widget(Widget(size_hint_y=0.45))
        expresion_container.add_widget(igual_box)
        
        # Fracción resultado
        self.fraccion_resultado = FractionVisual('1', '5')
        expresion_container.add_widget(self.fraccion_resultado)
        
        # Espaciador derecho
        expresion_container.add_widget(Widget(size_hint_x=0.1))
        
        self.add_widget(expresion_container)
        
        # Línea separadora
        linea = Widget(size_hint=(1, None), height=dp(2))
        with linea.canvas:
            Color(0.8, 0.8, 0.8, 1)
            Rectangle(pos=linea.pos, size=linea.size)
        linea.bind(pos=self.actualizar_linea_sep, size=self.actualizar_linea_sep)
        self.add_widget(linea)
        
        # Selector de operación
        ops_label = Label(
            text='SELECCIÓN OPERACIÓN:',
            size_hint=(1, 0.08),
            color=get_color_from_hex('#f39c12'),
            font_size=dp(14),
            halign='left',
            bold=True
        )
        ops_label.bind(size=ops_label.setter('text_size'))
        self.add_widget(ops_label)
        
        # Botones de operación
        ops = BoxLayout(size_hint=(1, 0.15), spacing=dp(10))
        operaciones = [
            ('+', '#2ecc71'),
            ('-', '#e74c3c'),
            ('×', '#3498db'),
            ('÷', '#f39c12')
        ]
        
        for texto, color in operaciones:
            btn = Button(
                text=texto,
                font_size=dp(24),
                background_color=get_color_from_hex(color),
                background_normal='',
                bold=True,
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=lambda x, o=texto: self.cambiar_operador(o))
            ops.add_widget(btn)
        
        self.add_widget(ops)
        
        # Botones de acción
        action_buttons = BoxLayout(size_hint=(1, 0.12), spacing=dp(10))
        
        btn_limpiar = Button(
            text="LIMPIAR TODO",
            background_color=get_color_from_hex('#7f8c8d'),
            background_normal='',
            font_size=dp(14),
            bold=True,
            color=(1, 1, 1, 1)
        )
        btn_limpiar.bind(on_press=self.limpiar_todo)
        
        btn_historial = Button(
            text="LIMPIAR HISTORIAL",
            background_color=get_color_from_hex('#c0392b'),
            background_normal='',
            font_size=dp(14),
            bold=True,
            color=(1, 1, 1, 1)
        )
        btn_historial.bind(on_press=self.limpiar_historial)
        
        action_buttons.add_widget(btn_limpiar)
        action_buttons.add_widget(btn_historial)
        self.add_widget(action_buttons)
        
        # Instrucciones
        instrucciones = Label(
            text='Escriba sobre numerador y denominador - Resultado automático',
            size_hint=(1, 0.05),
            color=get_color_from_hex('#7f8c8d'),
            font_size=dp(11)
        )
        self.add_widget(instrucciones)
        
        # Actualización inicial
        Clock.schedule_once(lambda dt: self.actualizar_resultado(), 0.5)
    
    def actualizar_fondo(self, *args):
        self.bg_rect.pos = self.parent.pos if self.parent else (0, 0)
        self.bg_rect.size = self.parent.size if self.parent else (0, 0)
    
    def actualizar_linea_sep(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def cambiar_operador(self, operador):
        """Cambia el operador y actualiza resultado"""
        self.operador_label.text = operador
        self.actualizar_resultado()
    
    def actualizar_resultado(self, *args):
        """Calcula y actualiza el resultado automáticamente"""
        try:
            # Obtener valores
            n1, d1 = self.fraccion1.get_valores()
            n2, d2 = self.fraccion2.get_valores()
            
            if d1 == 0 or d2 == 0:
                self.fraccion_resultado.set_valores('ERR', '0')
                return
            
            op = self.operador_label.text
            
            # Realizar operación según el operador seleccionado
            if op == '+':
                nr, dr = n1*d2 + n2*d1, d1*d2
            elif op == '-':
                nr, dr = n1*d2 - n2*d1, d1*d2
            elif op == '×':
                nr, dr = n1*n2, d1*d2
            elif op == '÷':
                nr, dr = n1*d2, d1*n2
            else:
                return
            
            # Simplificar fracción
            if nr != 0:
                mcd = math.gcd(abs(nr), abs(dr))
                if mcd != 0:
                    ns, ds = nr//mcd, dr//mcd
                else:
                    ns, ds = nr, dr
            else:
                ns, ds = 0, 1
            
            # Ajustar signo
            if ds < 0:
                ns, ds = -ns, -ds
            
            # Actualizar resultado visual
            self.fraccion_resultado.set_valores(ns, ds)
            
            # Guardar en historial
            app = App.get_running_app()
            if hasattr(app, 'guardar_en_historial'):
                app.guardar_en_historial(f"Fracción: {n1}/{d1} {op} {n2}/{d2} = {ns}/{ds}")
            
        except Exception as e:
            print(f"Error: {e}")
            self.fraccion_resultado.set_valores('ERR', '?')
    
    def limpiar_todo(self, instance):
        """Limpia todas las fracciones"""
        self.fraccion1.numerador.text = '1'
        self.fraccion1.denominador.text = '2'
        self.fraccion2.numerador.text = '1'
        self.fraccion2.denominador.text = '3'
        self.operador_label.text = '+'
        self.fraccion_resultado.set_valores('?', '?')
    
    def limpiar_historial(self, instance):
        """Limpia el historial"""
        app = App.get_running_app()
        if hasattr(app, 'limpiar_historial'):
            app.limpiar_historial(instance)

class CalculadoraKivySimple(App):
    def build(self):
        self.title = "CALCULADORA MATEMÁTICA PRO"
        Window.clearcolor = (1, 1, 1, 1)  # Fondo blanco
        Window.minimum_width = dp(550)
        Window.minimum_height = dp(700)
        
        main_layout = BoxLayout(orientation='vertical', spacing=dp(2))
        
        # Título principal
        title = Label(
            text='CALCULADORA MATEMÁTICA PRO',
            size_hint=(1, 0.08),
            font_size=dp(20),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        main_layout.add_widget(title)
        
        # Panel de pestañas
        self.tab_panel = TabbedPanel(do_default_tab=False)
        self.tab_panel.background_color = (1, 1, 1, 1)
        self.tab_panel.tab_width = dp(120)
        self.tab_panel.tab_height = dp(35)
        
        # Pestañas
        tab1 = TabbedPanelItem(text='BÁSICA')
        self.setup_basica(tab1)
        
        tab2 = TabbedPanelItem(text='FRACCIONES')
        self.setup_fracciones(tab2)
        
        tab3 = TabbedPanelItem(text='ECUACIONES')
        self.setup_ecuaciones(tab3)
        
        self.tab_panel.add_widget(tab1)
        self.tab_panel.add_widget(tab2)
        self.tab_panel.add_widget(tab3)
        
        main_layout.add_widget(self.tab_panel)
        
        # Historial
        historial_frame = BoxLayout(orientation='vertical', size_hint=(1, 0.15))
        historial_label = Label(
            text='HISTORIAL',
            size_hint=(1, 0.15),
            color=get_color_from_hex('#f39c12'),
            font_size=dp(12),
            halign='left',
            bold=True
        )
        historial_label.bind(size=historial_label.setter('text_size'))
        
        self.historial_text = TextInput(
            text='', 
            font_size=dp(11),
            readonly=True,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(8), dp(5)]
        )
        historial_frame.add_widget(historial_label)
        historial_frame.add_widget(self.historial_text)
        main_layout.add_widget(historial_frame)
        
        self.cargar_historial()
        return main_layout

    def setup_basica(self, tab):
        layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        
        # Display
        self.display = TextInput(
            text='0', 
            font_size=dp(32), 
            readonly=True, 
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            size_hint=(1, 0.15), 
            padding=[dp(15), dp(10)],
            halign='right'
        )
        layout.add_widget(self.display)
        
        # Teclado numérico
        grid = GridLayout(cols=4, spacing=dp(3), padding=dp(3))
        
        botones = [
            ('C', self.limpiar, '#e74c3c'),
            ('←', self.borrar, '#e74c3c'),
            ('%', self.porcentaje, '#f39c12'),
            ('/', lambda x: self.agregar_op('/'), '#f39c12'),
            ('7', lambda x: self.agregar_num('7'), '#3498db'),
            ('8', lambda x: self.agregar_num('8'), '#3498db'),
            ('9', lambda x: self.agregar_num('9'), '#3498db'),
            ('*', lambda x: self.agregar_op('*'), '#f39c12'),
            ('4', lambda x: self.agregar_num('4'), '#3498db'),
            ('5', lambda x: self.agregar_num('5'), '#3498db'),
            ('6', lambda x: self.agregar_num('6'), '#3498db'),
            ('-', lambda x: self.agregar_op('-'), '#f39c12'),
            ('1', lambda x: self.agregar_num('1'), '#3498db'),
            ('2', lambda x: self.agregar_num('2'), '#3498db'),
            ('3', lambda x: self.agregar_num('3'), '#3498db'),
            ('+', lambda x: self.agregar_op('+'), '#f39c12'),
            ('0', lambda x: self.agregar_num('0'), '#3498db'),
            ('.', lambda x: self.agregar_num('.'), '#3498db'),
            ('π', self.agregar_pi, '#9b59b6'),
            ('=', self.calcular, '#2ecc71')
        ]
        
        for texto, comando, color in botones:
            btn = Button(
                text=texto, 
                font_size=dp(18), 
                background_color=get_color_from_hex(color),
                background_normal='',
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=comando)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        tab.add_widget(layout)

    def setup_fracciones(self, tab):
        fracciones_layout = FraccionesLayout()
        tab.add_widget(fracciones_layout)

    def setup_ecuaciones(self, tab):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        titulo = Label(
            text='ECUACIÓN LINEAL: ax + b = c',
            font_size=dp(18),
            color=get_color_from_hex('#f39c12'),
            size_hint=(1, 0.1),
            bold=True
        )
        layout.add_widget(titulo)
        
        input_layout = GridLayout(cols=2, spacing=dp(15), size_hint=(1, 0.25))
        input_layout.add_widget(Label(text='a =', font_size=dp(16), color=(0, 0, 0, 1)))
        self.eq_a = TextInput(text='1', multiline=False, halign='center', font_size=dp(18))
        input_layout.add_widget(self.eq_a)
        input_layout.add_widget(Label(text='b =', font_size=dp(16), color=(0, 0, 0, 1)))
        self.eq_b = TextInput(text='0', multiline=False, halign='center', font_size=dp(18))
        input_layout.add_widget(self.eq_b)
        input_layout.add_widget(Label(text='c =', font_size=dp(16), color=(0, 0, 0, 1)))
        self.eq_c = TextInput(text='0', multiline=False, halign='center', font_size=dp(18))
        input_layout.add_widget(self.eq_c)
        layout.add_widget(input_layout)
        
        btn = Button(
            text="RESOLVER ECUACIÓN",
            size_hint=(1, 0.12),
            background_color=get_color_from_hex('#9b59b6'),
            background_normal='',
            font_size=dp(14),
            bold=True,
            color=(1, 1, 1, 1)
        )
        btn.bind(on_press=self.resolver_ecuacion)
        layout.add_widget(btn)
        
        resultado_box = BoxLayout(orientation='vertical', size_hint=(1, 0.15))
        resultado_box.add_widget(Label(text='RESULTADO:', color=get_color_from_hex('#f39c12'), font_size=dp(14)))
        self.res_eq = Label(text='x = ?', font_size=dp(24), color=get_color_from_hex('#2ecc71'), bold=True)
        resultado_box.add_widget(self.res_eq)
        layout.add_widget(resultado_box)
        
        tab.add_widget(layout)

    # --- LÓGICA GENERAL ---
    def agregar_num(self, n):
        if self.display.text == '0':
            self.display.text = n
        else:
            self.display.text += n
    
    def agregar_op(self, o):
        if self.display.text and self.display.text[-1] not in '+-*/.':
            self.display.text += o
    
    def agregar_pi(self, inst):
        if self.display.text == '0':
            self.display.text = '3.1416'
        else:
            self.display.text += '3.1416'
    
    def limpiar(self, inst):
        self.display.text = '0'
    
    def borrar(self, inst):
        self.display.text = self.display.text[:-1] or '0'
    
    def porcentaje(self, inst):
        try:
            valor = float(self.display.text)
            self.display.text = str(valor/100)
        except:
            self.display.text = 'Error'
    
    def calcular(self, inst):
        try:
            expresion = self.display.text
            resultado = eval(expresion)
            self.display.text = str(resultado)
        except:
            self.display.text = 'Error'
    
    def resolver_ecuacion(self, inst):
        try:
            a = float(self.eq_a.text)
            b = float(self.eq_b.text)
            c = float(self.eq_c.text)
            
            if a == 0:
                if abs(b - c) < 0.0001:
                    self.res_eq.text = "x = infinitas soluciones"
                else:
                    self.res_eq.text = "Sin solución"
            else:
                x = (c - b) / a
                x = round(x, 4)
                self.res_eq.text = f"x = {x}"
        except:
            self.res_eq.text = "Error en datos"
    
    def guardar_en_historial(self, texto):
        t = datetime.now().strftime("%H:%M:%S")
        entrada = f"[{t}] {texto}\n"
        self.historial_text.text = entrada + self.historial_text.text
        
        # Limitar a 20 líneas
        lineas = self.historial_text.text.split('\n')
        if len(lineas) > 21:
            self.historial_text.text = '\n'.join(lineas[:21])
        
        try:
            with open('historial.txt', 'w') as f:
                f.write(self.historial_text.text)
        except:
            pass
    
    def cargar_historial(self):
        try:
            if os.path.exists('historial.txt'):
                with open('historial.txt', 'r') as f:
                    self.historial_text.text = f.read()
        except:
            pass
    
    def limpiar_historial(self, instance):
        self.historial_text.text = ""
        try:
            if os.path.exists('historial.txt'):
                os.remove('historial.txt')
        except:
            pass

if __name__ == '__main__':
    CalculadoraKivySimple().run()