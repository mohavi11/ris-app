from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
import math


class RISWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radar_val = 10
        self.thermal_val = 10
        self.magnet_val = 10
        self.auto_mode = False
        self.angle = 0
        self.score = 0

        # لیبل وضعیت که روی صحنه نمایش داده می‌شود
        self.status_label = Label(
            text="🟢 SAFE",
            font_size='20sp',
            size_hint=(None, None),
            size=(200, 40),
        )
        self.add_widget(self.status_label)

        # هر تغییر اندازه/جابه‌جایی ویجت، صحنه دوباره رسم شود
        self.bind(pos=self.update, size=self.update)

        Clock.schedule_interval(self.update, 0.1)

    def update(self, *args):
        if self.auto_mode:
            t = Clock.get_time()
            self.radar_val = 50 + 30 * math.sin(t * 0.5)
            self.thermal_val = 50 + 30 * math.sin(t * 0.7 + 1)
            self.magnet_val = 50 + 30 * math.sin(t * 0.6 + 2)

        self.score = 0
        if self.radar_val > 70:
            self.score += 50
        if self.thermal_val > 60:
            self.score += 30
        if self.magnet_val > 50:
            self.score += 20

        self.angle = (self.angle + 5) % 360
        self.canvas.before.clear()
        self.canvas.after.clear()

        with self.canvas.before:
            # پس‌زمینه
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=self.pos, size=self.size)

            # جاده
            Color(0.4, 0.4, 0.4, 0.5)
            Rectangle(
                pos=(self.x, self.y + self.height * 0.2),
                size=(self.width, self.height * 0.2),
            )

            # خودرو
            if self.score >= 70:
                Color(1, 0.5, 0.5, 1)  # قرمز
            elif self.score >= 40:
                Color(1, 1, 0.5, 1)    # زرد
            else:
                Color(0.5, 0.8, 1, 1)  # آبی
            Rectangle(
                pos=(self.x + self.width * 0.3, self.y + self.height * 0.25),
                size=(self.width * 0.4, self.height * 0.25),
            )

            # رادار (آنتن گردان)
            Color(1, 0, 0, 1)
            Ellipse(
                pos=(self.x + self.width * 0.1, self.y + self.height * 0.75),
                size=(self.width * 0.06, self.height * 0.06),
            )

            # خط آنتن که واقعاً می‌چرخد
            cx = self.x + self.width * 0.13
            cy = self.y + self.height * 0.78
            ax = cx + self.width * 0.08 * math.cos(math.radians(self.angle))
            ay = cy + self.height * 0.08 * math.sin(math.radians(self.angle))
            Color(1, 0, 0, 1)
            from kivy.graphics import Line
            Line(points=[cx, cy, ax, ay], width=2)

            # LEDهای وضعیت (سمت راست)
            if self.score >= 70:
                led_colors = [(1, 0, 0), (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)]
            elif self.score >= 40:
                led_colors = [(0.5, 0.5, 0.5), (1, 1, 0), (0.5, 0.5, 0.5)]
            else:
                led_colors = [(0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0, 1, 0)]
            for i, col in enumerate(led_colors):
                Color(*col, 1)
                Ellipse(
                    pos=(self.x + self.width * 0.85, self.y + self.height * (0.85 - i * 0.08)),
                    size=(self.width * 0.05, self.height * 0.05),
                )

        # متن وضعیت (حالا واقعا رندر می‌شود)
        if self.score >= 70:
            status = "RED ALERT"
        elif self.score >= 40:
            status = "SUSPICIOUS"
        else:
            status = "SAFE"
        self.status_label.text = status
        self.status_label.pos = (self.x + self.width * 0.05, self.y + self.height * 0.88)


class RISApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.widget = RISWidget()

        # اسلایدرها
        sliders = BoxLayout(size_hint=(1, 0.3))
        for name in ['رادار', 'حرارتی', 'مغناطیس']:
            box = BoxLayout(orientation='vertical')
            lbl = Label(text=name, size_hint=(1, 0.3))
            slider = Slider(min=0, max=100, value=10, size_hint=(1, 0.7))
            val_lbl = Label(text='10%', size_hint=(1, 0.2))

            if name == 'رادار':
                slider.bind(value=self.set_radar)
            elif name == 'حرارتی':
                slider.bind(value=self.set_thermal)
            else:
                slider.bind(value=self.set_magnet)

            slider.bind(value=lambda s, v, lbl=val_lbl: setattr(lbl, 'text', f'{int(v)}%'))

            box.add_widget(lbl)
            box.add_widget(slider)
            box.add_widget(val_lbl)
            sliders.add_widget(box)

        # دکمه خودکار
        btn = Button(text='شروع شبیه‌سازی', size_hint=(1, 0.1))
        btn.bind(on_press=self.toggle_auto)

        layout.add_widget(self.widget)
        layout.add_widget(sliders)
        layout.add_widget(btn)
        return layout

    def set_radar(self, instance, value):
        self.widget.radar_val = value

    def set_thermal(self, instance, value):
        self.widget.thermal_val = value

    def set_magnet(self, instance, value):
        self.widget.magnet_val = value

    def toggle_auto(self, instance):
        self.widget.auto_mode = not self.widget.auto_mode
        instance.text = 'توقف' if self.widget.auto_mode else 'شروع شبیه‌سازی'


if __name__ == '__main__':
    RISApp().run()
