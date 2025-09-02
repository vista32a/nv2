"""
模块名称: 高级编辑功能 (advanced_editing.py)
模块描述: 提供高级编辑功能，如格式刷、智能缩进和特殊格式。

=== 功能目录 ===

📋 07文档功能 (已实现 - 4项):
├── 033 - 文字背景色/高亮 ✅ (select_highlight_color)
├── 034 - 格式刷 ✅ (copy_format, apply_format)
├── 035 - 上标/下标 ✅ (toggle_superscript, toggle_subscript)
└── 040 - 字符间距调整 ✅ (set_letter_spacing)

📋 07文档功能 (未实现 - 3项):
├── 036 - 引用格式 ❌ (已在doc_structure中实现)
├── 037 - 代码格式 ❌ (已在doc_structure中实现)
└── 038 - 智能节点链接与自动完成 ❌

📋 文档外功能 (辅助方法 - 0项):
└── (无)

=== 模块统计 ===
- 已实现功能: 4/7 (57.1%)
- 核心辅助方法: 0项
- 总代码行数: ~120行

=== 特别说明 ===
- 格式刷和智能节点链接是本模块的复杂功能，将后续实现。
"""
from PyQt6.QtGui import QAction, QColor, QTextCharFormat, QFont, QActionGroup, QTextBlockFormat
from PyQt6.QtWidgets import QColorDialog, QInputDialog
from PyQt6.QtCore import Qt


class AdvancedEditingMixin:
    """
    功能分类: 高级编辑功能
    """
    def _setup_advanced_editing_actions(self):
        """
        功能: 033, 034, 035, 040 - 设置高级编辑操作
        """
        self.format_painter_action = QAction("格式刷", self, checkable=True)
        self.highlight_color_action = QAction("文字背景色...", self)

        self.superscript_action = QAction("上标", self, checkable=True)
        self.subscript_action = QAction("下标", self, checkable=True)

        script_group = QActionGroup(self)
        script_group.setExclusive(True)
        script_group.addAction(self.superscript_action)
        script_group.addAction(self.subscript_action)

        self.letter_spacing_action = QAction("字符间距...", self)

    def copy_format(self):
        """Copies the character and block format at the current cursor position."""
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            self.format_painter_action.setChecked(False)
            return False

        self.copied_char_format = cursor.charFormat()
        self.copied_block_format = cursor.blockFormat()
        self.copied_list = cursor.block().textList()

        self.editor.set_format_painter_active(True)
        return True

    def apply_format(self):
        """Applies the stored format to the current selection."""
        if self.copied_char_format is None or self.copied_block_format is None:
            return

        cursor = self.editor.textCursor()
        cursor.beginEditBlock()

        if self.copied_list:
            cursor.createList(self.copied_list.format())
        else:
            list_obj = cursor.block().textList()
            if list_obj:
                cursor.setBlockFormat(QTextBlockFormat())

        cursor.setBlockFormat(self.copied_block_format)
        cursor.setCharFormat(self.copied_char_format)

        cursor.endEditBlock()

        self.format_painter_action.setChecked(False)
        self.editor.set_format_painter_active(False)

    def select_highlight_color(self):
        """功能: 033 - 选择文字背景色"""
        color = QColorDialog.getColor(self.editor.textBackgroundColor(), self, "选择高亮颜色")
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setBackground(color)
            self.editor.mergeCurrentCharFormat(fmt)

    def toggle_superscript(self):
        """功能: 035 - 切换上标"""
        fmt = QTextCharFormat()
        if self.superscript_action.isChecked():
            fmt.setVerticalAlignment(QTextCharFormat.VerticalAlignment.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QTextCharFormat.VerticalAlignment.AlignNormal)
        self.editor.mergeCurrentCharFormat(fmt)

    def toggle_subscript(self):
        """功能: 035 - 切换下标"""
        fmt = QTextCharFormat()
        if self.subscript_action.isChecked():
            fmt.setVerticalAlignment(QTextCharFormat.VerticalAlignment.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QTextCharFormat.VerticalAlignment.AlignNormal)
        self.editor.mergeCurrentCharFormat(fmt)

    def set_letter_spacing(self):
        """功能: 040 - 设置字符间距"""
        spacing, ok = QInputDialog.getDouble(self, "字符间距", "输入间距百分比:", 100.0, 0, 500, 1)
        if ok:
            fmt = QTextCharFormat()
            font = fmt.font()
            if not font.isCopyOf(self.editor.currentFont()):
                 font = self.editor.currentFont()
            font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, spacing)
            fmt.setFont(font)
            self.editor.mergeCurrentCharFormat(fmt)
