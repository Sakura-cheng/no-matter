# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-05-21 16:33:59
# @Last Modified by:   Sakura-cheng
# @Last Modified time: 2017-05-22 12:13:44
import os
import sys
import pcb

file_name = 'commands.txt'
result_name = 'result.txt'

def getcommands():
	file = open(file_name, 'r')
	commands = file.read()
	file.close()
	return commands

def write(content):
	file = open(result_name, 'a')
	file.write(content)
	file.close()

if __name__ == '__main__':
	if os.path.exists('.\\' + result_name):
		os.unlink(result_name)
	#if os.path.exists('.\\' + file_name):
	commands = getcommands().split('\n')
	processes = []
	for i in range(len(commands)):
		command = commands[i].split()
		if command[0] == 'init':
			pcb.init()
			print('init')
			write('init')
			write('\n')
		elif command[0] == 'quit':
			sys.exit()
		elif command[0] == 'cr':
			if int(command[2]) > 2 or int(command[2]) <= 0:
				print('error(wrong priority)')
				write('error(wrong priority)')
				write('\n')
				input()
				sys.exit()
			else:
				content = pcb.create(command[1], int(command[2]))
				processes.append(command[1])
				print(content)
				write(content)
				write('\n')
		elif command[0] == 'de':
			if command[1] in processes:
				content = pcb.destroy(command[1])
				processes.remove(command[1])
				print(content)
				write(content)
				write('\n')
		elif command[0] == 'req':
			if command[1] == 'R1' and command[2] == '1':
				content = pcb.request(1, 1)
				print(content)
				write(content)
				write('\n')
			elif command[1] == 'R2' and (0 < int(command[2]) and int(command[2]) <= 2):
				content = pcb.request(2, int(command[2]))
				print(content)
				write(content)
				write('\n')
			elif command[1] == 'R3' and (0 < int(command[2]) and int(command[2]) <= 3):
				content = pcb.request(3, int(command[2]))
				print(content)
				write(content)
				write('\n')
			elif command[1] == 'R4' and (0 < int(command[2]) and int(command[2]) <= 4):
				content = pcb.request(4, int(command[2]))
				print(content)
				write(content)
				write('\n')
			else:
				print('error(invalid request)')
				write('error(invalid request)')
				write('\n')
				input()
				sys.exit()
		elif command[0] == 'rel':
			if command[1] == 'R1' and command[2] == '1':
				if len(pcb.pcbs[pcb.current_running].resources_list) >= int(command[2]):
					content = pcb.release(1, int(command[2]))
				else:
					print('error(over the number of resource)')
					write('error(over the number of resource)')
					write('\n')
					input()
					sys.exit()
			elif command[1] == 'R2' and ((0 < int(command[2]) and int(command[2]) <= 2)):
				if len(pcb.pcbs[pcb.current_running].resources_list) >= int(command[2]):
					content = pcb.release(2, int(command[2]))
				else:
					print('error(over the number of resource)')
					write('error(over the number of resource)')
					write('\n')
					input()
					sys.exit()
			elif command[1] == 'R3' and ((0 < int(command[2]) and int(command[2]) <= 3)):
				if len(pcb.pcbs[pcb.current_running].resources_list) >= int(command[2]):
					content = pcb.release(3, int(command[2]))
				else:
					print('error(over the number of resource)')
					write('error(over the number of resource)')
					write('\n')
					input()
					sys.exit()
			elif command[1] == 'R4' and ((0 < int(command[2]) and int(command[2]) <= 4)):
				if len(pcb.pcbs[pcb.current_running].resources_list) >= int(command[2]):
					content = pcb.release(4, int(command[2]))
				else:
					print('error(over the number of resource)')
					write('error(over the number of resource)')
					write('\n')
					input()
					sys.exit()
			else:
				print('error(invalid release)')
				write('error(invalid release)')
				write('\n')
				sys.exit()
		elif command[0] == 'to':
			content = pcb.time_out()
			print(content)
			write(content)
			write('\n')