from docx import Document
from docx.oxml.ns import qn


# pip install python-docx, style样式查看tablestyles.py
def save_table_doc(tb_rows, tb_cols, tb_list):
    table_doc = Document()
    table_doc.styles['Normal'].font.name = u'宋体'
    table_doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

    table = table_doc.add_table(tb_rows, tb_cols, style="Table Grid")
    # 首行
    heading_list = tb_list[0]
    heading_cells = table.rows[0].cells
    for idx in range(tb_cols):
        heading_cells[idx].text = f'第一行第{idx+1}列:{heading_list[idx]}'
    # 设置每一行
    for row_idx in range(1, tb_rows):
        row_cells = table.rows[row_idx].cells
        row_list = tb_list[row_idx]
        for col_idx in range(tb_cols):
            row_cells[col_idx].text = f'第{row_idx+1}行第{col_idx+1}列:{row_list[col_idx]}'
    table_doc.save(r"E:\py-file\demo.docx")


if __name__ == '__main__':
    res_list = []
    tmp_list = [1, 2, 3, 4, 5]
    res_list.append(tmp_list)
    res_list.append(tmp_list)
    res_list.append(tmp_list)
    res_list.append(tmp_list)
    rows = len(res_list)
    cols = len(res_list[0])
    save_table_doc(rows, cols, res_list)
    print(">>>完成")
