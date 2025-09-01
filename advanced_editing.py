"""
模块名称: 高级编辑功能 (advanced_editing.py)
模块描述: 提供高级编辑功能，如格式刷、智能缩进和特殊格式。

=== 功能目录 ===

📋 07文档功能 (已实现 - 3项):
├── 033 - 文字背景色/高亮 ✅ (select_highlight_color)
├── 035 - 上标/下标 ✅ (toggle_superscript, toggle_subscript)
└── 040 - 字符间距调整 ✅ (set_letter_spacing)

📋 07文档功能 (未实现 - 5项):
├── 034 - 格式刷 ❌
├── 036 - 引用格式 ❌ (已在doc_structure中实现)
├── 037 - 代码格式 ❌ (已在doc_structure中实现)
├── 038 - 智能节点链接与自动完成 ❌
└── 039 - 智能缩进 ❌ (需要重构keyPressEvent)

📋 文档外功能 (辅助方法 - 0项):
└── (无)

=== 模块统计 ===
- 已实现功能: 3/8 (37.5%)
- 核心辅助方法: 0项
- 总代码行数: ~100行

=== 特别说明 ===
- 智能缩进功能需要对QTextEdit进行子类化以正确处理事件，已推迟。
"""
from PyQt6.QtGui import QAction, QColor, QTextCharFormat, QFont, QActionGroup
from PyQt6.QtWidgets import QColorDialog, QInputDialog
from PyQt6.QtCore import Qt


class AdvancedEditingMixin:
    """
    功能分类: 高级编辑功能
    """
    def _setup_advanced_editing_actions(self):
        """
        功能: 033, 035, 039, 040 - 设置高级编辑操作
        作用: 创建背景色、上下标、智能缩进、字符间距等QAction。
        """
        self.highlight_color_action = QAction("文字背景色...", self)

        self.superscript_action = QAction("上标", self, checkable=True)
        self.subscript_action = QAction("下标", self, checkable=True)

        script_group = QActionGroup(self)
        script_group.setExclusive(True)
        script_group.addAction(self.superscript_action)
        script_group.addAction(self.subscript_action)

        self.smart_indent_action = QAction("智能缩进", self, checkable=True)
        self.smart_indent_action.setChecked(True) # Enabled by default

        self.letter_spacing_action = QAction("字符间距...", self)

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

    def handle_smart_indent(self, event):
        """功能: 039 - 处理智能缩进的按键事件"""
        if not self.smart_indent_action.isChecked():
            return False # Let the default handler take over

        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.editor.textCursor()
            current_block = cursor.block()
            prev_block = current_block.previous()

            if prev_block.isValid():
                # Get current indentation
                current_indent_str = ""
                text = prev_block.text()
                for char in text:
                    if char.isspace():
                        current_indent_str += char
                    else:
                        break

                # Check if previous line is a list item
                if prev_block.textList():
                    cursor.insertBlock()
                    cursor.insertText(current_indent_str)
                    return True # We handled the event

                # Check if previous line ends with a colon
                if text.strip().endswith(':'):
                    current_indent_str += "    " # Add one level of tab
                    cursor.insertBlock()
                    cursor.insertText(current_indent_str)
                    return True # We handled the event

        return False # Event not handled

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
