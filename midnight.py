from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
import shutil
import sys
import os

PASTA_LUA = r"C:\Program Files (x86)\Steam\config\stplug-in"
PASTA_MANIFEST = r"C:\Program Files (x86)\Steam\depotcache"

class DropWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mover arquivos .lua e .manifest")
        self.setGeometry(100, 100, 400, 200)
        self.setAcceptDrops(True)

        layout = QVBoxLayout()
        self.label = QLabel("Arraste arquivos .lua ou .manifest aqui")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        moved = []
        for url in event.mimeData().urls():
            file = url.toLocalFile()
            try:
                if file.endswith(".lua"):
                    shutil.move(file, PASTA_LUA)
                    moved.append(file + " → LUA")
                elif file.endswith(".manifest"):
                    shutil.move(file, PASTA_MANIFEST)
                    moved.append(file + " → MANIFEST")
            except Exception as e:
                self.label.setText(f"Erro: {e}")
        if moved:
            self.label.setText("Arquivos movidos:\n" + "\n".join(moved))
        else:
            self.label.setText("Nenhum arquivo valido arrastado")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DropWindow()
    window.show()
    sys.exit(app.exec())
