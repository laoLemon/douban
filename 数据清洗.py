import csv
def comment(movie):
    # 打开表格  as从命名 file
    # 参数1：表格名称
    # 参数2："a+"追加模式  "w"写入模式   "r"读取模式
    # w：writer   r：read  a：append
    # wb二进制，不带b就是文本
    # 参数3：数据格式为utf-8
    # 参数4：newline 新行，空行
    i=0
    with open(movie,"r",encoding="ANSI",newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        rows = list(csvreader)
        #影评去回车
        comment_index=2
        for row in rows:
            comment_content = row[comment_index]
            row[comment_index] = comment_content.replace("\n","")
        with open('output_file.csv','w',newline='',encoding='ANSI') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(rows)
        csvfile.close()

def delstardate(movie):
    # 打开表格  as从命名 file
    # 参数1：表格名称
    # 参数2："a+"追加模式  "w"写入模式   "r"读取模式
    # w：writer   r：read  a：append
    # wb二进制，不带b就是文本
    # 参数3：数据格式为utf-8
    # 参数4：newline 新行，空行
    star_index = 1
    date_index = 3
    with open(movie, "r", encoding="ANSI", newline="") as csvfile, \
            open('output_file.csv', 'w', newline='', encoding='ANSI') as output_csvfile:
        csvreader = csv.reader(csvfile)
        csvwriter = csv.writer(output_csvfile)

        for row in csvreader:
            star_content = row[star_index]
            if star_content not in ['1','2','3','4','5']:
                continue
            csvwriter.writerow(row)
        csvfile.close()


def merge_csv_files(file_names, output_file, encoding='ANSI'):
    # 打开输出文件
    with open(output_file, 'w', encoding=encoding) as output_csvfile:
        # 逐个处理输入文件
        for file_name in file_names:
            try:
                # 打开当前文件并将其内容写入到输出文件中
                with open(file_name, 'r', encoding=encoding) as input_csvfile:
                    output_csvfile.write(input_csvfile.read())
            except UnicodeDecodeError:
                print(f"无法使用编码 '{encoding}' 读取文件: {file_name}")
                continue

    print(f"合并完成并保存为 {output_file}")


if __name__ == '__main__':
    file_names = ['./csv/clean/2019流浪地球.csv', './csv/clean/2021唐人街3.csv',
                  './csv/clean/2022长津湖.csv', './csv/clean/2023满江红.csv',
                  './csv/clean/2024热辣滚烫.csv']
    output_file = './csv/merged_file.csv'  # 合并后的文件名

    # a = delstardate('C:/Users/niwenkai/Desktop/毕业设计/数据/2019流浪地球未清洗.csv')
    # b = comment('output_file.csv')

    merge_csv_files(file_names, output_file)