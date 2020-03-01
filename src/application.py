"""Application module containing main window."""

# global imports:
import sys
from PySide2 import QtGui, QtCore, QtWidgets

# local imports:
from src import constants, utils

class DemoWindow(QtWidgets.QMainWindow):
    """Qt demo main window.
    
    Args:
        parent (QWidget): Parent object of this window.
    """
    def __init__(self, parent=None):
        super(DemoWindow, self).__init__(parent)
        self.setGeometry(0,0,300,100)
        self.setWindowTitle ('Demo Dialog')

        # status bar
        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)

        # menu bar
        self.menu_bar = QtWidgets.QMenuBar()
        demo_menu = self.menu_bar.addMenu('Menu')

        # status bar
        clear_action = QtWidgets.QAction('Clear', self)
        clear_action.setStatusTip(
            'Clear the text and reset font size and color.'
        )
        demo_menu.addAction(clear_action)
        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.setStatusTip(
            'Close this application.'
        )
        demo_menu.addAction(exit_action)
        demo_menu.triggered[QtWidgets.QAction].connect(
            self.process_menu_trigger
        )

        self.setMenuBar(self.menu_bar)

        # layout widget
        central_widget = QtWidgets.QWidget(self)
        main_layout = QtWidgets.QGridLayout()

        # line edit
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setMaxLength(constants.MAX_CHAR)
        self.line_edit.textChanged.connect(self.text_changed)
        main_layout.addWidget(self.line_edit, 0, 0, 1, 4)
        self.line_edit.setStatusTip(
            'This is a line edit you can enter text in.'
        )

        # font size spinbox
        self.font_size_sb = QtWidgets.QSpinBox()
        self.font_size_sb.setMinimum(1)
        self.font_size_sb.valueChanged.connect(self.font_size_changed)
        main_layout.addWidget(self.font_size_sb, 1, 3)
        self.font_size_sb.setStatusTip(
            'This is a spinbox you can enter a font size in.'
        )

        # font size label
        font_size_label = QtWidgets.QLabel('Font Size:')
        main_layout.addWidget(font_size_label, 1, 2)

        # set font spinbox to current font size
        font = self.line_edit.font()
        self.default_point_size = font.pointSize()
        if self.default_point_size == -1:
            primary_screen = QtGui.QGuiApplication.primaryScreen()
            dpi = primary_screen.logicalDotsPerInch()
            self.default_point_size = utils.pixel_to_point(font.pixelSize(), dpi)
        self.font_size_sb.setValue(self.default_point_size)
        
        # font color dialog
        self.font_color_cd = QtWidgets.QColorDialog()
        self.font_color_cd.currentColorChanged.connect(
            self.font_color_changed
        )
        # embed in current window
        self.font_color_cd.setWindowFlags(QtCore.Qt.Widget)
        flags = QtWidgets.QColorDialog.DontUseNativeDialog | QtWidgets.QColorDialog.NoButtons  # noqa
        self.font_color_cd.setOptions(
            flags
        )
        main_layout.addWidget(self.font_color_cd, 2, 0, 1, 4)

        # font color label
        font_color_label = QtWidgets.QLabel('Font Color:')
        main_layout.addWidget(font_color_label, 1, 0)
        self.font_color_cd.setStatusTip(
            'This is a color dialog you can select the font color in.'
        )

        # set font color dialog to current font color
        palette = self.line_edit.palette()
        self.default_color = palette.color(QtGui.QPalette.Text)
        self.font_color_cd.setCurrentColor(self.default_color)

        # label for displaying nr of chars
        self.count_label = QtWidgets.QLabel()
        self.count_label.setText(
            constants.TEMPLATE_MESSAGE.format(0,constants.MAX_CHAR)
        )
        main_layout.addWidget(self.count_label, 3, 0, 1, 4)
        self.count_label.setStatusTip(
            'This is a label for displaying the number of characters entered.'
        )

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.center()
        self.read_settings()

    def process_menu_trigger(self, action):
        """Process pressed menu items.
        
        Args:
            action(QAction): action object trigger came from.
        """
        action_name = action.text()
        if action_name == 'Exit':
            self.close()
        elif action_name == 'Clear':
            self.line_edit.clear()
            self.set_font_size(self.default_point_size)
            self.font_size_sb.setValue(self.default_point_size)
            self.set_font_color(self.default_color)
            self.font_color_cd.setCurrentColor(self.default_color)

    def font_color_changed(self):
        """Callback for color dialog color selected."""
        color = self.font_color_cd.currentColor()
        self.set_font_color(color)

    def set_font_color(self, color):
        """Set the font color of the line edit.
        
        Args:
            color (QColor): color to set font to.
        """
        palette = self.line_edit.palette()
        palette.setColor(QtGui.QPalette.Text, color)
        self.line_edit.setPalette(palette)

    def font_size_changed(self):
        """Callback for font size combobox value changed."""
        point_size = self.font_size_sb.value()
        self.set_font_size(point_size)

    def set_font_size(self, point_size):
        """Set the font size of the line edit.
        
        Args:
            point_size (float): point size to set font size to.
        """
        font = self.line_edit.font()
        font.setPointSize(point_size)
        self.line_edit.setFont(font)

    def text_changed(self):
        """Callback for text changed."""
        self.update_num_characters()

    def update_num_characters(self):
        """Update label with data from line edit."""
        length = len(self.line_edit.text())
        self.count_label.setText(
            constants.TEMPLATE_MESSAGE.format(
                length,
                constants.MAX_CHAR)
            )

    def center(self):
        """Center this window on active screen."""
        frame_geometry = self.frameGeometry()
        available_geometry = QtWidgets.QDesktopWidget().availableGeometry()
        center_point = available_geometry.center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def closeEvent(self, event):
        """Override close event to store geometry/state settings.
        
        Args:
            event (QEvent): event references passed by close emitter.
        """
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())
        super(DemoWindow, self).closeEvent(event)

    def read_settings(self):
        """Read settings to restore geometry/state of window."""
        self.settings = QtCore.QSettings('mvn', 'qt-demo')
        geometry = self.settings.value('geometry', '')
        if geometry:
            self.restoreGeometry(geometry)
        state = self.settings.value('windowState', '')
        if state:
            self.restoreState(state)

def launch():
    """Launch the qt demo application."""
    app = QtWidgets.QApplication(sys.argv)
    ex = DemoWindow()
    ex.show()
    sys.exit(app.exec_())