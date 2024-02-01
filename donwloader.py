import flet as ft
from pytube import YouTube
from time import sleep


def main(page: ft.page):
    page.title = 'Downloader'
    page.window_width = 500
    page.window_height = 450
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    img = ft.Image(src='1384060.png', width=200, height=200)
    link = ft.TextField(hint_text="Youtube link", width=300, border_color='white')
    user = ft.TextField(hint_text="nome de usuário", width=300, border_color='white')
    checbox = ft.Checkbox()
    texto = ft.Text('')

    def baixar(e):
        if user.value == '':
            texto.value = "Nome de usuário vazio"
            page.update()

        elif link.value == '':
            texto.value = "Link vazio"
            page.update()

        else:
            while True:
                try:
                    yt = YouTube(link.value)
                    break
                except:
                    texto.value = "Link invalido!"
                    link.value = ''
                    page.update()
                sleep(10000)

            if checbox.value:
                stream = yt.streams.filter(only_audio=True).first()
                try:
                    stream.download(rf"C:\Users\{user.value}\Music")
                    texto.value = "Donwload concluido!"
                    link.value = ''
                    page.update()
                except:
                    texto.value = "Nome de usuário invalido"
                    page.update()
                    pass

            else:
                stream = yt.streams.get_highest_resolution()
                try:
                    stream.download(rf"C:\Users\{user.value}\Music")
                    link.value = ""
                    texto.value = "Donwload concluido!"
                    page.update()
                except:
                    texto.value = "Nome de usuário invalido"
                    page.update()
                    pass

    page.add(
        img,
        ft.Row(controls=[user, checbox, ft.Text('Somente áudio!')], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=[link, ft.ElevatedButton('Download!', on_click=baixar, color='white')],
               alignment=ft.MainAxisAlignment.CENTER, spacing=35),
        texto)


ft.app(target=main)
