import itertools as its

#迭代器
words="1234567890"
#生成密码本的位数，五位数，repeat=5
r=its.product(words,repeat=5)
#保存在文件中，追加
dic=open("../00_项目文件库/2_File/password.txt","a")
for i in r:
    #Join空格连接
    dic.write("".join(i))
    dic.write("".join("\n"))
    print(i)

dic.close()
print("密码本已经生成")