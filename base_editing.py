"""
模块名称: 基础文本编辑功能 (base_editing.py)
模块描述: 提供基础的文本编辑功能，如剪切、复制、粘贴、撤销、重做等。

=== 功能目录 ===

📋 07文档功能 (已实现 - 6项):
├── 001 - 文本输入/删除 ✅ (原生支持)
├── 002 - 光标移动和定位 ✅ (原生支持)
├── 003 - 文本选择 ✅ (原生支持)
├── 004 - 复制/剪切/粘贴 ✅ (_setup_base_editing_actions)
├── 005 - 撤销/重做 ✅ (_setup_base_editing_actions)
└── 007 - 全选功能 ✅ (_setup_base_editing_actions)

📋 07文档功能 (未实现 - 1项):
└── 006 - 查找/替换 ❌ (后续实现)

📋 文档外功能 (辅助方法 - 0项):
└── (无)

=== 模块统计 ===
- 已实现功能: 6/7 (85.7%)
- 核心辅助方法: 0项
- 总代码行数: ~50行

=== 特别说明 ===
- 本模块功能主要通过连接QTextEdit的原生方法实现。
"""
from PyQt6.QtGui import QAction

class BaseEditingMixin:
    """
    功能分类: 基础文本编辑功能
    """
    def _setup_base_editing_actions(self):
        """
        功能: 004, 005, 007 - 设置基础编辑操作
        作用: 创建并连接复制、剪切、粘贴、撤销、重做、全选等QAction。
        """
        # Create actions
        self.undo_action = QAction("撤销 (&U)", self)
        self.redo_action = QAction("重做 (&R)", self)
        self.cut_action = QAction("剪切 (&T)", self)
        self.copy_action = QAction("复制 (&C)", self)
        self.paste_action = QAction("粘贴 (&P)", self)
        self.select_all_action = QAction("全选 (&A)", self)

        # Connect actions to editor slots
        self.undo_action.triggered.connect(self.editor.undo)
        self.redo_action.triggered.connect(self.editor.redo)
        self.cut_action.triggered.connect(self.editor.cut)
        self.copy_action.triggered.connect(self.editor.copy)
        self.paste_action.triggered.connect(self.editor.paste)
        self.select_all_action.triggered.connect(self.editor.selectAll)

        # These actions will be added to menus in the main window class
