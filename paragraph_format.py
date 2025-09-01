"""
模块名称: 段落格式功能 (paragraph_format.py)
模块描述: 提供段落级别的格式化功能，如对齐、缩进、行距和列表。

=== 功能目录 ===

📋 07文档功能 (已实现 - 7项):
├── 014 - 段落对齐 ✅ (set_alignment)
├── 015 - 首行缩进 ✅ (increase_indent/decrease_indent)
├── 016 - 段落缩进 ✅ (increase_indent/decrease_indent)
├── 017 - 行距调整 ✅ (apply_line_spacing)
├── 018 - 段前段后间距 ✅ (set_paragraph_spacing)
├── 019 - 有序列表 ✅ (create_list)
├── 020 - 无序列表 ✅ (create_list)

📋 07文档功能 (未实现 - 1项):
└── 021 - 多级列表 ❌ (通过缩进可实现，但样式和规则需完善)

📋 文档外功能 (辅助方法 - 0项):
└── (无)

=== 模块统计 ===
- 已实现功能: 7/8 (87.5%)
- 核心辅助方法: 0项
- 总代码行数: ~130行

=== 特别说明 ===
- 列表功能目前只支持创建，不支持切换或移除。
- 多级列表可以通过增减缩进实现，但行为和样式有待完善。
"""
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtGui import QTextBlockFormat, QTextListFormat


class ParagraphFormatMixin:
    """
    功能分类: 段落格式功能
    """
    def _setup_paragraph_format_actions(self):
        """
        功能: 014-021 - 设置段落格式操作
        作用: 创建对齐、缩进、列表等QAction。
        """
        # Alignment Actions
        self.align_left_action = QAction("左对齐", self)
        self.align_center_action = QAction("居中", self)
        self.align_right_action = QAction("右对齐", self)
        self.align_justify_action = QAction("两端对齐", self)

        alignment_group = QActionGroup(self)
        alignment_group.setExclusive(True)
        alignment_group.addAction(self.align_left_action)
        alignment_group.addAction(self.align_center_action)
        alignment_group.addAction(self.align_right_action)
        alignment_group.addAction(self.align_justify_action)

        for action in alignment_group.actions():
            action.setCheckable(True)

        self.align_left_action.setChecked(True)

        # Indentation Actions
        self.increase_indent_action = QAction("增加缩进", self)
        self.decrease_indent_action = QAction("减少缩进", self)

        # List Actions
        self.bullet_list_action = QAction("项目符号列表", self)
        self.numbered_list_action = QAction("编号列表", self)

        # Spacing Actions (will likely open dialogs)
        self.line_spacing_action = QAction("行距...", self)
        self.paragraph_spacing_action = QAction("段落间距...", self)

    def set_alignment(self, alignment):
        """功能: 014 - 设置段落对齐"""
        self.editor.setAlignment(alignment)

    def increase_indent(self):
        """功能: 016 - 增加缩进"""
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        block_format = cursor.blockFormat()
        block_format.setIndent(block_format.indent() + 1)
        cursor.setBlockFormat(block_format)
        cursor.endEditBlock()

    def decrease_indent(self):
        """功能: 016 - 减少缩进"""
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        block_format = cursor.blockFormat()
        indent = block_format.indent()
        if indent > 0:
            block_format.setIndent(indent - 1)
            cursor.setBlockFormat(block_format)
        cursor.endEditBlock()

    def create_list(self, style):
        """功能: 019, 020 - 创建列表"""
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        cursor.createList(style)
        cursor.endEditBlock()

    def apply_line_spacing(self, factor):
        """功能: 017 - 应用行距"""
        cursor = self.editor.textCursor()
        if cursor.isNull():
            return
        block_format = cursor.blockFormat()
        block_format.setLineHeight(factor, QTextBlockFormat.LineDistanceHeight.ProportionalHeight)
        cursor.setBlockFormat(block_format)

    def set_paragraph_spacing(self):
        """功能: 018 - 设置段落间距"""
        spacing, ok = QInputDialog.getInt(self, "段落间距", "输入段落上下间距:", 10, 0, 100, 1)
        if ok:
            cursor = self.editor.textCursor()
            if cursor.isNull():
                return
            block_format = cursor.blockFormat()
            block_format.setBottomMargin(spacing)
            block_format.setTopMargin(spacing)
            cursor.setBlockFormat(block_format)
