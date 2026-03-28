import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex

# ТВОЙ URL
URL = "https://controlling-browser-default-rtdb.europe-west1.firebasedatabase.app/result.json"

class BrowserAdControl(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        layout.add_widget(Label(text="УПРАВЛЕНИЕ ССЫЛКАМИ", font_size='22sp', bold=True))
        
        self.url_input = TextInput(
            hint_text="Вставьте ссылку (http...)",
            multiline=False,
            padding=[15, 15], 
            font_size='16sp'
        )
        layout.add_widget(self.url_input)
        
        # Кнопка ДОБАВИТЬ (в список)
        btn_add = Button(
            text="ДОБАВИТЬ В СПИСОК", 
            background_color=get_color_from_hex('#27ae60'),
            bold=True, size_hint_y=0.4
        )
        btn_add.bind(on_release=self.add_url)
        layout.add_widget(btn_add)

        # Кнопка ОЧИСТИТЬ (всё в базе)
        btn_clear = Button(
            text="ОЧИСТИТЬ ВСЕ", 
            background_color=get_color_from_hex('#e74c3c'),
            bold=True, size_hint_y=0.4
        )
        btn_clear.bind(on_release=self.clear_urls)
        layout.add_widget(btn_clear)
        
        self.status = Label(text="Ожидание...", color=get_color_from_hex('#bdc3c7'))
        layout.add_widget(self.status)
        
        return layout

    def add_url(self, instance):
        new_link = self.url_input.text.strip()
        if new_link.startswith("http"):
            try:
                # 1. Сначала получаем текущий список
                current_data = requests.get(URL).json()
                
                # 2. Если данных нет или это не список, создаем новый
                if not isinstance(current_data, list):
                    current_data = []
                
                # 3. Добавляем новую ссылку и отправляем обратно
                if current_data[0] == "https://media1.tenor.com/m/HaxFI-MpgJEAAAAd/el-primo-dance.gif":
                	current_data=[]
                current_data.append(new_link)
                res = requests.put(URL, json=current_data, timeout=10)
                
                if res.status_code == 200:
                    self.status.text = f"Добавлено! Всего ссылок: {len(current_data)}"
                    self.status.color = get_color_from_hex('#2ecc71')
                    self.url_input.text = "" # Очищаем поле ввода
                else:
                    self.status.text = "Ошибка сервера"
            except:
                self.status.text = "Ошибка сети"
        else:
            self.status.text = "Введите корректную ссылку"

    def clear_urls(self, instance):
        try:
            # Отправляем пустой список или null
            res = requests.put(URL, json=["https://media1.tenor.com/m/HaxFI-MpgJEAAAAd/el-primo-dance.gif"], timeout=10)
            if res.status_code == 200:
                self.status.text = "База данных очищена"
                self.status.color = get_color_from_hex('#f1c40f')
        except:
            self.status.text = "Ошибка при очистке"

if __name__ == "__main__":
    BrowserAdControl().run()
