import sys
from PySide6.QtWidgets import QApplication
from app.database import init_db
from app.ui.login import LoginWindow

def main():
    init_db()
    app = QApplication(sys.argv)
    app.setApplicationName("SnapLearn AI")
    app.setStyle("Fusion")
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
