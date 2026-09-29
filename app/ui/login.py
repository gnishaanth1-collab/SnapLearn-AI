from PySide6.QtWidgets import QWidget,QVBoxLayout,QLineEdit,QPushButton,QLabel,QMessageBox,QTabWidget,QFormLayout
from PySide6.QtCore import Qt
from app.database import db
from .main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapLearn AI - Login")
        self.resize(500,420)
        tabs=QTabWidget(); tabs.addTab(self.login_tab(),"Login"); tabs.addTab(self.register_tab(),"Register")
        lay=QVBoxLayout(self)
        title=QLabel("SnapLearn AI"); title.setStyleSheet("font-size:30px;font-weight:bold;")
        lay.addWidget(title); lay.addWidget(QLabel("On-device personalized learning assistant")); lay.addWidget(tabs)
        self.ensure_demo()

    def ensure_demo(self):
        with db() as c:
            if not c.execute("SELECT id FROM users WHERE email=?",("student@snaplearn.local",)).fetchone():
                c.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",("Demo Student","student@snaplearn.local","student123"))

    def login_tab(self):
        w=QWidget(); f=QFormLayout(w)
        self.email=QLineEdit(); self.password=QLineEdit(); self.password.setEchoMode(QLineEdit.Password)
        b=QPushButton("LOGIN"); b.clicked.connect(self.login)
        f.addRow("Email",self.email); f.addRow("Password",self.password); f.addRow(b); return w

    def register_tab(self):
        w=QWidget(); f=QFormLayout(w)
        self.rname=QLineEdit(); self.remail=QLineEdit(); self.rpass=QLineEdit(); self.rpass.setEchoMode(QLineEdit.Password)
        b=QPushButton("CREATE ACCOUNT"); b.clicked.connect(self.register)
        f.addRow("Name",self.rname); f.addRow("Email",self.remail); f.addRow("Password",self.rpass); f.addRow(b); return w

    def login(self):
        with db() as c:
            u=c.execute("SELECT * FROM users WHERE email=? AND password=?",(self.email.text().strip(),self.password.text())).fetchone()
        if not u:
            QMessageBox.warning(self,"Login","Invalid email or password."); return
        self.main=MainWindow(dict(u)); self.main.show(); self.close()

    def register(self):
        try:
            with db() as c:
                c.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",(self.rname.text().strip(),self.remail.text().strip(),self.rpass.text()))
            QMessageBox.information(self,"Register","Account created. Use the Login tab.")
        except Exception as e:
            QMessageBox.warning(self,"Register",str(e))
