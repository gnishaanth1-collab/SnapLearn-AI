from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtCore import QDate
from app.database import db
from app.services.document_service import extract_text
from app.services.ai_service import summarize, answer_question
from app.services.quiz_service import generate_quiz
from app.services.planner_service import make_plan
from app.services.qaihub_service import diagnostics, benchmark
from app.services.report_service import create_report

class MainWindow(QMainWindow):
    def __init__(self,user):
        super().__init__(); self.user=user; self.current_doc=None; self.quiz=[]; self.q_index=0; self.score=0
        self.setWindowTitle("SnapLearn AI"); self.resize(1250,780); self.build()

    def build(self):
        root=QWidget(); self.setCentralWidget(root); h=QHBoxLayout(root); side=QVBoxLayout()
        t=QLabel("SNAPLEARN AI"); t.setStyleSheet("font-size:22px;font-weight:bold;"); side.addWidget(t)
        for txt,fn in [("Dashboard",self.dashboard),("My Materials",self.materials),("AI Study Assistant",self.assistant),("Quiz",self.quiz_page),("Flashcards",self.flashcards),("Study Planner",self.planner),("Analytics",self.analytics),("Snapdragon / AI Hub",self.hardware)]:
            b=QPushButton(txt); b.clicked.connect(fn); side.addWidget(b)
        side.addStretch(); b=QPushButton("Logout"); b.clicked.connect(self.logout); side.addWidget(b)
        h.addLayout(side,1); self.content=QVBoxLayout(); h.addLayout(self.content,4); self.dashboard()

    def clear(self):
        while self.content.count():
            x=self.content.takeAt(0)
            if x.widget(): x.widget().deleteLater()

    def heading(self,s):
        x=QLabel(s); x.setStyleSheet("font-size:26px;font-weight:bold;"); self.content.addWidget(x)

    def dashboard(self):
        self.clear(); self.heading(f"Good day, {self.user['name']}!")
        with db() as c:
            docs=c.execute("SELECT COUNT(*) n FROM documents WHERE user_id=?",(self.user["id"],)).fetchone()["n"]
            qs=c.execute("SELECT COUNT(*) n FROM quiz_attempts WHERE user_id=?",(self.user["id"],)).fetchone()["n"]
            mins=c.execute("SELECT COALESCE(SUM(minutes),0) n FROM study_sessions WHERE user_id=?",(self.user["id"],)).fetchone()["n"]
        for s in [f"Documents: {docs}",f"Quiz attempts: {qs}",f"Study time: {mins} minutes"]:
            x=QLabel(s); x.setStyleSheet("font-size:20px;padding:15px;"); self.content.addWidget(x)
        self.content.addWidget(QLabel("● ON-DEVICE / LOCAL-FIRST MODE — documents stay on this PC."))
        for txt,fn in [("Upload Material",self.upload),("Ask AI",self.assistant),("Generate Quiz",self.quiz_page)]:
            b=QPushButton(txt); b.clicked.connect(fn); self.content.addWidget(b)

    def upload(self):
        path,_=QFileDialog.getOpenFileName(self,"Select material","","Documents (*.pdf *.docx *.pptx *.txt)")
        if not path:return
        try:
            text=extract_text(path)
            if len(text.strip())<20: raise ValueError("The file contains too little readable text.")
            with db() as c:c.execute("INSERT INTO documents(user_id,name,path,content) VALUES(?,?,?,?)",(self.user["id"],Path(path).name,path,text))
            QMessageBox.information(self,"Imported",f"Imported {Path(path).name}"); self.materials()
        except Exception as e: QMessageBox.critical(self,"Import error",str(e))

    def materials(self):
        self.clear(); self.heading("My Materials"); b=QPushButton("＋ Upload Material"); b.clicked.connect(self.upload); self.content.addWidget(b)
        self.docs=QListWidget(); self.content.addWidget(self.docs)
        with db() as c: rows=c.execute("SELECT * FROM documents WHERE user_id=? ORDER BY id DESC",(self.user["id"],)).fetchall()
        for r in rows:
            i=QListWidgetItem(r["name"]); i.setData(Qt.UserRole,dict(r)); self.docs.addItem(i)
        self.docs.itemClicked.connect(lambda i:self.select_doc(i.data(Qt.UserRole)))

    def select_doc(self,d):
        self.current_doc=d; self.materials_detail()

    def materials_detail(self):
        self.clear(); self.heading(self.current_doc["name"])
        for txt,fn in [("AI Summary",self.summary_current),("Ask About This Document",self.assistant),("Generate Quiz",self.quiz_page),("Generate Flashcards",self.flashcards)]:
            b=QPushButton(txt); b.clicked.connect(fn); self.content.addWidget(b)
        out=QTextEdit(); out.setReadOnly(True); out.setPlainText(self.current_doc["content"][:10000]); self.content.addWidget(out)

    def get_text(self):
        if self.current_doc:return self.current_doc["content"]
        with db() as c:r=c.execute("SELECT * FROM documents WHERE user_id=? ORDER BY id DESC LIMIT 1",(self.user["id"],)).fetchone()
        return r["content"] if r else ""

    def summary_current(self):
        self.clear(); self.heading("AI Summary"); out=QTextEdit(); out.setReadOnly(True); out.setPlainText(summarize(self.get_text(),10)); self.content.addWidget(out)
        self.current_summary=out.toPlainText(); b=QPushButton("Export PDF Report"); b.clicked.connect(self.export_report); self.content.addWidget(b)

    def assistant(self):
        self.clear(); self.heading("AI Study Assistant"); self.content.addWidget(QLabel("Ask about your uploaded material."))
        q=QLineEdit(); q.setPlaceholderText("Explain TCP congestion control simply"); self.content.addWidget(q)
        out=QTextEdit(); out.setReadOnly(True); self.content.addWidget(out); b=QPushButton("Ask Local AI"); self.content.addWidget(b)
        b.clicked.connect(lambda:out.setPlainText(answer_question(q.text(),self.get_text()) if self.get_text() else "Upload a study material first."))

    def quiz_page(self):
        self.clear(); self.heading("AI Quiz Generator"); text=self.get_text()
        if not text:self.content.addWidget(QLabel("Upload a document first."));return
        if not self.quiz:self.quiz=generate_quiz(text,8); self.q_index=0; self.score=0
        if not self.quiz:self.content.addWidget(QLabel("Not enough text to generate questions."));return
        q=self.quiz[self.q_index]; self.content.addWidget(QLabel(f"Question {self.q_index+1} / {len(self.quiz)}")); l=QLabel(q.question); l.setWordWrap(True); l.setStyleSheet("font-size:18px;"); self.content.addWidget(l)
        for i,opt in enumerate(q.options):
            b=QPushButton(f"{chr(65+i)}. {opt}"); b.clicked.connect(lambda checked=False,idx=i:self.answer_quiz(idx)); self.content.addWidget(b)

    def answer_quiz(self,idx):
        if idx==self.quiz[self.q_index].answer:self.score+=1
        self.q_index+=1
        if self.q_index>=len(self.quiz):
            with db() as c:c.execute("INSERT INTO quiz_attempts(user_id,topic,score,total) VALUES(?,?,?,?)",(self.user["id"],"Uploaded Material",self.score,len(self.quiz)))
            QMessageBox.information(self,"Quiz complete",f"Score: {self.score}/{len(self.quiz)}"); self.quiz=[]; self.q_index=0; self.score=0; self.analytics()
        else:self.quiz_page()

    def flashcards(self):
        self.clear(); self.heading("AI Flashcards"); cards=generate_quiz(self.get_text(),8)
        if not cards:self.content.addWidget(QLabel("Upload more readable material first."));return
        for i,q in enumerate(cards):
            box=QGroupBox(f"Card {i+1}"); lay=QVBoxLayout(box); lay.addWidget(QLabel("Front: "+q.question)); lay.addWidget(QLabel("Answer: "+q.options[q.answer])); lay.addWidget(QLabel("Context: "+q.explanation)); self.content.addWidget(box)

    def planner(self):
        self.clear(); self.heading("Personalized Study Planner"); form=QFormLayout()
        topic=QLineEdit("Computer Networks"); exam=QDateEdit(QDate.currentDate().addDays(14)); exam.setCalendarPopup(True); mins=QSpinBox(); mins.setRange(15,480); mins.setValue(60)
        form.addRow("Topic",topic);form.addRow("Exam date",exam);form.addRow("Minutes/day",mins);self.content.addLayout(form)
        out=QTextEdit();out.setReadOnly(True);self.content.addWidget(out);b=QPushButton("Generate Study Plan");self.content.addWidget(b)
        b.clicked.connect(lambda:out.setPlainText(make_plan(topic.text(),exam.date().toString("yyyy-MM-dd"),mins.value())))

    def analytics(self):
        self.clear(); self.heading("Learning Analytics")
        with db() as c:
            rows=c.execute("SELECT topic,score,total,created_at FROM quiz_attempts WHERE user_id=? ORDER BY id DESC",(self.user["id"],)).fetchall()
            mins=c.execute("SELECT COALESCE(SUM(minutes),0) n FROM study_sessions WHERE user_id=?",(self.user["id"],)).fetchone()["n"]
        self.content.addWidget(QLabel(f"Total study minutes: {mins}"))
        table=QTableWidget(len(rows),4);table.setHorizontalHeaderLabels(["Topic","Score","Total","Date"])
        for i,r in enumerate(rows):
            for j,k in enumerate(["topic","score","total","created_at"]):table.setItem(i,j,QTableWidgetItem(str(r[k])))
        self.content.addWidget(table);self.content.addWidget(QLabel("AI weakness rule: average below 60% → extra revision recommendation."))

    def hardware(self):
        self.clear();self.heading("Snapdragon / Qualcomm AI Hub")
        info=diagnostics();out=QTextEdit();out.setReadOnly(True);out.setPlainText("\n".join(f"{k}: {v}" for k,v in info.items()));self.content.addWidget(out)
        b=QPushButton("Benchmark Configured ONNX Model");self.content.addWidget(b);b.clicked.connect(lambda:QMessageBox.information(self,"Benchmark",str(benchmark())))
        self.content.addWidget(QLabel("Configure SNAPLEARN_ONNX_MODEL with a compatible Qualcomm AI Hub optimized ONNX/QNN model. Only claim NPU acceleration when the real provider/benchmark confirms it."))

    def export_report(self):
        path,_=QFileDialog.getSaveFileName(self,"Save PDF report","SnapLearn_Report.pdf","PDF (*.pdf)")
        if not path:return
        create_report(path,self.user["name"],getattr(self,"current_summary",summarize(self.get_text(),8)),"Use Analytics for quiz history and study time.")
        QMessageBox.information(self,"Exported","PDF report created.")

    def logout(self):
        self.close()
        from .login import LoginWindow
        self.login=LoginWindow();self.login.show()
