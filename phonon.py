#!/usr/bin/env python
#coding=utf-8
"""
播放相关逻辑
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon
import os,sys

class player():
	# =========================初始化播放组件=============================================
	def __init__(self,window):  #参数window为播放器父框对象
		reload(sys)
		sys.setdefaultencoding('utf8')
		self.window = window
		self.mediaObject = Phonon.MediaObject(self.window)   #实例化一个媒体对象
		self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self.window)   #实例化音频输出
		Phonon.createPath(self.mediaObject, self.audioOutput)   #将上面的媒体对象作为音频来源并对接到音频输出
		self.mediaObject.stateChanged.connect(self.handleStateChanged)  #播放状态改变触发事件
		# -------加载播放列表----------
		self.songlist = {}
		self.songing = -5   #当前播放的歌曲编号
		fp = open("songs.list")
		s = fp.read()
		arr = s.split("\n")
		for index ,value in enumerate (arr): 
			if value == '':
				continue
			self.songlist[index] = value
			item = QListWidgetItem (" "+str(index+1)+"   "+u""+os.path.basename(value)+"")
			item.setSizeHint (QSize(250,35))
			window.songList.addItem(item)
		#----------加载进度条----------
		self.seek = Phonon.SeekSlider(self.mediaObject,window.proWgt) 
    # ==============================播放、暂停======================================
	def playit(self,songUrl=''):    #指定播放
		songNum = (int)(songUrl[1])-1
		songUrl = self.songlist[songNum]
		self.songing = int(songNum)
		# print u""+songUrl+""
		self.mediaObject.setCurrentSource(Phonon.MediaSource(u""+songUrl+""))
		self.mediaObject.play()  
	def playsong(self):  #自动播放当前item
		print 'playsong'
	# ==============================下一曲====================================
	def next(self):
		lens = len(self.songlist)
		if self.songing == -5:
			self.songing = lens-1
		if lens-self.songing>1:
			songUrl = self.songlist[self.songing+1]
			self.mediaObject.setCurrentSource(Phonon.MediaSource(u""+songUrl+""))
			self.mediaObject.play()
			self.songing = self.songing+1
		else:
			songUrl = self.songlist[0]
			self.mediaObject.setCurrentSource(Phonon.MediaSource(u""+songUrl+""))
			self.mediaObject.play()
			self.songing = 0
	# ===============================上一曲=====================================
	def pre(self):
		if self.songing == -5:
			self.songing = 0
		if self.songing != 0:
			self.songing-=1
		else:
			self.songing = len(self.songlist)-1
		songUrl = self.songlist[self.songing]
		self.mediaObject.setCurrentSource(Phonon.MediaSource(u""+songUrl+""))
		self.mediaObject.play()

# ============================回调函数============================================
	# ------------播放状态发生改变-----------------------
	def handleStateChanged(self, newstate, oldstate):
		if newstate == Phonon.PlayingState:  
			print 'playing'
		elif newstate == Phonon.StoppedState:
			print u"停止"
			
		elif newstate == Phonon.PausedState:
			print u"暂停"
			lens = len(self.songlist)
			if lens-self.songing>1:
				self.songing += 1
			else:
				self.songing = 0
			songUrl = self.songlist[self.songing]
			self.mediaObject.setCurrentSource(Phonon.MediaSource(u""+songUrl+""))
			self.mediaObject.play()
				
		elif newstate == Phonon.ErrorState:  
			source = self.mediaObject.currentSource().fileName()   #抛出播放出错的文件名
			print 'ERROR: could not play:', source.toLocal8Bit().data()
  # ========================事件集合========================================

  	def evt(self):
  		self.mediaObject.stateChanged.connect(self.handleStateChanged)  #播放状态改变触发事件

if __name__ == "__main__":
	fp = open("songs.list")
	s = fp.read()
	arr = s.split("\n")
	for v in arr:
		print v