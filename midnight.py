from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QTimer
import shutil
import sys
import os
import subprocess

PASTA_LUA = r"C:\Program Files (x86)\Steam\config\stplug-in"
PASTA_MANIFEST = r"C:\Program Files (x86)\Steam\depotcache"
STEAM_PATH = r"C:\Program Files (x86)\Steam\Steam.exe"

class DropWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Midnight")
        self.setGeometry(100, 100, 420, 220)
        self.setFixedSize(420, 220)

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #dcdcdc;
                font-family: Consolas, monospace;
                font-size: 14px;
            }
            QLabel {
                border: 2px dashed #555;
                border-radius: 10px;
                padding: 40px;
                background-color: #252526;
            }
        """)

        # Layout
        layout = QVBoxLayout()
        self.label = QLabel("Arraste arquivos .lua ou .manifest aqui")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("""
                border: 2px dashed #00bfff;
                background-color: #2a2a2a;
                border-radius: 10px;
                padding: 40px;
            """)
            self.label.setText("Solte os arquivos aqui...")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.reset_label()

    def dropEvent(self, event):
        self.reset_label()
        moved = []

        for url in event.mimeData().urls():
            file = url.toLocalFile()
            try:
                if file.endswith(".lua"):
                    destino = os.path.join(PASTA_LUA, os.path.basename(file))
                elif file.endswith(".manifest"):
                    destino = os.path.join(PASTA_MANIFEST, os.path.basename(file))
                else:
                    continue

                if os.path.exists(destino):
                    os.remove(destino)

                shutil.move(file, destino)
                moved.append(f"{os.path.basename(file)} → {destino}")

            except Exception as e:
                self.label.setText(f"❌ Erro: {e}")
                return

        if moved:
            self.label.setText("Arquivos movidos:\n" + "\n".join(moved))
            QTimer.singleShot(500, self.ask_restart_steam)
        else:
            self.label.setText("Nenhum arquivo válido arrastado")

    def reset_label(self):
        self.label.setStyleSheet("""
            border: 2px dashed #555;
            border-radius: 10px;
            padding: 40px;
            background-color: #252526;
        """)
        self.label.setText("Arraste arquivos .lua ou .manifest aqui")

    def ask_restart_steam(self):
        reply = QMessageBox.question(
            self,
            "Reiniciar Steam",
            "Arquivos movidos com sucesso!\nDeseja reiniciar a Steam agora?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.restart_steam()

    def restart_steam(self):
        try:
            subprocess.run("taskkill /f /im Steam.exe", shell=True)
            subprocess.Popen(STEAM_PATH, shell=True)
            self.label.setText("Steam reiniciada com sucesso!")
        except Exception as e:
            self.label.setText(f"Erro ao reiniciar: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DropWindow()
    window.show()
    sys.exit(app.exec())