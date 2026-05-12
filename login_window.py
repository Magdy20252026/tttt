import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox,
    QSizePolicy,
)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تسجيل الدخول")
        self.setLayoutDirection(Qt.RightToLeft)

        self.shop_name = "اسم المحل"
        self.logo_path = "logo.png"  # ضع صورة الشعار بجانب الملف بهذا الاسم

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)

        # توزيع رأسي لتمركز الكارت
        main_layout.addStretch()

        container = QHBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        container.addStretch()

        self.card = QFrame()
        self.card.setObjectName("loginCard")
        self.card.setMinimumWidth(380)
        self.card.setMaximumWidth(460)
        self.card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(35, 30, 35, 30)
        card_layout.setSpacing(16)
        card_layout.setAlignment(Qt.AlignTop)

        self.title_label = QLabel(self.shop_name)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFixedHeight(120)

        pixmap = QPixmap(self.logo_path)
        if not pixmap.isNull():
            self.logo_label.setPixmap(
                pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.logo_label.setText("شعار المحل")
            self.logo_label.setObjectName("logoPlaceholder")

        subtitle = QLabel("يرجى تسجيل الدخول للوصول إلى النظام")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.username_input.setMinimumHeight(50)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة السر")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(50)

        self.login_button = QPushButton("تسجيل الدخول")
        self.login_button.setMinimumHeight(52)
        self.login_button.clicked.connect(self.handle_login)

        card_layout.addWidget(self.title_label)
        card_layout.addWidget(self.logo_label)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(8)
        card_layout.addWidget(self.login_button)

        container.addWidget(self.card)
        container.addStretch()

        main_layout.addLayout(container)
        main_layout.addStretch()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fff8fb,
                    stop:1 #f3e8ff
                );
                font-family: 'Segoe UI', 'Cairo', sans-serif;
                color: #333333;
            }

            QFrame#loginCard {
                background-color: white;
                border-radius: 24px;
                border: 1px solid #f1d9e6;
                padding: 4px;
            }

            QLabel#titleLabel {
                color: #7a3e65;
                font-size: 30px;
                font-weight: 700;
                margin-bottom: 6px;
                background: transparent;
            }

            QLabel#subtitleLabel {
                color: #8c7a86;
                font-size: 14px;
                margin-bottom: 8px;
                background: transparent;
            }

            QLabel#logoPlaceholder {
                color: #b08aa4;
                font-size: 16px;
                border: 2px dashed #e5c8d8;
                border-radius: 14px;
                background-color: #fff7fa;
            }

            QLineEdit {
                background-color: #fcfcfe;
                border: 1px solid #e6dce5;
                border-radius: 14px;
                padding: 12px 14px;
                font-size: 15px;
                color: #333333;
            }

            QLineEdit:focus {
                border: 2px solid #c0618b;
                background-color: white;
                color: #222222;
            }

            QPushButton {
                background-color: #c0618b;
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 16px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #b4557d;
            }

            QPushButton:pressed {
                background-color: #9d466c;
            }

            QMessageBox {
                background-color: #ffffff;
            }

            QMessageBox QLabel {
                color: #222222;
                background-color: #ffffff;
                font-size: 14px;
            }

            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 32px;
                padding: 6px 12px;
                background-color: #c0618b;
                color: white;
                border-radius: 8px;
                border: none;
                font-weight: 700;
            }

            QMessageBox QPushButton:hover {
                background-color: #b4557d;
            }
        """)

    def show_message(self, title, text, icon):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_message("تنبيه", "يرجى إدخال اسم المستخدم وكلمة السر", QMessageBox.Warning)
            return

        # بيانات مؤقتة للتجربة
        if username == "admin" and password == "1234":
            self.show_message("نجاح", "تم تسجيل الدخول بنجاح", QMessageBox.Information)
        else:
            self.show_message("خطأ", "اسم المستخدم أو كلمة السر غير صحيحة", QMessageBox.Critical)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showMaximized()  # فتح الشاشة بشكل افتراضي ملء الشاشة
    sys.exit(app.exec())