# !/usr/bin/env python2
# -*-coding:utf-8-*-

"""
python2 bag2csv.py xxx.bag
each topic create a topic_name.csv
"""


import sys
import os
import time
import string

import csv
import rosbag

def bag2csv(bag_name, time_interval=300):  # time_interval'unit is s
	path = os.getcwd()
	bag = rosbag.Bag(bag_name)
	bag_contents = bag.read_messages()

	topics_list = []
	for topic, msg, t in bag_contents:
		if topic not in topics_list:
			topics_list.append(topic)

	for topic_name in topics_list:
		filename = os.path.join(path, string.replace(topic_name, '/', '') + '.csv')
		with open(filename, 'w+') as csv_file:
			file_writer = csv.writer(csv_file, delimiter=',')
			firstIteration = True
			init_time = 0.0
			for subtopic, msg, t in bag.read_messages(topic_name):
				msg_list = string.split(str(msg), '\n')
				instantaneousListOfData = []  # 每个topic的所有值的集合
				for nameValuePair in msg_list:
					splitPair = string.split(nameValuePair, ':')
					instantaneousListOfData.append(splitPair)
				if firstIteration:  # header
					headers = ['rosbagTimestamp']  # first column header
					for index in instantaneousListOfData:
						headers.append(index[0])
					file_writer.writerow(headers)
					firstIteration = False
				# write the value from each pair to the file
				dt = time.strftime('%H:%M:%S', time.localtime(t.to_time()))
				if t.to_time() - init_time > time_interval:
					values = [dt]  # first column will have rosbag timestamp
					for index in instantaneousListOfData:
						if len(index) > 1:
							values.append(index[1])
					file_writer.writerow(values)
					init_time = t.to_time()
	bag.close()

def main():
	if len(sys.argv) != 2:
		print "invalid number of arguments:   " + str(len(sys.argv))
		print "should be 2: 'bag2csv.py' and 'bagName'"
		print "or just 1  : 'bag2csv.py'"
		sys.exit(1)
	elif len(sys.argv) == 2:
		bag_name = sys.argv[1]
		print "reading only 1 rosbag: " + bag_name
		bag2csv(bag_name)


if __name__ == '__main__':
	main()
