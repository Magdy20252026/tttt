import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

NAME_COLUMN = 0
PHONE_COLUMN = 1
TRANSFER_NUMBER_COLUMN = 2
TRANSFER_TYPE_COLUMN = 3
BALANCE_COLUMN = 4
INITIAL_SUPPLIER_BALANCE = 0


class SuppliersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_row = None
        self.setup_ui()

    def setup_ui(self):
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(24)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)

        title_box = QVBoxLayout()
        title_box.setSpacing(6)

        self.page_title = QLabel("إدارة الموردين")
        self.page_title.setObjectName("pageTitle")
        self.page_title.setToolTip("صفحة إدارة الموردين")

        self.page_caption = QLabel("إضافة وتعديل وحذف الموردين من شاشة واحدة")
        self.page_caption.setObjectName("pageCaption")

        title_box.addWidget(self.page_title)
        title_box.addWidget(self.page_caption)
        header_layout.addLayout(title_box)
        header_layout.addStretch()

        self.summary_card = QFrame()
        self.summary_card.setObjectName("summaryCard")
        summary_layout = QVBoxLayout(self.summary_card)
        summary_layout.setContentsMargins(20, 16, 20, 16)
        summary_layout.setSpacing(4)

        summary_title = QLabel("إجمالي الموردين")
        summary_title.setObjectName("summaryTitle")
        self.summary_value = QLabel("0")
        self.summary_value.setObjectName("summaryValue")

        summary_layout.addWidget(summary_title)
        summary_layout.addWidget(self.summary_value)
        header_layout.addWidget(self.summary_card)

        form_card = QFrame()
        form_card.setObjectName("panelCard")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(22, 22, 22, 22)
        form_layout.setSpacing(18)

        fields_layout = QHBoxLayout()
        fields_layout.setSpacing(16)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("اسم المورد")
        fields_layout.addWidget(self.create_field_box("اسم المورد", self.name_input), 2)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("رقم الهاتف")
        fields_layout.addWidget(self.create_field_box("رقم الهاتف", self.phone_input), 1)

        self.transfer_number_input = QLineEdit()
        self.transfer_number_input.setPlaceholderText("رقم التحويل")
        fields_layout.addWidget(self.create_field_box("رقم التحويل", self.transfer_number_input), 1)

        self.transfer_type_input = QComboBox()
        self.transfer_type_input.addItems(["محفظة", "انستا باي"])
        fields_layout.addWidget(self.create_field_box("نوع التحويل", self.transfer_type_input), 1)

        form_layout.addLayout(fields_layout)

        self.status_label = QLabel("جاهز لإضافة مورد جديد")
        self.status_label.setObjectName("statusLabel")
        form_layout.addWidget(self.status_label)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)

        self.add_button = QPushButton("إضافة المورد")
        self.add_button.setObjectName("primaryButton")
        self.add_button.clicked.connect(self.add_supplier)

        self.update_button = QPushButton("حفظ التعديل")
        self.update_button.setObjectName("secondaryButton")
        self.update_button.clicked.connect(self.update_supplier)
        self.update_button.setEnabled(False)

        self.delete_button = QPushButton("حذف المورد")
        self.delete_button.setObjectName("dangerButton")
        self.delete_button.clicked.connect(self.delete_supplier)
        self.delete_button.setEnabled(False)

        self.clear_button = QPushButton("تفريغ الحقول")
        self.clear_button.setObjectName("ghostButton")
        self.clear_button.clicked.connect(self.clear_form)

        actions_layout.addWidget(self.add_button)
        actions_layout.addWidget(self.update_button)
        actions_layout.addWidget(self.delete_button)
        actions_layout.addStretch()
        actions_layout.addWidget(self.clear_button)
        form_layout.addLayout(actions_layout)

        table_card = QFrame()
        table_card.setObjectName("panelCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(22, 22, 22, 22)
        table_layout.setSpacing(16)

        table_header = QHBoxLayout()
        table_header.setSpacing(12)

        table_title = QLabel("جدول الموردين")
        table_title.setObjectName("sectionTitle")
        table_header.addWidget(table_title)
        table_header.addStretch()
        table_layout.addLayout(table_header)

        self.suppliers_table = QTableWidget(0, 5)
        self.suppliers_table.setHorizontalHeaderLabels(
            ["اسم المورد", "رقم الهاتف", "رقم التحويل", "نوع التحويل", "رصيد المورد"]
        )
        self.suppliers_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.suppliers_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.suppliers_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.suppliers_table.verticalHeader().setVisible(False)
        self.suppliers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.suppliers_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.suppliers_table.setAlternatingRowColors(True)
        self.suppliers_table.itemSelectionChanged.connect(self.handle_selection_change)
        table_layout.addWidget(self.suppliers_table)

        page_layout.addLayout(header_layout)
        page_layout.addWidget(form_card)
        page_layout.addWidget(table_card)

    def create_field_box(self, label_text, field_widget):
        container = QFrame()
        container.setObjectName("fieldBox")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QLabel(label_text)
        label.setObjectName("fieldLabel")
        layout.addWidget(label)
        field_widget.setMinimumHeight(48)
        layout.addWidget(field_widget)

        return container

    def show_message(self, title, text, icon):
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    def validate_inputs(self):
        name = self.normalize_name(self.name_input.text())
        phone = self.phone_input.text().strip()
        transfer_number = self.transfer_number_input.text().strip()

        if not name:
            self.show_message("تنبيه", "يرجى إدخال اسم المورد", QMessageBox.Warning)
            self.name_input.setFocus()
            return None

        if not phone:
            self.show_message("تنبيه", "يرجى إدخال رقم الهاتف", QMessageBox.Warning)
            self.phone_input.setFocus()
            return None

        if not transfer_number:
            self.show_message("تنبيه", "يرجى إدخال رقم التحويل", QMessageBox.Warning)
            self.transfer_number_input.setFocus()
            return None

        return {
            "name": name,
            "phone": phone,
            "transfer_number": transfer_number,
            "transfer_type": self.transfer_type_input.currentText(),
        }

    def normalize_name(self, name):
        return " ".join(name.split())

    def format_balance(self, balance):
        return f"{balance:.2f}"

    def supplier_exists(self, name, exclude_row=None):
        normalized_name = self.normalize_name(name).casefold()
        for row in range(self.suppliers_table.rowCount()):
            if exclude_row is not None and row == exclude_row:
                continue
            if (
                self.normalize_name(self.suppliers_table.item(row, NAME_COLUMN).text()).casefold()
                == normalized_name
            ):
                return True
        return False

    def set_row_values(self, row, supplier_data, balance):
        values = [
            supplier_data["name"],
            supplier_data["phone"],
            supplier_data["transfer_number"],
            supplier_data["transfer_type"],
            balance,
        ]

        for column, value in enumerate(values):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            self.suppliers_table.setItem(row, column, item)

    def add_supplier(self):
        supplier_data = self.validate_inputs()
        if not supplier_data:
            return

        if self.supplier_exists(supplier_data["name"]):
            self.show_message("تنبيه", "اسم المورد مسجل بالفعل", QMessageBox.Warning)
            return

        row = self.suppliers_table.rowCount()
        self.suppliers_table.insertRow(row)
        self.set_row_values(row, supplier_data, self.format_balance(INITIAL_SUPPLIER_BALANCE))
        self.update_summary()
        self.clear_form(show_status=False)
        self.status_label.setText(f"تمت إضافة المورد {supplier_data['name']} بنجاح")
        self.show_message("نجاح", "تم حفظ المورد بنجاح", QMessageBox.Information)

    def update_supplier(self):
        if self.selected_row is None:
            self.show_message("تنبيه", "يرجى اختيار مورد من الجدول أولاً", QMessageBox.Warning)
            return

        supplier_data = self.validate_inputs()
        if not supplier_data:
            return

        if self.supplier_exists(supplier_data["name"], exclude_row=self.selected_row):
            self.show_message("تنبيه", "اسم المورد مسجل لمورد آخر", QMessageBox.Warning)
            return

        balance_item = self.suppliers_table.item(self.selected_row, BALANCE_COLUMN)
        balance = (
            balance_item.text()
            if balance_item is not None
            else self.format_balance(INITIAL_SUPPLIER_BALANCE)
        )
        self.set_row_values(self.selected_row, supplier_data, balance)
        self.status_label.setText(f"تم تحديث بيانات المورد {supplier_data['name']}")
        self.show_message("نجاح", "تم تعديل بيانات المورد بنجاح", QMessageBox.Information)

    def delete_supplier(self):
        if self.selected_row is None:
            self.show_message("تنبيه", "يرجى اختيار مورد من الجدول أولاً", QMessageBox.Warning)
            return

        supplier_name = self.suppliers_table.item(self.selected_row, NAME_COLUMN).text()
        confirmation = QMessageBox.question(
            self,
            "تأكيد الحذف",
            f"هل تريد حذف المورد {supplier_name}؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation != QMessageBox.Yes:
            return

        self.suppliers_table.removeRow(self.selected_row)
        self.update_summary()
        self.clear_form(show_status=False)
        self.status_label.setText(f"تم حذف المورد {supplier_name}")
        self.show_message("نجاح", "تم حذف المورد بنجاح", QMessageBox.Information)

    def handle_selection_change(self):
        selected_items = self.suppliers_table.selectedItems()
        if not selected_items:
            return

        self.selected_row = selected_items[0].row()
        self.name_input.setText(self.suppliers_table.item(self.selected_row, NAME_COLUMN).text())
        self.phone_input.setText(self.suppliers_table.item(self.selected_row, PHONE_COLUMN).text())
        self.transfer_number_input.setText(
            self.suppliers_table.item(self.selected_row, TRANSFER_NUMBER_COLUMN).text()
        )
        self.transfer_type_input.setCurrentText(
            self.suppliers_table.item(self.selected_row, TRANSFER_TYPE_COLUMN).text()
        )
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.status_label.setText("يمكنك الآن تعديل المورد المحدد أو حذفه")

    def clear_form(self, show_status=True):
        self.selected_row = None
        self.suppliers_table.clearSelection()
        self.name_input.clear()
        self.phone_input.clear()
        self.transfer_number_input.clear()
        self.transfer_type_input.setCurrentIndex(0)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        if show_status:
            self.status_label.setText("جاهز لإضافة مورد جديد")
        self.name_input.setFocus()

    def update_summary(self):
        self.summary_value.setText(str(self.suppliers_table.rowCount()))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام الإدارة")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 22, 18, 22)
        sidebar_layout.setSpacing(18)

        app_title = QLabel("لوحة التحكم")
        app_title.setObjectName("sidebarTitle")

        app_subtitle = QLabel("إدارة بيانات النظام")
        app_subtitle.setObjectName("sidebarSubtitle")

        self.suppliers_button = QPushButton("الموردين")
        self.suppliers_button.setObjectName("navButton")
        self.suppliers_button.setCheckable(True)
        self.suppliers_button.setChecked(True)
        self.suppliers_button.clicked.connect(self.show_suppliers_page)

        sidebar_layout.addWidget(app_title)
        sidebar_layout.addWidget(app_subtitle)
        sidebar_layout.addSpacing(8)
        sidebar_layout.addWidget(self.suppliers_button)
        sidebar_layout.addStretch()

        content_wrapper = QFrame()
        content_wrapper.setObjectName("contentWrapper")
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(0)

        self.pages = QStackedWidget()
        self.suppliers_page = SuppliersPage()
        self.pages.addWidget(self.suppliers_page)
        content_layout.addWidget(self.pages)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_wrapper, 1)

    def show_suppliers_page(self):
        self.suppliers_button.setChecked(True)
        self.pages.setCurrentWidget(self.suppliers_page)

    def apply_styles(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f5f7fb;
                font-family: 'Segoe UI', 'Cairo', sans-serif;
                color: #1f2937;
                font-size: 14px;
            }

            QFrame#sidebar {
                background-color: #111827;
                border-radius: 28px;
            }

            QLabel#sidebarTitle {
                color: #ffffff;
                font-size: 24px;
                font-weight: 700;
                background: transparent;
            }

            QLabel#sidebarSubtitle {
                color: #cbd5e1;
                font-size: 13px;
                background: transparent;
            }

            QPushButton#navButton {
                min-height: 50px;
                background-color: #7c3aed;
                color: #ffffff;
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: 700;
                text-align: right;
                padding: 0 18px;
            }

            QPushButton#navButton:hover {
                background-color: #6d28d9;
            }

            QPushButton#navButton:checked {
                background-color: #8b5cf6;
            }

            QFrame#contentWrapper,
            QFrame#panelCard,
            QFrame#summaryCard {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 24px;
            }

            QLabel#pageTitle {
                font-size: 28px;
                font-weight: 700;
                color: #111827;
                background: transparent;
            }

            QLabel#pageCaption {
                font-size: 14px;
                color: #6b7280;
                background: transparent;
            }

            QLabel#summaryTitle {
                font-size: 13px;
                color: #6b7280;
                background: transparent;
            }

            QLabel#summaryValue {
                font-size: 28px;
                font-weight: 700;
                color: #7c3aed;
                background: transparent;
            }

            QLabel#fieldLabel,
            QLabel#sectionTitle {
                font-size: 14px;
                font-weight: 700;
                color: #374151;
                background: transparent;
            }

            QLabel#sectionTitle {
                font-size: 18px;
            }

            QLabel#statusLabel {
                color: #7c3aed;
                font-size: 13px;
                background-color: #f5f3ff;
                border: 1px solid #ddd6fe;
                border-radius: 14px;
                padding: 12px 14px;
            }

            QLineEdit,
            QComboBox {
                background-color: #f9fafb;
                border: 1px solid #d1d5db;
                border-radius: 14px;
                padding: 0 14px;
                color: #111827;
            }

            QLineEdit:focus,
            QComboBox:focus {
                border: 2px solid #8b5cf6;
                background-color: #ffffff;
            }

            QComboBox::drop-down {
                border: none;
                width: 28px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #6b7280;
                margin-left: 10px;
            }

            QPushButton#primaryButton,
            QPushButton#secondaryButton,
            QPushButton#dangerButton,
            QPushButton#ghostButton {
                min-height: 48px;
                border-radius: 14px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: 700;
                border: none;
            }

            QPushButton#primaryButton {
                background-color: #7c3aed;
                color: #ffffff;
            }

            QPushButton#primaryButton:hover {
                background-color: #6d28d9;
            }

            QPushButton#secondaryButton {
                background-color: #e0e7ff;
                color: #4338ca;
            }

            QPushButton#secondaryButton:hover {
                background-color: #c7d2fe;
            }

            QPushButton#dangerButton {
                background-color: #fee2e2;
                color: #b91c1c;
            }

            QPushButton#dangerButton:hover {
                background-color: #fecaca;
            }

            QPushButton#ghostButton {
                background-color: #f3f4f6;
                color: #374151;
            }

            QPushButton#ghostButton:hover {
                background-color: #e5e7eb;
            }

            QPushButton:disabled {
                background-color: #e5e7eb;
                color: #9ca3af;
            }

            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                gridline-color: #e5e7eb;
                selection-background-color: #ede9fe;
                selection-color: #111827;
            }

            QHeaderView::section {
                background-color: #f3f4f6;
                color: #374151;
                padding: 14px;
                border: none;
                border-bottom: 1px solid #e5e7eb;
                font-weight: 700;
            }

            QTableWidget::item {
                padding: 12px;
            }

            QMessageBox {
                background-color: #ffffff;
            }

            QMessageBox QLabel {
                color: #111827;
                font-size: 14px;
                min-width: 260px;
            }

            QMessageBox QPushButton {
                min-width: 90px;
                min-height: 34px;
                border-radius: 10px;
                background-color: #7c3aed;
                color: #ffffff;
                font-weight: 700;
                border: none;
                padding: 0 14px;
            }

            QMessageBox QPushButton:hover {
                background-color: #6d28d9;
            }
            """
        )


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تسجيل الدخول")
        self.setLayoutDirection(Qt.RightToLeft)
        self.shop_name = "اسم المحل"
        self.logo_path = "logo.png"
        self.main_window = None
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)
        main_layout.addStretch()

        container = QHBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        container.addStretch()

        self.card = QFrame()
        self.card.setObjectName("loginCard")
        self.card.setMinimumWidth(400)
        self.card.setMaximumWidth(480)
        self.card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(38, 34, 38, 34)
        card_layout.setSpacing(18)
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
            self.logo_label.setText("الشعار")
            self.logo_label.setObjectName("logoPlaceholder")

        self.username_label = QLabel("اسم المستخدم")
        self.username_label.setObjectName("loginFieldLabel")
        self.username_input = QLineEdit()
        self.username_input.setMinimumHeight(50)

        self.password_label = QLabel("كلمة السر")
        self.password_label.setObjectName("loginFieldLabel")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(50)

        self.login_button = QPushButton("تسجيل الدخول")
        self.login_button.setMinimumHeight(52)
        self.login_button.clicked.connect(self.handle_login)

        card_layout.addWidget(self.title_label)
        card_layout.addWidget(self.logo_label)
        card_layout.addSpacing(6)
        card_layout.addWidget(self.username_label)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_label)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.login_button)

        container.addWidget(self.card)
        container.addStretch()

        main_layout.addLayout(container)
        main_layout.addStretch()

    def apply_styles(self):
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #f8fafc,
                    stop: 1 #ede9fe
                );
                font-family: 'Segoe UI', 'Cairo', sans-serif;
                color: #1f2937;
            }

            QFrame#loginCard {
                background-color: #ffffff;
                border-radius: 28px;
                border: 1px solid #e5e7eb;
            }

            QLabel#titleLabel {
                color: #111827;
                font-size: 30px;
                font-weight: 700;
                background: transparent;
            }

            QLabel#logoPlaceholder {
                color: #7c3aed;
                font-size: 18px;
                font-weight: 700;
                border: 2px dashed #c4b5fd;
                border-radius: 18px;
                background-color: #f5f3ff;
            }

            QLabel#loginFieldLabel {
                color: #374151;
                font-size: 14px;
                font-weight: 700;
                background: transparent;
            }

            QLineEdit {
                background-color: #f9fafb;
                border: 1px solid #d1d5db;
                border-radius: 14px;
                padding: 0 14px;
                font-size: 15px;
                color: #111827;
            }

            QLineEdit:focus {
                border: 2px solid #8b5cf6;
                background-color: #ffffff;
            }

            QPushButton {
                background-color: #7c3aed;
                color: #ffffff;
                border: none;
                border-radius: 14px;
                font-size: 16px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #6d28d9;
            }

            QPushButton:pressed {
                background-color: #5b21b6;
            }

            QMessageBox {
                background-color: #ffffff;
            }

            QMessageBox QLabel {
                color: #111827;
                background-color: #ffffff;
                font-size: 14px;
            }

            QMessageBox QPushButton {
                min-width: 90px;
                min-height: 34px;
                padding: 6px 12px;
                background-color: #7c3aed;
                color: #ffffff;
                border-radius: 10px;
                border: none;
                font-weight: 700;
            }

            QMessageBox QPushButton:hover {
                background-color: #6d28d9;
            }
            """
        )

    def show_message(self, title, text, icon):
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setIcon(icon)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_message("تنبيه", "يرجى إدخال اسم المستخدم وكلمة السر", QMessageBox.Warning)
            return

        if username == "admin" and password == "1234":
            self.main_window = MainWindow()
            self.main_window.showMaximized()
            self.close()
            return

        self.show_message("خطأ", "اسم المستخدم أو كلمة السر غير صحيحة", QMessageBox.Critical)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showMaximized()
    sys.exit(app.exec())
