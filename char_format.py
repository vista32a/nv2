"""
模块名称: 字符格式功能 (char_format.py)
模块描述: 提供字符级别的格式化功能，如字体、字号、颜色和样式。

=== 功能目录 ===

📋 07文档功能 (已实现 - 5项):
├── 008 - 粗体/斜体/下划线 ✅ (toggle_bold, toggle_italic, toggle_underline)
├── 009 - 字体选择 ✅ (select_font)
├── 010 - 字号调整 ✅ (select_font)
├── 011 - 文字颜色 ✅ (select_color)
└── 012 - 删除线 ✅ (toggle_strike)

📋 07文档功能 (未实现 - 1项):
└── 013 - 格式化粘贴 ❌ (后续实现)

📋 文档外功能 (辅助方法 - 1项):
└── update_format_actions ⚙️ (根据光标位置更新UI)

=== 模块统计 ===
- 已实现功能: 5/6 (83.3%)
- 核心辅助方法: 1项
- 总代码行数: ~100行

=== 特别说明 ===
- 字体和颜色选择使用QDialog。
- 格式状态更新是本模块的关键。
"""
from PyQt6.QtGui import QAction, QTextCharFormat, QFont
from PyQt6.QtWidgets import QFontDialog, QColorDialog

class CharFormatMixin:
    """
    功能分类: 字符格式功能
    """
    def _setup_char_format_actions(self):
        """
        功能: 008, 009, 010, 011, 012 - 设置字符格式操作
        作用: 创建并连接粗体、斜体、下划线、字体、颜色等QAction。
        """
        # Actions
        self.bold_action = QAction("粗体 (&B)", self, checkable=True)
        self.italic_action = QAction("斜体 (&I)", self, checkable=True)
        self.underline_action = QAction("下划线 (&U)", self, checkable=True)
        self.strike_action = QAction("删除线", self, checkable=True)
        self.font_action = QAction("字体...", self)
        self.color_action = QAction("颜色...", self)

        # Triggers
        self.bold_action.triggered.connect(self.toggle_bold)
        self.italic_action.triggered.connect(self.toggle_italic)
        self.underline_action.triggered.connect(self.toggle_underline)
        self.strike_action.triggered.connect(self.toggle_strike)
        self.font_action.triggered.connect(self.select_font)
        self.color_action.triggered.connect(self.select_color)

    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if self.bold_action.isChecked() else QFont.Weight.Normal)
        self.editor.mergeCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italic_action.isChecked())
        self.editor.mergeCurrentCharFormat(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underline_action.isChecked())
        self.editor.mergeCurrentCharFormat(fmt)

    def toggle_strike(self):
        fmt = QTextCharFormat()
        fmt.setFontStrikeOut(self.strike_action.isChecked())
        self.editor.mergeCurrentCharFormat(fmt)

    def select_font(self):
        current_font = self.editor.currentFont()
        ok, font = QFontDialog.getFont(current_font, self, "选择字体")
        if ok:
            fmt = QTextCharFormat()
            fmt.setFont(font)
            self.editor.mergeCurrentCharFormat(fmt)

    def select_color(self):
        current_color = self.editor.textColor()
        color = QColorDialog.getColor(current_color, self, "选择颜色")
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.editor.mergeCurrentCharFormat(fmt)

    def update_format_actions(self):
        """
        根据光标位置的格式，更新工具栏按钮的状态。
        """
        fmt = self.editor.currentCharFormat()
        self.bold_action.setChecked(fmt.fontWeight() == QFont.Weight.Bold)
        self.italic_action.setChecked(fmt.fontItalic())
        self.underline_action.setChecked(fmt.fontUnderline())
        self.strike_action.setChecked(fmt.fontStrikeOut())
