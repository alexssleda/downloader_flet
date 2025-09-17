import flet as ft
import yt_dlp
from pathlib import Path
import shutil
import threading

def fechar_dialog(page):
    page.dialog.open = False
    page.update()
    
def main(page: ft.Page):
    page.title = 'Downloader'
    page.window_width = 500
    page.window_height = 450
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    img = ft.Image(src='youtube_logo.png', width=200, height=200)
    link = ft.TextField(hint_text="YouTube link", width=300, border_color='white')
    checbox = ft.Checkbox(label="Somente áudio")
    texto = ft.Text('')
    loader = ft.ProgressRing(visible=False, width=50, height=50)

    pasta_download = Path.home() / "Downloads"
    pasta_download.mkdir(exist_ok=True)
    ffmpeg_instalado = shutil.which("ffmpeg") is not None

    def baixar_thread(link_value, audio_only):
        destino = str(pasta_download)
        if audio_only:
            if ffmpeg_instalado:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f"{destino}/%(title)s.%(ext)s",
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'noplaylist': True,
                    'quiet': True,
                }
                mensagem = "Áudio em MP3"
            else:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f"{destino}/%(title)s.%(ext)s",
                    'noplaylist': True,
                    'quiet': True,
                }
                mensagem = "Áudio no formato original (sem FFmpeg)"
        else:
            ydl_opts = {
                'format': 'best',
                'outtmpl': f"{destino}/%(title)s.%(ext)s",
                'noplaylist': True,
                'quiet': True,
            }
            mensagem = "Vídeo"

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link_value])

            # Mostrar popup de sucesso
            dialog = ft.AlertDialog(
                title=ft.Text("Download Concluído!"),
                content=ft.Text(f"Tipo: {mensagem}\nArquivo salvo em: {destino}"),
                actions=[ft.TextButton("Fechar", on_click=lambda e: fechar_dialog(page))],
                modal=True
            )
            page.dialog = dialog
            dialog.open = True
        except Exception as ex:
            dialog = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text(f"Erro durante o download: {ex}"),
                actions=[ft.TextButton("Fechar", on_click=lambda e: fechar_dialog(page))],
                modal=True
            )
            page.dialog = dialog
            dialog.open = True
        finally:
            loader.visible = False
            page.update()

    def baixar(e):
        if not link.value.strip():
            texto.value = "Link vazio"
            page.update()
            return

        loader.visible = True
        page.update()

        # Rodar download em thread separada para não travar a interface
        threading.Thread(target=baixar_thread, args=(link.value, checbox.value), daemon=True).start()

    page.add(
        img,
        ft.Row(controls=[checbox], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            controls=[link, ft.ElevatedButton('Download!', on_click=baixar, color='white')],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=35
        ),
        loader,
        texto
    )

ft.app(target=main)
