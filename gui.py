import sys
import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class HRDashboard(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Corporate HR People Analytics Dashboard")
        self.setGeometry(100, 50, 1600, 1000)  # Increased size

        self.setStyleSheet("""
        QMainWindow{
            background:white;
        }

        QLabel{
            font-size:15px;
        }

        QPushButton{
            background:#007ACC;
            color:white;
            font-size:14px;
            border-radius:8px;
            padding:10px;
            min-width:150px;
        }

        QPushButton:hover{
            background:#005999;
        }

        QFrame{
            background:#F5F5F5;
            border-radius:10px;
        }

        QLineEdit{
            padding:8px;
            border:2px solid #ccc;
            border-radius:8px;
            font-size:14px;
            min-width:300px;
        }

        QLineEdit:focus{
            border:2px solid #007ACC;
        }
        """)

        self.df = None
        self.createUI()

    def createUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Title
        title = QLabel("Corporate HR People Analytics Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
        font-size:32px;
        font-weight:bold;
        color:#003366;
        padding:10px;
        """)
        layout.addWidget(title)

        # Button Layout
        buttonLayout = QHBoxLayout()
        self.loadBtn = QPushButton("📂 Load Dataset")
        self.dashboardBtn = QPushButton("📊 Generate Dashboard")
        self.exportBtn = QPushButton("💾 Export CSV")
        self.exitBtn = QPushButton("🚪 Exit")

        buttonLayout.addWidget(self.loadBtn)
        buttonLayout.addWidget(self.dashboardBtn)
        buttonLayout.addWidget(self.exportBtn)
        buttonLayout.addWidget(self.exitBtn)
        layout.addLayout(buttonLayout)

        # Search Layout
        searchLayout = QHBoxLayout()
        self.searchBox = QLineEdit()
        self.searchBox.setPlaceholderText("🔍 Search Employee Name...")
        searchButton = QPushButton("Search")
        searchButton.setStyleSheet("min-width:100px;")
        searchLayout.addWidget(self.searchBox)
        searchLayout.addWidget(searchButton)
        layout.addLayout(searchLayout)

        # Cards - 2 rows
        cards = QGridLayout()
        cards.setSpacing(15)
        
        self.totalEmployees = self.createCard("👥 Total Employees", "0", "#3498db")
        self.departments = self.createCard("🏢 Departments", "0", "#2ecc71")
        self.averageSalary = self.createCard("💰 Average Salary", "0", "#e67e22")
        self.activeEmployees = self.createCard("✅ Active Employees", "0", "#9b59b6")
        self.attrition = self.createCard("📉 Attrition Rate", "0%", "#e74c3c")

        cards.addWidget(self.totalEmployees, 0, 0)
        cards.addWidget(self.departments, 0, 1)
        cards.addWidget(self.averageSalary, 0, 2)
        cards.addWidget(self.activeEmployees, 1, 0)
        cards.addWidget(self.attrition, 1, 1)

        layout.addLayout(cards)

        # Chart Area - Make it bigger
        self.figure = Figure(figsize=(16, 8), dpi=100)  # Increased size
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background:white; border:2px solid #ddd; border-radius:10px;")
        self.canvas.setMinimumHeight(600)  # Set minimum height
        layout.addWidget(self.canvas)

        # Footer
        footer = QLabel("© 2026 Corporate HR People Analytics Dashboard | Python + PyQt5")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
        font-size:12px;
        color:gray;
        padding:10px;
        """)
        layout.addWidget(footer)

        self.statusBar().showMessage("Ready")

        # Connect Signals
        self.loadBtn.clicked.connect(self.loadDataset)
        self.dashboardBtn.clicked.connect(self.generateDashboard)
        self.exportBtn.clicked.connect(self.exportCSV)
        self.exitBtn.clicked.connect(self.close)
        searchButton.clicked.connect(self.searchEmployee)

        self.createMenu()

    def createMenu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu("File")
        helpMenu = menubar.addMenu("Help")

        openAction = QAction("Load Dataset", self)
        exportAction = QAction("Export CSV", self)
        exitAction = QAction("Exit", self)
        aboutAction = QAction("About", self)

        fileMenu.addAction(openAction)
        fileMenu.addAction(exportAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        helpMenu.addAction(aboutAction)

        openAction.triggered.connect(self.loadDataset)
        exportAction.triggered.connect(self.exportCSV)
        exitAction.triggered.connect(self.close)
        aboutAction.triggered.connect(
            lambda: QMessageBox.about(
                self,
                "About",
                "Corporate HR People Analytics Dashboard\nDeveloped using Python + PyQt5"
            )
        )

    def createCard(self, title, value, color):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame{{
                background:qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}, stop:1 {color}dd);
                border-radius:15px;
                padding:10px;
            }}
        """)
        frame.setFixedHeight(130)
        frame.setMinimumWidth(200)

        layout = QVBoxLayout()

        titleLabel = QLabel(title)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("""
            color:white;
            font-size:16px;
            font-weight:bold;
            background:transparent;
        """)

        valueLabel = QLabel(value)
        valueLabel.setAlignment(Qt.AlignCenter)
        valueLabel.setStyleSheet("""
            color:white;
            font-size:32px;
            font-weight:bold;
            background:transparent;
        """)

        frame.valueLabel = valueLabel

        layout.addWidget(titleLabel)
        layout.addWidget(valueLabel)
        frame.setLayout(layout)

        return frame

    def loadDataset(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open CSV",
            "",
            "CSV Files (*.csv)"
        )

        if filename:
            try:
                self.df = pd.read_csv(filename)
                self.statusBar().showMessage(f"Dataset Loaded Successfully: {filename}")
                self.updateCards()
                QMessageBox.information(
                    self,
                    "Success",
                    f"Dataset loaded successfully!\nRows: {len(self.df)}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to load dataset:\n{str(e)}"
                )

    def updateCards(self):
        if self.df is None or len(self.df) == 0:
            return

        total = len(self.df)
        departments = self.df["Department"].nunique()
        average = round(self.df["Salary"].mean(), 2)
        active = len(self.df[self.df["Status"] == "Active"])
        attrition = round(
            len(self.df[self.df["Status"] != "Active"]) / total * 100,
            1
        )

        self.totalEmployees.valueLabel.setText(str(total))
        self.departments.valueLabel.setText(str(departments))
        self.averageSalary.valueLabel.setText(f"Rs {average:,.0f}")
        self.activeEmployees.valueLabel.setText(str(active))
        self.attrition.valueLabel.setText(f"{attrition}%")

    def generateDashboard(self):
        if self.df is None or len(self.df) == 0:
            QMessageBox.warning(self, "Error", "Please load a dataset first!")
            return

        self.figure.clear()
        
        # Use a larger figure with better spacing
        self.figure.set_size_inches(16, 8)
        
        # Chart 1: Employees by Department
        ax1 = self.figure.add_subplot(2, 3, 1)
        dept = self.df["Department"].value_counts()
        colors = ["#3498db", "#2ecc71", "#e67e22", "#e74c3c", "#9b59b6", "#1abc9c"]
        bars = ax1.bar(dept.index, dept.values, color=colors[:len(dept)], edgecolor='black', linewidth=0.5)
        ax1.set_title("Employees by Department", fontsize=12, fontweight='bold')
        ax1.set_ylabel("Number of Employees", fontsize=10)
        ax1.tick_params(axis='x', rotation=30, labelsize=9)
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)

        # Chart 2: Employee Status Pie Chart
        ax2 = self.figure.add_subplot(2, 3, 2)
        status = self.df["Status"].value_counts()
        colors_pie = ['#2ecc71' if x == 'Active' else '#e74c3c' for x in status.index]
        wedges, texts, autotexts = ax2.pie(
            status, 
            labels=status.index, 
            autopct="%1.1f%%", 
            startangle=90,
            colors=colors_pie,
            textprops={'fontsize': 10}
        )
        ax2.set_title("Employee Status", fontsize=12, fontweight='bold')
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        # Chart 3: Salary Distribution
        ax3 = self.figure.add_subplot(2, 3, 3)
        ax3.hist(self.df["Salary"], bins=10, color="#3498db", edgecolor="black", linewidth=0.5, alpha=0.7)
        ax3.set_title("Salary Distribution", fontsize=12, fontweight='bold')
        ax3.set_xlabel("Salary (Rs)", fontsize=10)
        ax3.set_ylabel("Frequency", fontsize=10)
        ax3.tick_params(labelsize=9)

        # Chart 4: Average Salary by Department
        ax4 = self.figure.add_subplot(2, 3, 4)
        avg_salary = self.df.groupby("Department")["Salary"].mean().sort_values()
        bars4 = ax4.barh(avg_salary.index, avg_salary.values, color="#1abc9c", edgecolor='black', linewidth=0.5)
        ax4.set_title("Average Salary by Department", fontsize=12, fontweight='bold')
        ax4.set_xlabel("Average Salary (Rs)", fontsize=10)
        ax4.tick_params(axis='y', labelsize=9)
        # Add value labels
        for bar in bars4:
            width = bar.get_width()
            ax4.text(width, bar.get_y() + bar.get_height()/2.,
                    f'Rs {width:,.0f}', ha='left', va='center', fontsize=9)

        # Chart 5: Attrition Analysis
        ax5 = self.figure.add_subplot(2, 3, 5)
        attrition_data = self.df["Status"].apply(
            lambda x: "Active" if x == "Active" else "Attrition"
        ).value_counts()
        colors5 = ['#2ecc71', '#e74c3c']
        bars5 = ax5.bar(attrition_data.index, attrition_data.values, color=colors5, edgecolor='black', linewidth=0.5)
        ax5.set_title("Attrition Analysis", fontsize=12, fontweight='bold')
        ax5.set_ylabel("Number of Employees", fontsize=10)
        ax5.tick_params(labelsize=9)
        # Add value labels
        for bar in bars5:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)

        # Chart 6: Summary Statistics
        ax6 = self.figure.add_subplot(2, 3, 6)
        total = len(self.df)
        active = len(self.df[self.df["Status"] == "Active"])
        inactive = total - active
        avg = self.df["Salary"].mean()
        min_sal = self.df["Salary"].min()
        max_sal = self.df["Salary"].max()
        attrition_rate = (inactive / total) * 100

        ax6.axis("off")
        
        # Create a nice summary box
        summary_text = f"""
        📊 HR PEOPLE ANALYTICS SUMMARY
        ─────────────────────────────
        
        👥 Total Employees    : {total}
        ✅ Active Employees   : {active} ({active/total*100:.1f}%)
        ❌ Inactive Employees : {inactive} ({attrition_rate:.1f}%)
        
        💰 Salary Statistics:
        • Average : Rs {avg:,.0f}
        • Minimum : Rs {min_sal:,.0f}
        • Maximum : Rs {max_sal:,.0f}
        
        🏢 Departments        : {self.df['Department'].nunique()}
        """
        
        ax6.text(
            0.5, 0.5, summary_text,
            fontsize=11,
            verticalalignment="center",
            horizontalalignment="center",
            transform=ax6.transAxes,
            bbox=dict(
                facecolor="#f0f8ff", 
                edgecolor="#3498db",
                boxstyle="round,pad=0.8",
                linewidth=2
            ),
            family='monospace'
        )

        plt.tight_layout(pad=3.0)
        self.canvas.draw()
        self.statusBar().showMessage("Dashboard Generated Successfully")

    def exportCSV(self):
        if self.df is None or len(self.df) == 0:
            QMessageBox.warning(self, "Error", "Load dataset first!")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV",
            "",
            "CSV Files (*.csv)"
        )

        if filename:
            try:
                self.df.to_csv(filename, index=False)
                QMessageBox.information(
                    self,
                    "Success",
                    "Dataset Exported Successfully!"
                )
                self.statusBar().showMessage(f"Dataset exported to: {filename}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to export dataset:\n{str(e)}"
                )

    def searchEmployee(self):
        if self.df is None or len(self.df) == 0:
            QMessageBox.warning(self, "Error", "Please load a dataset first!")
            return

        name = self.searchBox.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a name to search!")
            return

        employee = self.df[
            self.df["Name"].str.contains(name, case=False, na=False)
        ]

        if employee.empty:
            QMessageBox.information(
                self,
                "Search Result",
                "❌ Employee Not Found"
            )
        else:
            message = employee.to_string(index=False)
            QMessageBox.information(
                self,
                f"✅ Employee Found ({len(employee)} match(es))",
                message
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HRDashboard()
    window.show()
    sys.exit(app.exec_())