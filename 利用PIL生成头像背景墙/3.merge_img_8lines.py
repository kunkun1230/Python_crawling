import os
from PIL import Image

UNIT_SIZE = 100 # the size of image 根据实际情况修改
def pinjie(images,num):
    target = Image.new('RGB', (UNIT_SIZE*20, UNIT_SIZE*8))   # result is 80*2 根据实际情况修改
    for j in range(1,9):   #这里选择的是8列，因此是1-9，其他情况可以看着修改成1-n
        n=20*(j-1) #因为是20张图片一行，所以是20，换成别的数字需要修改
        m=20*j
        for i in range(n,m):
            left=UNIT_SIZE*(i-n)
            upper=UNIT_SIZE*(j-1)
#           right=left+UNIT_SIZE #左上有了，右下可以不写 
#           lower=upper+UNIT_SIZE
            target.paste(images[i], (left,upper))
    quality_value = 100
    target.save(path+dirlist[num]+'.jpg', quality = quality_value)

path = "E:/数据学习资料/自己做的小项目/爬取简书推荐作者/src/"
dirlist = [] # all dir name
for root, dirs, files in os.walk(path):     
    for dir in dirs :
        dirlist.append(dir) #找到path下所有的文件名，最好只有一个

num = 0
for dir in dirlist:
    images = [] # images in each folder
    for root, dirs, files in os.walk(path+dir): # traverse each folder
        print(path+dir+'')
        for file in files:
            images.append(Image.open(path+dir+'/'+file)) #注意这个地方，images里面不是直接添加图片地址，而是先打开，避免了转义的发生
    pinjie(images,num) #加这个num是连续生成多张图片的意思
    num +=1
    print(num)
    images = []
