"""
模块名称: 文档管理功能 (doc_management.py)
模块描述: 提供文档的新建、打开、保存等管理功能。

=== 功能目录 ===

📋 07文档功能 (已实现 - 1项):
├── 041 - 新建/打开/保存 ✅ (new_file, open_file, save_file, save_as_file)

📋 07文档功能 (未实现 - 6项):
├── 042 - 自动保存 ❌
├── 043 - 一键多格式导出与发布预设 ❌
├── 044 - 文档模板 ❌
├── 045 - 标签页切换 ❌
├── 046 - 会话恢复 ❌
└── 047 - 自动备份 ❌

📋 文档外功能 (辅助方法 - 2项):
├── maybe_save ⚙️ (处理未保存的更改)
└── _update_window_title ⚙️ (根据文件状态更新窗口标题)

=== 模块统计 ===
- 已实现功能: 1/7 (14.3%)
- 核心辅助方法: 2项
- 总代码行数: ~120行

=== 特别说明 ===
- 本模块是编辑器的核心功能，关系到用户数据安全。
"""
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import os


class DocManagementMixin:
    """
    功能分类: 文档管理功能
    """
    def _setup_doc_management_actions(self):
        """
        功能: 041 - 设置文档管理操作
        作用: 创建新建、打开、保存等QAction。
        """
        self.new_action = QAction("新建", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)

        self.open_action = QAction("打开...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)

        self.save_action = QAction("保存", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)

        self.save_as_action = QAction("另存为...", self)
        self.save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)

    def _update_window_title(self):
        filename = os.path.basename(self.current_file_path) if self.current_file_path else "未命名文档"
        self.setWindowTitle(f"{filename}[*] - StoryWeaver Editor")

    def new_file(self):
        """功能: 041 - 新建文件"""
        if self.maybe_save():
            self.editor.clear()
            self.current_file_path = None
            self.editor.document().setModified(False)
            self._update_window_title()

    def open_file(self):
        """功能: 041 - 打开文件"""
        if self.maybe_save():
            path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "HTML Files (*.html);;Text Files (*.txt);;All Files (*)")
            if path:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if path.endswith('.html'):
                        self.editor.setHtml(content)
                    else:
                        self.editor.setPlainText(content)

                    self.current_file_path = path
                    self.editor.document().setModified(False)
                    self._update_window_title()
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"无法打开文件: {e}")

    def save_file(self):
        """功能: 041 - 保存文件"""
        if self.current_file_path is None:
            return self.save_as_file()
        else:
            try:
                with open(self.current_file_path, 'w', encoding='utf-8') as f:
                    f.write(self.editor.toHtml())
                self.editor.document().setModified(False)
                self._update_window_title()
                return True
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法保存文件: {e}")
                return False

    def save_as_file(self):
        """功能: 041 - 另存为文件"""
        path, _ = QFileDialog.getSaveFileName(self, "另存为", "", "HTML Files (*.html);;Text Files (*.txt);;All Files (*)")
        if path:
            self.current_file_path = path
            return self.save_file()
        return False

    def maybe_save(self):
        """检查是否有未保存的更改，并提示用户。返回True表示可以继续（已保存或放弃），False表示取消操作。"""
        if not self.editor.document().isModified():
            return True

        ret = QMessageBox.warning(self, "StoryWeaver Editor",
                                  "文档已被修改。\n你想保存你的更改吗？",
                                  QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

        if ret == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif ret == QMessageBox.StandardButton.Cancel:
            return False
        return True # Discard
