# -*- coding: utf-8 -*-
# @Author: wsljc
# @Date:   2017-05-21 16:36:27
# @Last Modified by:   Sakura-cheng
# @Last Modified time: 2017-05-22 09:43:26
import sys
import os

current_running = 0#存PID值
pcbs = []#存pcb实例
RL = [[], [], []]#存PID值
wait_list = []#存pcb实例
R = []

class PCB(object):
	def __init__(self, pid, name, priority, resources, status_type, parent):
		self.PID = pid
		self.name =name
		self.resources = resources
		self.resources_list = []#存实例
		self.status_type = status_type
		self.status_list = []#存实例
		self.parent = parent
		self.children = []
		self.priority = priority

class RCB(object):
	def __init__(self, rid, total, available):
		self.RID = rid
		self.total = total
		self.available = available
		self.wait_line = []#存实例

def scheduler():
	global pcbs, current_running, RL
	if len(RL[2]) != 0:
		current_running = RL[2][0]
		pcbs[current_running].status_type = 'running'
		return pcbs[current_running].name
	elif len(RL[1]) != 0:
		current_running = RL[1][0]
		pcbs[current_running].status_type = 'running'
		return pcbs[current_running].name
	else:
		current_running = 0
		pcbs[current_running].status_type = 'running'
		return 'init'

def init():
	global current_running, pcbs, RL, R
	pcb = PCB(0, 'init',0,  -1, 'running', -1)
	pcbs.append(pcb)
	current_running = 0
	RL[0].append(current_running)
	for i in range(4):
		R.append(RCB(i+1, i+1, i+1))

def create(name, priority):
	global current_running, pcbs, RL
	pcb = PCB(0, name, priority, resources=-1, status_type='ready', parent=-1)
	pcb.parent = current_running
	pcbs.append(pcb)
	pcbs[-1].PID = len(pcbs) - 1
	for parent in pcbs:
		if parent.PID == current_running:
			parent.children.append(pcbs[-1].PID)
	RL[priority].append(pcbs[-1].PID)
	return scheduler()

def destroy(name):
	global pcbs, current_running, RL, R
	for pcb in pcbs:
		if pcb.name == name:
			kill(pcb)
	return scheduler()

def free_resources(r):
	global wait_list, RL
	w = wait_list[0]
	while len(r.wait_line) != 0 and r.available >= len(w.status_list):
		r.available = r.available - len(w.status_list)
		r.wait_line.pop(0)
		wait_list.remove(w)
		w.status_type = 'ready'
		RL[w.priority].append(w.PID)
		for i in range(len(w.status_list)):
			w.resources_list.append(r)
		w.status_list.append(RL[w.priority][-1])
		w = wait_list[0]

def kill(pcb):
	global current_running, pcbs, RL, R, wait_list
	if len(pcb.children) == 0:
		if pcb in wait_list:
			wait_list.remove(pcb)
		for r in pcb.resources_list:
			r.available = r.available + 1
		for r in pcb.resources_list:
			free_resources(r)
		for i in range(len(pcb.resources_list)):
			pcb.resources_list.pop()
		if pcb.PID in RL[pcb.priority]:
			RL[pcb.priority].remove(pcb.PID)
		pcbs.pop(pcb.PID)
		for pcb in pcbs[pcb.PID:]:
			pcb.PID = pcb.PID - 1
	else:
		for children in pcbs:
			if children.PID == pcb.children[0]:
				kill(children)

def request(rid, n):
	global R, current_running, pcbs, wait_list
	for pcb in pcbs:
		if pcb.PID == current_running:
			p = pcb
	for r in R:
		if r.RID == rid:
			if r.available >= n:
				r.available = r.available - n
				for i in range(n):
					p.resources_list.append(r)
			else:
				if n > r.total:
					print('错误：申请量超过资源总数')
					input()
					sys.exit()
				p.status_type = 'blocked'
				for i in range(n):
					p.status_list.append(r)
				RL[p.priority].pop(0)
				r.wait_line.append(p)
				wait_list.append(p)
	return scheduler()

def release(rid, n):
	global R, current_running, pcbs, wait_list, RL
	w = wait_list[0]
	for pcb in pcbs:
		if pcb.PID == current_running:
			p = pcb
	for r in R:
		if r.RID == rid:
			for i in range(n):
				p.resources_list.remove(r)
			r.available = r.available + n
			while len(r.wait_line) != 0 and r.available >= len(w.status_list):
				r.available = r.available - len(w.status_list)
				wait_list.remove(w)
				w.status_type = 'ready'
				RL[w.priority].append(w.PID)
				for i in range(len(w.status_list)):
					w.resources_list.append(r)
				w.status_list.append(RL[w.priority][-1])
				w = wait_list[0]

	return scheduler()

def time_out():
	global pcbs, current_running, RL
	for pcb in pcbs:
		if pcb.PID == current_running:
			RL[pcb.priority].pop(0)
			pcb.status_type = 'ready'
			RL[pcb.priority].append(pcb.PID)
	return scheduler()