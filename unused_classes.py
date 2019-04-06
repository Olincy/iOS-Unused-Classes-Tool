#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys,os,re


# 匹配class 的申明  ^[ ]*@interface[ ]+([a-zA-Z_][\w]+)[ ]*:
# 匹配被使用的class  (?:[<]*([A-Z_][\w]+)[ ]+\*[>]*)|(?:.*\[[ ]*([A-Z_][\w]+)[ ].*\])|(?:[:][ ]*([A-Z_][\w]+))


CLASS_NAME_KEY = "CLASS_NAME_KEY"
CLASS_COUNT_KEY = "CLASS_COUNT_KEY"
SCAN_CLASS_DEF= "SCAN_CLASS_DEF" #扫描类的申明
SCAN_CLASS_USE = "SCAN_CLASS_USE" # 扫描类的使用

temp_classes =  []


# 匹配类	
def match_class(line,regex,scan_type):
	matches = re.finditer(regex, line, re.MULTILINE)

	for matchNum, match in enumerate(matches, start=1):
		for groupNum in range(0, len(match.groups())):
			groupNum = groupNum + 1
			matched_class = "{group}".format(group = match.group(groupNum))
			if scan_type == SCAN_CLASS_DEF:
				temp_classes.append(matched_class)
			else:
				for item in temp_classes[:]:
					if matched_class == item:
						temp_classes.remove(item)
			


def walk_files(scan_type, dirname, names):
	# 不扫描Pods中的文件
	if dirname.endswith("/Pods") or ("/Pods/" in dirname):
		return;
	# 不扫描framework中的文件
	if dirname.endswith(".framework") or (".framework/" in dirname):
		return;
	for file in names:
		# if file.startswith("TC"): //过滤前缀
		
		file_path = ("%s/%s"%(dirname,file))
		if os.path.isfile(file_path):
			file_name = os.path.splitext(file)[0]
			file_type = os.path.splitext(file)[-1]
			if file_type in ('.h','.m','.mm'):
				print "checking file:",file
				f = open(file_path)
				
				for line in f:
					regex = ""
					if scan_type == SCAN_CLASS_DEF:# 匹配类的申明
						regex = r"^[ ]*@interface[ ]+([a-zA-Z_][\w]+)[ ]*:" 
					else: # 匹配类的使用
						regex = r"(?:[<]*([A-Z_][\w]+)[ ]+\*[>]*)|(?:.*\[[ ]*([A-Z_][\w]+)[ ].*\])|(?:[:][ ]*([A-Z_][\w]+))"

					match_class(line,regex,scan_type)
						
				f.close()
			
	
	

def check(dir):
	try:
		os.chdir(dir)
	except Exception as e:
		print e
		sys.exit(2)
	else:
		print 'change to dir:',os.getcwd()
		print "---------begin-------\n"
		print "checking defined classes:\n"
		os.path.walk(dir, walk_files, SCAN_CLASS_DEF)
		# print "\n====== here is the defined classes({num}) ======\n".format(num=len(temp_classes))
		# for class_key in temp_classes:
		# 	print class_key
		print "now checking unused classes:\n"
		os.path.walk(dir, walk_files, SCAN_CLASS_USE)
		header = "\n====== here is the unused classes ======\n"
		print header

		f = open("unused_classes_report.txt","w")
		f.write(header)
		for class_key in temp_classes:
			print class_key
			f.write(class_key+'\n')
			
		f.write("\nTotal count:{num}\n".format(num=len(temp_classes)))
		f.close()

		
		print "\n---------complete(total count:{num})---------\n".format(num=len(temp_classes))
		print "A report file is generated in: {dir}".format(dir=os.getcwd())
		print 'use "cat {dir}/unused_classes_report.txt"\n'.format(dir=os.getcwd())

	finally:
		pass
	

def main(argv):
	dir = argv[0]
	if len(argv) > 1:
		print "usage: python unused_classes.py <your-project-directory>"
		sys.exit()
	elif len(argv) <= 0:
		dir = '.'
	# 	print "check in current directory。"
	# else:
	# 	print 'check in directory:',dir

	check(dir)


if __name__ == "__main__":
   main(sys.argv[1:])