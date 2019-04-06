#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys,os,re

temp_h_files =  {}
NO_PATH = "NO_PATH"
FILTER_CLASS_PRE	= ""  #扫描的文件前缀

def check_file(dirname,file):
	file_path = ("%s/%s"%(dirname,file))
	if os.path.isfile(file_path):
		file_name = os.path.splitext(file)[0]
		file_type = os.path.splitext(file)[-1]
		if file_type in ('.h','.m','.mm'):
			print 'checking:',file	
			f = open(file_path)
			
			if file_type == '.h':
				if file not in temp_h_files.keys():
					temp_h_files[file]={"file_path":file_path,"import_times":0}
				else:
					temp_h_files[file]["file_path"] = file_path
			else:
				pass

			# match import files
			for line in f:
				regex = r"#import.*[\"|<\/]([\w\+\d.]+).*[\"|>]"
				matches = re.finditer(regex, line, re.MULTILINE)
				for matchNum, match in enumerate(matches, start=1):
					for groupNum in range(0, len(match.groups())):
						groupNum = groupNum + 1
						matched_file = "{group}".format(group = match.group(groupNum))
						# print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
						if os.path.splitext(matched_file)[0] != file_name :
							# insert
							if matched_file not in temp_h_files.keys():
								temp_h_files[matched_file]={"file_path":NO_PATH,"import_times":1}
							else:
								temp_h_files[matched_file]["import_times"] = temp_h_files[matched_file]["import_times"]+1
						



			f.close()
			
		

def walk_files(arg, dirname, names):
	# 不扫描Pods中的文件
	if dirname.endswith("/Pods") or ("/Pods/" in dirname):
		return;
	# 不扫描framework中的文件
	if dirname.endswith(".framework") or (".framework/" in dirname):
		return;
	for file in names:
		if FILTER_CLASS_PRE:
			if file.startswith(FILTER_CLASS_PRE): # 文件前缀过滤
				check_file(dirname,file)
		else:
			check_file(dirname,file)
			
	
	

def check(dir):
	try:
		os.chdir(dir)
	except Exception as e:
		print e
		sys.exit(2)
	else:
		print 'change to dir:',os.getcwd()
		print "---------begin-------\n"
		os.path.walk(dir, walk_files, "walking")

		header = "\n====== here is the unused files ======\n"
		print header
		
		f = open("unused_files_report.txt","w")
		f.write(header)
		count = 0
		for file_key in temp_h_files:
			if temp_h_files[file_key]["import_times"]<=0 and temp_h_files[file_key]["file_path"]!=NO_PATH:
				# report_file =  "file:  {key} \npath: {dir}".format(key=file_key,dir=temp_h_files[file_key]["file_path"])
				report_file =  "file:  {key}".format(key=file_key)
				print report_file
				f.write(report_file+'\n')
				count = count+1
		print "\n---------complete(total count:{num})---------\n".format(num=count)
		f.write("\nTotal count:{num}\n".format(num=count))
		f.close()
		
	finally:
		pass
	

def main(argv):
	dir = ''
	if len(argv) > 1:
		print "usage: python unused_files.py <your-project-directory>"
		sys.exit()
	elif len(argv) <= 0:
		dir = '.'
	else:
		dir = argv[0]

	check(dir)


if __name__ == "__main__":
   main(sys.argv[1:])
