import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit

from base_editing import BaseEditingMixin
from char_format import CharFormatMixin

# Inherit from QMainWindow and all created mixins
class DemoEditor(QMainWindow, BaseEditingMixin, CharFormatMixin):
    """
    The main window for the StoryWeaver editor.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StoryWeaver Editor")
        self.setGeometry(100, 100, 800, 600)

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        # Setup actions from all mixins
        self._setup_base_editing_actions()
        self._setup_char_format_actions()

        # Setup UI components
        self._setup_ui_components()

        # Connect signals for format updates
        self.editor.cursorPositionChanged.connect(self.update_format_actions)

    def _setup_ui_components(self):
        """
        功能: 028, 029, 054, 055 - 设置UI组件
        作用: 创建并设置菜单栏和工具栏。
        """
        # --- Edit Toolbar ---
        edit_toolbar = self.addToolBar("编辑")
        edit_toolbar.addAction(self.undo_action)
        edit_toolbar.addAction(self.redo_action)
        edit_toolbar.addSeparator()
        edit_toolbar.addAction(self.cut_action)
        edit_toolbar.addAction(self.copy_action)
        edit_toolbar.addAction(self.paste_action)

        # --- Format Toolbar ---
        format_toolbar = self.addToolBar("格式")
        format_toolbar.addAction(self.bold_action)
        format_toolbar.addAction(self.italic_action)
        format_toolbar.addAction(self.underline_action)
        format_toolbar.addAction(self.strike_action)
        format_toolbar.addSeparator()
        format_toolbar.addAction(self.font_action)
        format_toolbar.addAction(self.color_action)

        # --- Menu Bar ---
        menu_bar = self.menuBar()

        # Edit Menu
        edit_menu = menu_bar.addMenu("编辑 (&E)")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_all_action)

        # Format Menu
        format_menu = menu_bar.addMenu("格式 (&F)")
        format_menu.addAction(self.bold_action)
        format_menu.addAction(self.italic_action)
        format_menu.addAction(self.underline_action)
        format_menu.addAction(self.strike_action)
        format_menu.addSeparator()
        format_menu.addAction(self.font_action)
        format_menu.addAction(self.color_action)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = DemoEditor()
    main_window.show()
    sys.exit(app.exec())
