import os

def stats_start(root_path):
    n = 0
    # 遍历删除
    for tmp_root, tmp_dir, tmp_names in os.walk(root_path):
        for tmp_name in tmp_names:
            if tmp_name.endswith('.java'):
                n += 1
    print(n)

# 统计文件数量
if __name__ == '__main__':
    stats_start('F:\mes_workspace_test\\N2\src')
