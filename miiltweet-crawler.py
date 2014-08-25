#!/usr/bin/env python
# -*- coding: utf-8 -*-                                                                              
import codecs
import datetime
import dateutil.parser
import json
import os.path
import re
import sys
import urllib
import urllib2

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

# Twitterから#miilのタグがついたpostを100件取得
post = urllib.urlopen("http://search.twitter.com/search.json?q=%23miil&since=2011-01-20&rpp=500")
rPost = post.read().decode("utf-8")
l = json.loads(rPost);

#日付を取得
d = datetime.datetime.today()
today = '%s-%s-%s' % (d.year, d.month, d.day)
today += '-'
#print today

# 文字列を格納する配列を作成
array = []
array2 = []
i = 0; # CSV格納の配列用
j = 0; # txt格納の配列用

#ディレクトリ移動
os.chdir("./miil")

for s in l["results"]:

	# postのタイムゾーンをJSTに変更
	dt = dateutil.parser.parse(s["created_at"])
	dt = dt.replace(tzinfo=dateutil.tz.tzutc()).astimezone(dateutil.tz.tzlocal())
	print str(dt)

	# 発言から短縮URLを抽出
	res = re.search("http://t.co/[^/].......",str(s))

	#短縮URLが入っていない投稿ははじく
	if res == None :
		print "none"

	#短縮URLがある投稿を抽出
	elif res != None :


		# 短縮URLを展開し、末尾に.jpegをつけて画像URLを取得
		tiny = str(res.group(0))
		url = urllib2.urlopen(tiny).geturl()
		url += ".jpeg"


		#文字列at Homeを含む発言を抽出
		if re.search("at Home", str(s)) != None :

			# csvファイルに画像URLと時間、発言者名を記録
			#txt.write(url + "\n");
			#csv.write(url + "," + str(dt) +","+ s["from_user"] + ",at Home ,"+"\n");
			csvData = url + "," + str(dt) +","+ s["from_user"] + ",at Home ,"+"\n"
			array2.insert(j, url + "\n")
			j = j+1

			# URLから画像をローカルに保存しファイル名を変更
			img = urllib.urlopen(url)
			localfile = open( os.path.basename(url), 'wb')
			localfile.write(img.read())
			os.rename(os.path.basename(url),today+(os.path.basename(url)) ) 

			img.close()
			localfile.close()

			#print s["created_at"]

		# at Homeと書かれていないpostをcsvに書き込む
		elif re.search("at Home", str(s)) == None :
			#csv.write(url + "," + str(dt) +","+ s["from_user"] +", ,\n");
			csvData = url + "," + str(dt) +","+ s["from_user"] + ", ,"+"\n"

		array.insert(i, csvData)
		#print array[i]
		i = i+1

#ディレクトリ移動
os.chdir("../")

# UTF-8でファイルを開く
csv = codecs.open('miilData.csv', 'a+', 'utf-8');
txt = codecs.open('miilData.txt', 'a+', 'utf-8');

#配列要素を逆に変換してcsvとtxtに保存
array.reverse()
print array
i = 0
for i in array:
	print i
	csv.write(i)

array2.reverse()
print array2
j = 0
for j in array2:
	print j
	txt.write(j)

csv.close();
txt.close();
