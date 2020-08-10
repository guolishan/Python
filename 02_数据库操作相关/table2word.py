from docx import Document
from docx.oxml.ns import qn
from src.main.db import connectoracle as cnt


# pip install python-docx
# 改一下表名和数据库连接
table_name = 'BASIC_DEPT'
sql = "SELECT t.table_name,t.colUMN_NAME,t1.COMMENTS,t.DATA_TYPE || '(' || t.DATA_LENGTH || ')' " \
      "FROM User_Tab_Cols t, User_Col_Comments t1 WHERE t.table_name = t1.table_name " \
      f"AND t.column_name = t1.column_name and t.TABLE_NAME =upper('{table_name}')"
result_list = cnt.get_oracle_data(sql)
# 数据设置
tb_list = []
head_list = ("表名", "字段", "备注", "类型")
tb_list.append(head_list)
for result in result_list:
    tb_list.append(result)
tb_rows = len(tb_list)
tb_cols = len(tb_list[0])
print(tb_rows)
print(tb_cols)
# 开始生成
print('文档生成开始')
table_doc = Document()
table_doc.styles['Normal'].font.name = u'宋体'
table_doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
table = table_doc.add_table(tb_rows, tb_cols, style="Table Grid")
# 首行
heading_list = tb_list[0]
heading_cells = table.rows[0].cells
for idx in range(tb_cols):
    heading_cells[idx].text = heading_list[idx]
# 设置每一行
for row_idx in range(1, tb_rows):
    row_cells = table.rows[row_idx].cells
    row_list = tb_list[row_idx]
    for col_idx in range(tb_cols):
        col_value = row_list[col_idx]
        if col_value is None:
            col_value = ""
        row_cells[col_idx].text = col_value.lower()
table_doc.save(r"E:\py-file\demo.docx")
print('文档生成结束')