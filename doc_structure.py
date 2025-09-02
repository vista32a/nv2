"""
模块名称: 文档结构功能 (doc_structure.py)
模块描述: 提供文档结构级别的功能，如标题、样式库和分页符。

=== 功能目录 ===

📋 07文档功能 (已实现 - 4项):
├── 022 - 标题样式(H1-H6) ✅ (set_heading_style)
├── 023 - 样式库管理 ✅ (apply_quote_style, apply_code_block_style)
├── 024 - 分页符/分节符 ✅ (insert_page_break)
└── 025 - 目录自动生成 ✅ (generate_toc_html, insert_toc_at_top)

📋 07文档功能 (未实现 - 2项):
├── 026 - 书签/锚点 ❌ (通过TOC功能部分实现)
└── 027 - 章节管理 ❌

📋 文档外功能 (辅助方法 - 0项):
└── (无)

=== 模块统计 ===
- 已实现功能: 4/6 (66.7%)
- 核心辅助方法: 0项
- 总代码行数: ~200行

=== 特别说明 ===
- 目录生成功能通过设置锚点实现，这部分满足了“书签/锚点”功能的核心需求。
"""
from PyQt6.QtGui import QAction, QTextBlockFormat, QTextCharFormat, QColor, QFont, QTextCursor, QTextFormat, QTextFrameFormat


class DocStructureMixin:
    """
    功能分类: 文档结构功能
    """
    def _setup_doc_structure_actions(self):
        """
        功能: 022, 023, 024 - 设置文档结构操作
        作用: 创建标题、样式、分页符等QAction。
        """
        # Heading Actions
        self.heading1_action = QAction("标题 1", self)
        self.heading2_action = QAction("标题 2", self)
        self.heading3_action = QAction("标题 3", self)
        self.heading4_action = QAction("标题 4", self)
        self.heading5_action = QAction("标题 5", self)
        self.heading6_action = QAction("标题 6", self)
        self.normal_text_action = QAction("正文", self) # Action to revert to normal text

        # Style Library Actions
        self.quote_style_action = QAction("引用样式", self)
        self.code_block_style_action = QAction("代码块样式", self)

        # Page Break Action
        self.page_break_action = QAction("插入分页符", self)

        # TOC Action
        self.generate_toc_action = QAction("生成目录", self)

    def set_heading_style(self, level):
        """功能: 022 - 设置标题样式"""
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.SelectionType.BlockUnderCursor)

        block_fmt = cursor.blockFormat()
        block_fmt.setHeadingLevel(level)

        char_fmt = QTextCharFormat()
        font = QFont()
        font_sizes = {1: 22, 2: 18, 3: 15, 4: 13, 5: 12, 6: 11}

        if level > 0:
            font.setPointSize(font_sizes.get(level, 12))
            font.setBold(True)
        else: # Level 0 is normal text
            # Use default font size
            font.setBold(False)

        char_fmt.setFont(font)

        cursor.mergeBlockFormat(block_fmt)
        cursor.mergeCharFormat(char_fmt)
        self.editor.setFocus()

    def apply_quote_style(self):
        """功能: 023 - 应用引用样式"""
        cursor = self.editor.textCursor()

        block_fmt = cursor.blockFormat()
        block_fmt.setBackground(QColor("#f0f0f0"))
        block_fmt.setLeftMargin(20)
        block_fmt.setRightMargin(20)
        block_fmt.setTopMargin(5)
        block_fmt.setBottomMargin(5)

        char_fmt = QTextCharFormat()
        char_fmt.setFontItalic(True)
        char_fmt.setForeground(QColor("#555555"))

        cursor.mergeBlockFormat(block_fmt)
        cursor.mergeCharFormat(char_fmt)
        self.editor.setFocus()

    def apply_code_block_style(self):
        """功能: 023 - 应用代码块样式"""
        cursor = self.editor.textCursor()

        block_fmt = cursor.blockFormat()
        block_fmt.setBackground(QColor("#e9e9e9"))
        block_fmt.setLeftMargin(20)
        block_fmt.setRightMargin(20)
        block_fmt.setTopMargin(5)
        block_fmt.setBottomMargin(5)

        char_fmt = QTextCharFormat()
        font = QFont("Consolas", 11)
        char_fmt.setFont(font)
        char_fmt.setForeground(QColor("#333333"))

        cursor.mergeBlockFormat(block_fmt)
        cursor.mergeCharFormat(char_fmt)
        self.editor.setFocus()

    def insert_page_break(self):
        """功能: 024 - 插入分页符"""
        cursor = self.editor.textCursor()
        block_fmt = QTextBlockFormat()
        block_fmt.setPageBreakPolicy(QTextFormat.PageBreakFlag.PageBreak_AlwaysBefore)

        char_fmt = QTextCharFormat()
        hr_font = QFont()
        hr_font.setOverline(True)
        char_fmt.setFont(hr_font)
        char_fmt.setForeground(QColor("lightgray"))

        cursor.insertBlock(block_fmt, char_fmt)
        self.editor.setFocus()

    def generate_toc_html(self):
        """
        功能: 025 - 生成TOC的HTML内容
        扫描文档，为标题设置锚点，并返回TOC的HTML字符串。
        """
        toc_items = []
        doc = self.editor.document()
        block = doc.begin()

        # First pass: find headings and set anchors
        while block.isValid():
            level = block.blockFormat().headingLevel()
            if 1 <= level <= 6:
                text = block.text()
                if not text:
                    block = block.next()
                    continue

                # Create and set anchor name on the heading text
                anchor = f"heading-{block.blockNumber()}"
                cursor = QTextCursor(block)
                cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
                char_format = cursor.charFormat()
                char_format.setAnchorNames([anchor])
                cursor.mergeCharFormat(char_format)

                toc_items.append((level, text, anchor))
            block = block.next()

        if not toc_items:
            return "<p><i>文档中未找到标题。</i></p>"

        # Second pass: build HTML string
        html = "<h2>目录</h2><ul>"
        for level, text, anchor in toc_items:
            indent = (level - 1) * 20
            html += f'<li style="margin-left: {indent}px;"><a href="#{anchor}">{text}</a></li>'
        html += "</ul>"

        return html

    def insert_toc_at_top(self):
        """
        功能: 025 - 生成TOC并将其插入或更新到文档顶部的专用框架中。
        """
        toc_html = self.generate_toc_html()
        doc = self.editor.document()
        root_frame = doc.rootFrame()

        toc_frame = None
        # Find existing TOC frame by its object name
        for frame in root_frame.childFrames():
            if frame.objectName() == "storyweaver_toc_frame":
                toc_frame = frame
                break

        cursor = self.editor.textCursor()
        if toc_frame:
            # Frame exists, replace its content
            cursor = toc_frame.firstCursorPosition()
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.removeSelectedText()
            cursor.insertHtml(toc_html)
        else:
            # Frame does not exist, create it at the top
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            frame_format = QTextFrameFormat()
            frame_format.setBorder(1)
            frame_format.setBorderBrush(QColor("lightgray"))
            frame_format.setPadding(10)

            # Insert the frame and then set its name
            new_frame = cursor.insertFrame(frame_format)
            new_frame.setObjectName("storyweaver_toc_frame")

            cursor.insertHtml(toc_html)

        self.editor.setFocus()
