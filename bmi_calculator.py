from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QPainter, QPen
import sys
import math

# Custom widget for analog BMI dial
class BMIDial(QWidget):
    def __init__(self):
        super().__init__()
        self.bmi_value = 0

    def set_bmi_value(self, value):
        self.bmi_value = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define dial dimensions
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 20

        # Draw dial background
        painter.setBrush(QColor("#f1faee"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, radius, radius)

        # Draw colored BMI ranges
        pen = QPen()
        pen.setWidth(10)

        # Draw arcs for BMI ranges
        ranges = [
            (QColor("#457b9d"), 30, 30),  # Blue (Underweight)
            (QColor("#2a9d8f"), 60, 60),  # Green (Normal weight)
            (QColor("#e9c46a"), 120, 60), # Yellow (Overweight)
            (QColor("#f4a261"), 180, 60), # Orange (Obese)
            (QColor("#e63946"), 240, 60)  # Red (Severe obesity)
        ]

        for color, start_angle, span_angle in ranges:
            pen.setColor(color)
            painter.setPen(pen)
            painter.drawArc(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius, start_angle * 16, span_angle * 16)

        # Draw Needle
        if self.bmi_value > 0:
            # Map BMI value to angle (0-180 degrees)
            if self.bmi_value < 18.5:
                angle = 30
                needle_color = QColor("#457b9d")  # Blue
            elif 18.5 <= self.bmi_value < 24.9:
                angle = 90
                needle_color = QColor("#2a9d8f")  # Green
            elif 25 <= self.bmi_value < 29.9:
                angle = 150
                needle_color = QColor("#e9c46a")  # Yellow
            elif 30 <= self.bmi_value < 34.9:
                angle = 210
                needle_color = QColor("#f4a261")  # Orange
            else:
                angle = 270
                needle_color = QColor("#e63946")  # Red

            radian_angle = math.radians(angle)
            needle_length = radius - 10

            # Calculate needle endpoint
            x = center.x() + needle_length * math.cos(radian_angle)
            y = center.y() - needle_length * math.sin(radian_angle)

            # Draw the needle
            pen.setColor(needle_color)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(center, QPointF(x, y))

# Main application window for BMI Calculator
class BMICalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #f1faee;")
        self.init_ui()

    def init_ui(self):
        # Title for the application
        self.label_title = QLabel("BMI Calculator", self)
        self.label_title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1d3557;
        """)
        self.label_title.setAlignment(Qt.AlignCenter)

        # Weight input
        self.label_weight = QLabel("Weight (kg):")
        self.label_weight.setStyleSheet("font-size: 16px; color: #1d3557;")
        self.input_weight = QLineEdit()
        self.input_weight.setStyleSheet("""
            font-size: 16px;
            padding: 8px;
            border: 2px solid #457b9d;
            border-radius: 8px;
        """)

        # Height input
        self.label_height = QLabel("Height (cm):")
        self.label_height.setStyleSheet("font-size: 16px; color: #1d3557;")
        self.input_height = QLineEdit()
        self.input_height.setStyleSheet("""
            font-size: 16px;
            padding: 8px;
            border: 2px solid #457b9d;
            border-radius: 8px;
        """)

        # Button to calculate BMI
        self.button_calculate = QPushButton("Calculate BMI")
        self.button_calculate.setStyleSheet("""
            font-size: 18px;
            color: white;
            background-color: #457b9d;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
        """)
        self.button_calculate.clicked.connect(self.calculate_bmi)

        # BMI Dial
        self.bmi_dial = BMIDial()
        self.bmi_dial.setMinimumSize(300, 300)

        # Label to display results
        self.label_result = QLabel("", self)
        self.label_result.setStyleSheet("""
            font-size: 18px;
            color: #1d3557;
            margin-top: 15px;
        """)
        self.label_result.setAlignment(Qt.AlignCenter)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_weight)
        layout.addWidget(self.input_weight)
        layout.addWidget(self.label_height)
        layout.addWidget(self.input_height)
        layout.addWidget(self.button_calculate)
        layout.addWidget(self.bmi_dial, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_result)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def calculate_bmi(self):
        try:
            weight = float(self.input_weight.text())
            height = float(self.input_height.text()) / 100
            if height <= 0 or weight <= 0:
                raise ValueError("Height and weight must be positive numbers.")
            bmi = weight / (height ** 2)
            self.bmi_dial.set_bmi_value(bmi)
            category = ""
            if bmi < 18.5:
                category = "Underweight (لاغر)"
            elif 18.5 <= bmi < 24.9:
                category = "Normal weight (نرمال)"
            elif 25 <= bmi < 29.9:
                category = "Overweight (در معرض چاقی)"
            elif 30 <= bmi < 34.9:
                category = "Obese (چاق)"
            else:
                category = "Severe Obesity (چاقی شدید)"
                QMessageBox.warning(self, "Warning", "You are in the severe obesity range. Please consult a doctor.")

            self.label_result.setText(f"BMI: {bmi:.2f}\nCategory: {category}")
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers for height and weight.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = BMICalculator()
    calculator.show()
    sys.exit(app.exec_())
