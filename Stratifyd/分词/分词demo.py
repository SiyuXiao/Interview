import jieba
#seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
#print("Full Mode: " + "/ ".join(seg_list))  # 全模式
lines = []
with open('pos.txt', 'rb') as f:
	for line in f:
		line = line.decode('utf-8')#把二进制解码成文字
		line = line.rstrip()
		line = ' '.join(jieba.cut(line))
		lines.append(line)
with open('pos1.txt', 'wb') as f:
	for line in lines:
		line = '{}\r\n'.format(line)
		line = line.encode('utf-8')#把文字编码成二进制
		f.write(line)
