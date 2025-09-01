import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenu, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextListFormat, QKeyEvent, QTextCharFormat

from base_editing import BaseEditingMixin
from char_format import CharFormatMixin
from paragraph_format import ParagraphFormatMixin
from doc_structure import DocStructureMixin
from advanced_editing import AdvancedEditingMixin

class DemoEditor(QMainWindow, BaseEditingMixin, CharFormatMixin, ParagraphFormatMixin, DocStructureMixin, AdvancedEditingMixin):
    """
    The main window for the StoryWeaver editor.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StoryWeaver Editor")
        self.setGeometry(100, 100, 1200, 800)

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        # Setup actions from all mixins
        self._setup_base_editing_actions()
        self._setup_char_format_actions()
        self._setup_paragraph_format_actions()
        self._setup_doc_structure_actions()
        self._setup_advanced_editing_actions()

        # Setup UI components and connect signals
        self._setup_ui_components()
        self._connect_signals()

    def _setup_ui_components(self):
        # --- Toolbars ---
        edit_toolbar = self.addToolBar("编辑")
        edit_toolbar.addAction(self.undo_action)
        edit_toolbar.addAction(self.redo_action)
        edit_toolbar.addSeparator()
        edit_toolbar.addAction(self.cut_action)
        edit_toolbar.addAction(self.copy_action)
        edit_toolbar.addAction(self.paste_action)

        format_toolbar = self.addToolBar("格式")
        format_toolbar.addAction(self.bold_action)
        format_toolbar.addAction(self.italic_action)
        format_toolbar.addAction(self.underline_action)
        format_toolbar.addAction(self.strike_action)
        format_toolbar.addSeparator()
        format_toolbar.addAction(self.superscript_action)
        format_toolbar.addAction(self.subscript_action)
        format_toolbar.addSeparator()
        format_toolbar.addAction(self.font_action)
        format_toolbar.addAction(self.color_action)
        format_toolbar.addAction(self.highlight_color_action)
        format_toolbar.addAction(self.letter_spacing_action)

        paragraph_toolbar = self.addToolBar("段落")
        paragraph_toolbar.addActions(self.align_left_action.parent().actions())
        paragraph_toolbar.addSeparator()
        paragraph_toolbar.addAction(self.decrease_indent_action)
        paragraph_toolbar.addAction(self.increase_indent_action)
        paragraph_toolbar.addSeparator()
        paragraph_toolbar.addAction(self.bullet_list_action)
        paragraph_toolbar.addAction(self.numbered_list_action)
        paragraph_toolbar.addSeparator()
        paragraph_toolbar.addAction(self.line_spacing_action)
        paragraph_toolbar.addAction(self.paragraph_spacing_action)

        styles_toolbar = self.addToolBar("样式")
        self.heading_combo = QComboBox()
        self.heading_combo.addItems(["正文", "标题 1", "标题 2", "标题 3", "标题 4", "标题 5", "标题 6"])
        styles_toolbar.addWidget(self.heading_combo)
        styles_toolbar.addAction(self.quote_style_action)
        styles_toolbar.addAction(self.code_block_style_action)
        styles_toolbar.addAction(self.page_break_action)

        # --- Menu Bar ---
        menu_bar = self.menuBar()

        edit_menu = menu_bar.addMenu("编辑 (&E)")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_all_action)

        format_menu = menu_bar.addMenu("格式 (&F)")
        format_menu.addAction(self.bold_action)
        format_menu.addAction(self.italic_action)
        format_menu.addAction(self.underline_action)
        format_menu.addAction(self.strike_action)
        format_menu.addSeparator()
        format_menu.addAction(self.superscript_action)
        format_menu.addAction(self.subscript_action)
        format_menu.addSeparator()
        format_menu.addAction(self.font_action)
        format_menu.addAction(self.color_action)
        format_menu.addAction(self.highlight_color_action)
        format_menu.addSeparator()
        format_menu.addAction(self.letter_spacing_action)
        format_menu.addSeparator()
        format_menu.addAction(self.smart_indent_action)


        paragraph_menu = menu_bar.addMenu("段落 (&P)")
        paragraph_menu.addActions(self.align_left_action.parent().actions())
        paragraph_menu.addSeparator()
        paragraph_menu.addAction(self.decrease_indent_action)
        paragraph_menu.addAction(self.increase_indent_action)
        paragraph_menu.addSeparator()
        paragraph_menu.addAction(self.bullet_list_action)
        paragraph_menu.addAction(self.numbered_list_action)
        paragraph_menu.addSeparator()

        line_spacing_menu = QMenu("行距", self)
        line_spacing_menu.addAction("单倍行距").triggered.connect(lambda: self.apply_line_spacing(1.0))
        line_spacing_menu.addAction("1.15倍行距").triggered.connect(lambda: self.apply_line_spacing(1.15))
        line_spacing_menu.addAction("1.5倍行距").triggered.connect(lambda: self.apply_line_spacing(1.5))
        line_spacing_menu.addAction("2.0倍行距").triggered.connect(lambda: self.apply_line_spacing(2.0))
        self.line_spacing_action.setMenu(line_spacing_menu)
        paragraph_menu.addAction(self.line_spacing_action)
        paragraph_menu.addAction(self.paragraph_spacing_action)

        styles_menu = menu_bar.addMenu("样式 (&S)")
        styles_menu.addAction(self.normal_text_action)
        styles_menu.addSeparator()
        styles_menu.addAction(self.heading1_action)
        styles_menu.addAction(self.heading2_action)
        styles_menu.addAction(self.heading3_action)
        styles_menu.addAction(self.heading4_action)
        styles_menu.addAction(self.heading5_action)
        styles_menu.addAction(self.heading6_action)
        styles_menu.addSeparator()
        styles_menu.addAction(self.quote_style_action)
        styles_menu.addAction(self.code_block_style_action)
        styles_menu.addSeparator()
        styles_menu.addAction(self.page_break_action)

    def _connect_signals(self):
        # Char format signals
        self.editor.cursorPositionChanged.connect(self.update_format_actions)

        # Paragraph format signals
        self.align_left_action.triggered.connect(lambda: self.set_alignment(Qt.AlignmentFlag.AlignLeft))
        self.align_center_action.triggered.connect(lambda: self.set_alignment(Qt.AlignmentFlag.AlignCenter))
        self.align_right_action.triggered.connect(lambda: self.set_alignment(Qt.AlignmentFlag.AlignRight))
        self.align_justify_action.triggered.connect(lambda: self.set_alignment(Qt.AlignmentFlag.AlignJustify))
        self.increase_indent_action.triggered.connect(self.increase_indent)
        self.decrease_indent_action.triggered.connect(self.decrease_indent)
        self.bullet_list_action.triggered.connect(lambda: self.create_list(QTextListFormat.Style.ListDisc))
        self.numbered_list_action.triggered.connect(lambda: self.create_list(QTextListFormat.Style.ListDecimal))
        self.paragraph_spacing_action.triggered.connect(self.set_paragraph_spacing)
        self.editor.cursorPositionChanged.connect(self.update_paragraph_actions_state)

        # Doc structure signals
        self.heading_combo.currentIndexChanged.connect(self.set_heading_style_from_combo)
        self.normal_text_action.triggered.connect(lambda: self.set_heading_style(0))
        self.heading1_action.triggered.connect(lambda: self.set_heading_style(1))
        self.heading2_action.triggered.connect(lambda: self.set_heading_style(2))
        self.heading3_action.triggered.connect(lambda: self.set_heading_style(3))
        self.heading4_action.triggered.connect(lambda: self.set_heading_style(4))
        self.heading5_action.triggered.connect(lambda: self.set_heading_style(5))
        self.heading6_action.triggered.connect(lambda: self.set_heading_style(6))
        self.quote_style_action.triggered.connect(self.apply_quote_style)
        self.code_block_style_action.triggered.connect(self.apply_code_block_style)
        self.page_break_action.triggered.connect(self.insert_page_break)
        self.editor.cursorPositionChanged.connect(self.update_structure_actions_state)

        # Advanced editing signals
        self.highlight_color_action.triggered.connect(self.select_highlight_color)
        self.superscript_action.triggered.connect(self.toggle_superscript)
        self.subscript_action.triggered.connect(self.toggle_subscript)
        self.letter_spacing_action.triggered.connect(self.set_letter_spacing)
        self.editor.cursorPositionChanged.connect(self.update_advanced_actions_state)

    def set_heading_style_from_combo(self, index):
        self.set_heading_style(index)

    def update_paragraph_actions_state(self):
        alignment = self.editor.alignment()
        if alignment == Qt.AlignmentFlag.AlignLeft:
            self.align_left_action.setChecked(True)
        elif alignment == Qt.AlignmentFlag.AlignCenter:
            self.align_center_action.setChecked(True)
        elif alignment == Qt.AlignmentFlag.AlignRight:
            self.align_right_action.setChecked(True)
        elif alignment == Qt.AlignmentFlag.AlignJustify:
            self.align_justify_action.setChecked(True)

    def update_structure_actions_state(self):
        level = self.editor.textCursor().blockFormat().headingLevel()
        self.heading_combo.blockSignals(True)
        self.heading_combo.setCurrentIndex(level)
        self.heading_combo.blockSignals(False)

    def update_advanced_actions_state(self):
        fmt = self.editor.currentCharFormat()
        align = fmt.verticalAlignment()
        self.superscript_action.setChecked(align == QTextCharFormat.VerticalAlignment.AlignSuperScript)
        self.subscript_action.setChecked(align == QTextCharFormat.VerticalAlignment.AlignSubScript)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = DemoEditor()
    main_window.show()
    sys.exit(app.exec())
