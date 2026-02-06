# -*- coding: utf-8 -*-
"""
App Android: Sistema ortogonale 12 numeri su 10 - 10eLotto.
Kivy UI per smartphone.
"""

import os
import sys

# Inclusione path per moduli (necessario in alcuni ambienti Android)
if getattr(sys, 'frozen', False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import sp
from kivy.core.window import Window

from premi import PREMI, premio
from probabilita import tutte_le_probabilità, probabilità_almeno_k_su_10
from logica import (
    colonne_ortogonali_default,
    numeri_colonna,
    vincita_sistema,
    aggiorna_indice_progressione,
    spesa_colpo,
)


def parse_numeri(s, min_val=1, max_val=90):
    try:
        parts = s.strip().split()
        nums = [int(p) for p in parts]
        if any(n < min_val or n > max_val for n in nums):
            return None
        return nums
    except (ValueError, TypeError):
        return None


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = None
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=sp(8), spacing=sp(6))
        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=sp(8), padding=sp(4))
        content.bind(minimum_height=content.setter('height'))

        # Titolo
        title = Label(
            text='12 numeri su 10 - 10eLotto',
            font_size=sp(18),
            size_hint_y=None,
            height=sp(36),
        )
        content.add_widget(title)

        # --- 12 numeri ---
        content.add_widget(Label(text='I tuoi 12 numeri (1-90)', font_size=sp(14), size_hint_y=None, height=sp(24)))
        self.entry_numeri = TextInput(
            text='1 5 12 23 34 45 56 67 72 78 82 90',
            multiline=False,
            font_size=sp(14),
            size_hint_y=None,
            height=sp(44),
            input_type='text',
        )
        content.add_widget(self.entry_numeri)
        btn_apply_num = Button(text='Applica numeri', size_hint_y=None, height=sp(44))
        btn_apply_num.bind(on_press=self._applica_numeri)
        content.add_widget(btn_apply_num)

        self.label_colonne = Label(
            text='Applica per vedere le 6 colonne.',
            font_size=sp(12),
            size_hint_y=None,
            height=sp(80),
            halign='left',
            valign='top',
        )
        content.add_widget(self.label_colonne)

        # --- Tipo gioco ---
        content.add_widget(Label(text='Tipo di gioco', font_size=sp(14), size_hint_y=None, height=sp(24)))
        self.spinner_tipo = Spinner(
            text='10eLotto',
            values=('10eLotto', 'Numero Oro', 'Doppio Oro', 'Extra'),
            size_hint_y=None,
            height=sp(44),
        )
        content.add_widget(self.spinner_tipo)

        # --- Progressione ---
        content.add_widget(Label(text='Progressione (importi separati da spazio)', font_size=sp(14), size_hint_y=None, height=sp(24)))
        self.entry_progressione = TextInput(
            text='1 2 3 5 8 13 21',
            multiline=False,
            font_size=sp(14),
            size_hint_y=None,
            height=sp(44),
        )
        content.add_widget(self.entry_progressione)
        btn_prog = Button(text='Applica progressione', size_hint_y=None, height=sp(44))
        btn_prog.bind(on_press=self._applica_progressione)
        content.add_widget(btn_prog)
        self.label_step = Label(text='Step: 1 | Puntata/colonna: 1.00 €', font_size=sp(13), size_hint_y=None, height=sp(28))
        content.add_widget(self.label_step)

        # --- Estrazione ---
        content.add_widget(Label(text='20 numeri estratti (separati da spazio)', font_size=sp(14), size_hint_y=None, height=sp(24)))
        self.entry_estrazione = TextInput(
            text='',
            multiline=False,
            font_size=sp(14),
            size_hint_y=None,
            height=sp(44),
            hint_text='Inserisci 20 numeri',
        )
        content.add_widget(self.entry_estrazione)
        btn_est = Button(text='Registra estrazione', size_hint_y=None, height=sp(48))
        btn_est.bind(on_press=self._registra_estrazione)
        content.add_widget(btn_est)

        # --- Saldo ---
        content.add_widget(Label(text='Saldo', font_size=sp(14), size_hint_y=None, height=sp(24)))
        self.label_saldo = Label(text='Saldo: 0.00 €', font_size=sp(16), size_hint_y=None, height=sp(32), bold=True)
        content.add_widget(self.label_saldo)
        saldo_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=sp(44), spacing=sp(8))
        self.entry_saldo_iniziale = TextInput(text='0', multiline=False, font_size=sp(14), size_hint_x=0.4, height=sp(44))
        saldo_row.add_widget(Label(text='Saldo iniziale:', size_hint_x=0.35, font_size=sp(13)))
        saldo_row.add_widget(self.entry_saldo_iniziale)
        btn_saldo = Button(text='Imposta', size_hint_x=0.25, size_hint_y=None, height=sp(44))
        btn_saldo.bind(on_press=self._imposta_saldo)
        saldo_row.add_widget(btn_saldo)
        content.add_widget(saldo_row)

        # Link a Premi e Probabilità
        nav_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=sp(48), spacing=sp(8))
        btn_premi = Button(text='Tabella premi', size_hint_x=0.5)
        btn_premi.bind(on_press=self._go_premi)
        btn_prob = Button(text='Probabilità', size_hint_x=0.5)
        btn_prob.bind(on_press=self._go_prob)
        nav_row.add_widget(btn_premi)
        nav_row.add_widget(btn_prob)
        content.add_widget(nav_row)

        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def _go_premi(self, *args):
        if self.manager:
            self.manager.current = 'premi'

    def _go_prob(self, *args):
        if self.manager:
            self.manager.current = 'prob'

    def _applica_numeri(self, *args):
        app = App.get_running_app()
        if not app:
            return
        s = self.entry_numeri.text
        nums = parse_numeri(s)
        if nums is None or len(nums) != 12:
            self._popup('Attenzione', 'Inserisci 12 numeri tra 1 e 90.')
            return
        app.numeri_12 = nums
        lines = []
        for i, col_indici in enumerate(app.colonne):
            numeri_col = numeri_colonna(col_indici, app.numeri_12)
            lines.append('Col %d: %s' % (i + 1, str(numeri_col)))
        self.label_colonne.text = '\n'.join(lines)

    def _applica_progressione(self, *args):
        app = App.get_running_app()
        if not app:
            return
        try:
            parts = self.entry_progressione.text.strip().split()
            prog = [float(x.replace(',', '.')) for x in parts if x]
            if not prog:
                raise ValueError('Vuota')
            app.progressione = prog
            if app.indice_progressione >= len(app.progressione):
                app.indice_progressione = max(0, len(app.progressione) - 1)
            self._aggiorna_step(app)
        except ValueError:
            self._popup('Attenzione', 'Progressione non valida.')

    def _aggiorna_step(self, app):
        if not app.progressione:
            self.label_step.text = 'Step: -'
            return
        idx = min(app.indice_progressione, len(app.progressione) - 1)
        p = app.progressione[idx]
        tot = p * 6
        self.label_step.text = 'Step %d/%d | %.2f €/col | Tot: %.2f €' % (idx + 1, len(app.progressione), p, tot)

    def _imposta_saldo(self, *args):
        app = App.get_running_app()
        if not app:
            return
        try:
            app.saldo = float(self.entry_saldo_iniziale.text.replace(',', '.'))
            self.label_saldo.text = 'Saldo: %+.2f €' % app.saldo
        except ValueError:
            self._popup('Attenzione', 'Numero non valido.')

    def _registra_estrazione(self, *args):
        app = App.get_running_app()
        if not app:
            return
        estratti = parse_numeri(self.entry_estrazione.text, 1, 90)
        if estratti is None or len(estratti) != 20:
            self._popup('Attenzione', 'Inserisci 20 numeri (1-90).')
            return
        if len(app.numeri_12) != 12:
            self._popup('Attenzione', 'Applica prima i 12 numeri.')
            return
        if not app.progressione:
            self._popup('Attenzione', 'Imposta la progressione.')
            return
        puntata = app.progressione[min(app.indice_progressione, len(app.progressione) - 1)]
        spesa = spesa_colpo(app.progressione, app.indice_progressione, 6)
        vincita = vincita_sistema(app.numeri_12, app.colonne, estratti, self.spinner_tipo.text, puntata)
        saldo_prima = app.saldo
        app.saldo += vincita - spesa
        app.indice_progressione = aggiorna_indice_progressione(
            app.indice_progressione, app.progressione, vincita, spesa, saldo_prima, True
        )
        app.estrazioni.append(estratti[:])
        self.label_saldo.text = 'Saldo: %+.2f € (vincita: %.2f, spesa: %.2f)' % (app.saldo, vincita, spesa)
        self._aggiorna_step(app)
        self.entry_estrazione.text = ''
        self._popup('Estrazione registrata', 'Vincita: %.2f €\nSpesa: %.2f €\nSaldo: %+.2f €' % (vincita, spesa, app.saldo))

    def _popup(self, title, msg):
        p = Popup(title=title, content=Label(text=msg, font_size=sp(14)), size_hint=(0.85, 0.4))
        p.open()


class PremiScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=sp(4), padding=sp(4))
        grid.bind(minimum_height=grid.setter('height'))
        headers = ['N.vincenti', '10eLotto', 'Numero Oro', 'Doppio Oro', 'Extra']
        for h in headers:
            grid.add_widget(Label(text=h, font_size=sp(11), size_hint_y=None, height=sp(28)))
        for k in range(10, -1, -1):
            grid.add_widget(Label(text=str(k), font_size=sp(11), size_hint_y=None, height=sp(24)))
            for nome in ['10eLotto', 'Numero Oro', 'Doppio Oro', 'Extra']:
                v = PREMI[nome].get(k, 0)
                if v == 0:
                    txt = '-'
                elif v >= 1_000_000:
                    txt = '€%.1fM' % (v / 1_000_000)
                else:
                    txt = '€%s' % ('%d' % v)
                grid.add_widget(Label(text=txt, font_size=sp(10), size_hint_y=None, height=sp(24)))
        scroll.add_widget(grid)
        btn = Button(text='Indietro', size_hint_y=None, height=sp(48))
        btn.bind(on_press=lambda *a: setattr(self.manager, 'current', 'main') if self.manager else None)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(scroll)
        layout.add_widget(btn)
        self.add_widget(layout)


class ProbScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = ScrollView()
        text = Label(
            font_size=sp(12),
            size_hint_y=None,
            halign='left',
            valign='top',
        )
        probs = tutte_le_probabilità()
        lines = ['Prob. esattamente k numeri su 10:\n']
        for k in range(11):
            p = probs[k]
            lines.append('  k=%2d  P=%.6f  (%.4f%%)' % (k, p, p * 100))
        lines.append('\nProb. almeno k numeri:\n')
        for k in [6, 7, 8, 9, 10]:
            p = probabilità_almeno_k_su_10(k)
            lines.append('  almeno %d  P=%.6f  (%.4f%%)' % (k, p, p * 100))
        text.text = '\n'.join(lines)
        text.height = sp(600)
        scroll.add_widget(text)
        btn = Button(text='Indietro', size_hint_y=None, height=sp(48))
        btn.bind(on_press=lambda *a: setattr(self.manager, 'current', 'main') if self.manager else None)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(scroll)
        layout.add_widget(btn)
        self.add_widget(layout)


class App10eLottoAndroid(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numeri_12 = []
        self.colonne = colonne_ortogonali_default()
        self.saldo = 0.0
        self.progressione = [1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0]
        self.indice_progressione = 0
        self.estrazioni = []

    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        sm = ScreenManager()
        main = MainScreen(name='main')
        sm.add_widget(main)
        sm.add_widget(PremiScreen(name='premi'))
        sm.add_widget(ProbScreen(name='prob'))
        sm.current = 'main'
        return sm


if __name__ == '__main__':
    App10eLottoAndroid().run()
