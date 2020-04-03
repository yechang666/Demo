# -*- coding: utf-8 -*-

# history:
# 4: info output use old key but carrying new value in 3.0
# 	update for additional info array.
# 5: presentation window add id, value same as event id.
# 6: move sg bfp config to excel.
#	globalfileid generate by 'f12'
#	endtime auto generate when start time exist, duration exist but no endtime.
#	change to ntp timestamp.
#	alternatives not processing empty string.
#	service schedule content id auto generate when empty.
#	icon uri, service description empty no output.
#	SLTInetUrl config in excel stream url and sls config in python.
# 7: supporting virtual playlist.
#	output icon uri list.
# 8: sls www url derived from sg url.
#	ref program no name bug fix.
#	generate poster icon image uri index for swserver api.
#	event content override add.
#	service icon uri generate using icon url when empty.
#	can generate ad icon image for app page.
#	delete key when key not exist in processResIdReference exception bug fix.
# 9: reference program can generate presentation window correctly.
#	reference event can always have presentation window id.
#	date time can handle 2014/9/23 2:00
# 10: remove duplicate content fragment.
#	remove vpl output for services no need vpl.
#	duplicate content uri replacement list text file add.

import collections
import json
import sys
import csv
import codecs
#import time
from datetime import datetime, timedelta
import calendar
import copy
import urlparse
import os

HEAD_ROW_NUM = 2
PROTOCOL_VERSION = 6

PAT_ITEM_NUM = 6 + 13
SDT_ITEM_NUM = 9 + 3

# INPUT_CODEC = "gb2312"
INPUT_CODEC = "gb2312"
OUTPUT_CODEC = "utf8"

SG_SERVICECATEGORY_VIDEO = 1
SG_SERVICECATEGORY_AUDIO = 2
SG_SERVICECATEGORY_PL = 3
SG_SERVICECATEGORY_SG = 4
SG_SERVICECATEGORY_EAS = 5
SG_SERVICECATEGORY_BFP = 6
SG_SERVICECATEGORY_RT = 7
SG_SERVICECATEGORY_EMM = 8
SG_SERVICECATEGORY_SPT = 9

STREAMTYPE_VOD = 6
STREAMTYPE_LIST = 10

PAGETYPE_GENERAL_LIST = 1
PAGETYPE_MEIZHOUDIANYING = 5
PAGETYPE_PODCAST = 8
PAGETYPE_YUGAOPIAN = 9
PAGETYPE_XINGYUNCD = 10
PAGETYPE_FUMEITI = 11
PAGETYPE_PODCAST_VIDEO = 13
PAGETYPE_JIQUN_CHEXUNSUDI_TYPE = 19
PAGETYPE_JIQUN_JINGCAIYINGSHI_TYPE = 20
PAGETYPE_JIQUN_APP_ENTERTAINMENT_TYPE = 21
PAGETYPE_JIQUN_MINI_VIDEO_TYPE = 22
VPL_PAGETYPE_LIST = [PAGETYPE_MEIZHOUDIANYING, PAGETYPE_PODCAST, PAGETYPE_YUGAOPIAN, 
	PAGETYPE_XINGYUNCD, PAGETYPE_FUMEITI, PAGETYPE_PODCAST_VIDEO, 
	PAGETYPE_JIQUN_CHEXUNSUDI_TYPE, PAGETYPE_JIQUN_JINGCAIYINGSHI_TYPE, PAGETYPE_JIQUN_APP_ENTERTAINMENT_TYPE, PAGETYPE_JIQUN_MINI_VIDEO_TYPE]

OPENTYPE_PLAY_ONLY = 1
OPENTYPE_SHOW_ONLY = 2
OPENTYPE_CUSTOM = 3

SLTINETURL_TYPE_SLS = 1
SLTINETURL_TYPE_SG = 2
SLTINETURL_TYPE_SPT = 3

EVENT_TYPE_NORMAL = 0
EVENT_TYPE_PROGRAM = 1
EVENT_TYPE_BFP = 2

RES_TYPE_EVENT = 0
RES_TYPE_PROGRAM = 1

SPEECH_ALTERNATIVE_TEXT_SEPRATOR = ','

SLT_FILE_NAME = 'slt.json'
SLS_FILE_NAME = 'sls.json'
SG_FILE_NAME = 'sg.json'
INFO_FILE_NAME = 'info_sid.json'
URI_LIST_FILE_NAME = 'uri.txt'
DUPLICATE_ID_LIST_FILE_NAME = 'dupid.json'

LANGUAGE_ZH_CN = 'zh-CN'

RESOURCE_FOLDER_NAME = 'resources/'
FOLDER_NAME_BFP = 'bfp'
FOLDER_NAME_VOD = 'vod'
FOLDER_NAME_CT = 'ct'

BFP_MOVIE_ICON_POSTER_FILE_NAME_SUFFIX = '_poster'
APP_ICON_AD_FILE_NAME_SUFFIX = '_ad'

SG_URI_PREFIX = 'tag:gvmedia.com.cn,2017:'
SG_URI_SERVICE_ID_PATH_PREFIX = 'silkwave/sg/services'
SG_URI_SCHEDULE_ID_PATH_PREFIX = 'silkwave/sg/schedules'
SG_URI_CONTENT_ID_PATH_PREFIX = 'silkwave/sg/contents'
SG_URI_ICON_ID_PATH_PREFIX = 'silkwave/icons'
SG_URI_PATH_SEPARATOR = '/'

DATA_TABLE_DICT_KEY_STREAM_TYPE = "stream_type"
DATA_TABLE_DICT_KEY_PAGE_TYPE = "page_type"
DATA_TABLE_DICT_KEY_SERVICE_NAME = "service_name"
DATA_TABLE_DICT_KEY_STREAM_URL = "stream_url"
DATA_TABLE_DICT_KEY_BANDWIDTH = "bandwidth"
DATA_TABLE_DICT_KEY_SERVICE_PROVIDER_NAME = "service_provider_name"
DATA_TABLE_DICT_KEY_ICON_URL = "icon_url"
DATA_TABLE_DICT_KEY_EVENT_ID = "event_id"
DATA_TABLE_DICT_KEY_START_TIME = "start_time"
DATA_TABLE_DICT_KEY_DURATION = "duration"
DATA_TABLE_DICT_KEY_RUNNING_STATUS = "running_status"
DATA_TABLE_DICT_KEY_EVENT_NAME = "event_name"
DATA_TABLE_DICT_KEY_RATING = "rating"
DATA_TABLE_DICT_KEY_YEAR = "year"
DATA_TABLE_DICT_KEY_DIRECTOR = "director"
DATA_TABLE_DICT_KEY_STARRING = "starring"
DATA_TABLE_DICT_KEY_SPEECH_EVENT_NAME = "speech_event_name"
DATA_TABLE_DICT_KEY_SPEECH_SERVICE_NAME = "speech_service_name"
DATA_TABLE_DICT_KEY_FREE_CA_MODE = "free_ca_mode"
DATA_TABLE_DICT_KEY_INFLATE_MODE = "inflate_mode"
DATA_TABLE_DICT_KEY_SEGMENTER_URL = "segmenter_url"
DATA_TABLE_DICT_KEY_SPEECH_SERVICE_PROVIDER_NAME = "speech_service_provider_name"
DATA_TABLE_DICT_KEY_RES_ID = "res_id"
DATA_TABLE_DICT_KEY_OPEN_TYPE = "open_type"

INFO_DICT_KEY_STREAM_OUTPUT_URL = "stream_output_url"
INFO_DICT_KEY_CTS_ID = "cts_id"
INFO_DICT_KEY_ISS_ID = "iss_id"

DATA_TABLE_DICT_KEY_SLS_CTSID = "sls_ctsId"
DATA_TABLE_DICT_KEY_SLS_ISSID = "sls_issId"
DATA_TABLE_DICT_KEY_SG_SERVICE_ID = "sg_service_id"
DATA_TABLE_DICT_KEY_SG_SCHEDULE_ID = "sg_schedule_id"
DATA_TABLE_DICT_KEY_SG_SERVICE_VERSION = "sg_service_version"
DATA_TABLE_DICT_KEY_SG_SCHEDULE_VERSION = "sg_schedule_version"
DATA_TABLE_DICT_KEY_ICON_URI = "icon_uri"
DATA_TABLE_DICT_KEY_SG_CONTENT_ID = "sg_content_id"
DATA_TABLE_DICT_KEY_REGION = "region"
DATA_TABLE_DICT_KEY_SG_EVENT_VERSION = "sg_event_version"

SG_DICT_KEY_SERVICEID = "serviceId"
SG_DICT_KEY_SLTSVCSEQNUM = "sltSvcSeqNum"
SG_DICT_KEY_CTSID = "ctsId"
SG_DICT_KEY_ISSID = "issId"
SG_DICT_KEY_ID = "id"
SG_DICT_KEY_VERSION = "version"
SG_DICT_KEY_SERVICECATEGORY = "serviceCategory"
SG_DICT_KEY_SHORTSERVICENAME = "shortServiceName"
SG_DICT_KEY_SERVICETYPE = "ServiceType"
SG_DICT_KEY_SERVICE = "Service"
SG_DICT_KEY_BROADCASTSVCSIGNALING = "BroadcastSvcSignaling"
SG_DICT_KEY_SLSPROTOCOL = "slsProtocol"
SG_DICT_KEY_SLTINETURL = "SLTInetUrl"
SG_DICT_KEY_URLTYPE = "urlType"
SG_DICT_KEY_URL = "url"
SG_DICT_KEY_USERSERVICEDESCRIPTION = "UserServiceDescription"
SG_DICT_KEY_SGSERVICEIDREF = "sgServiceIdRef"
SG_DICT_KEY_NAME = "Name"
SG_DICT_KEY_TEXT = "text"
SG_DICT_KEY_LANG = "lang"
SG_DICT_KEY_VPL = "VPL"
SG_DICT_KEY_CT = "CT"
SG_DICT_KEY_VOD = "VOD"
SG_DICT_KEY_PLAYURL = "PlayUrl"
SG_DICT_KEY_SGCONTENTIDREF = "sgContentIdRef"
SG_DICT_KEY_CTURL = "CtUrl"
SG_DICT_KEY_BW = "bw"
SG_DICT_KEY_DESCRIPTION = "Description"
SG_DICT_KEY_PRIVATEEXT = "PrivateExt"
SG_DICT_KEY_SERVICEICON = "ServiceIcon"
SG_DICT_KEY_URI = "uri"
SG_DICT_KEY_SCHEDULE = "Schedule"
SG_DICT_KEY_SERVICEREFERENCE = "ServiceReference"
SG_DICT_KEY_CONTENTREFERENCE = "ContentReference"
SG_DICT_KEY_IDREF = "idRef"
SG_DICT_KEY_PRESENTATIONWINDOW = "PresentationWindow"
SG_DICT_KEY_STARTTIME = "startTime"
SG_DICT_KEY_ENDTIME = "endTime"
SG_DICT_KEY_DURATION = "duration"
SG_DICT_KEY_GENRE = "Genre"
SG_DICT_KEY_CONTENT = "Content"
SG_DICT_KEY_CONTENTICON = "ContentIcon"
SG_DICT_KEY_DESCRIPTIONEXT = "DescriptionExt"
SG_DICT_KEY_TYPE = "type"
SG_DICT_KEY_ALTERNATIVES = "Alternatives"
SG_DICT_KEY_BFP = "BFP"
SG_DICT_KEY_GLOBALFILEID = "globalFileId"
SG_DICT_KEY_PROTECTED = "protected"
SG_DICT_KEY_HIDDEN = "hidden"
SG_DICT_KEY_INFLATEMODE = "inflateMode"
SG_DICT_KEY_WEIGHT = "weight"

INNER_DICT_KEY_REFERENCE_RES_ID = '_refid'
INNER_DICT_KEY_SERVICE_CT = '_svcct'
INNER_DICT_KEY_REMOVE_VPL = '_removevpl'

NTP2UNIX = 2208988800 # seconds from NTP to UNIX epoch

SLTINETURL_SUFFIX_SLS = "sls"

sltInetUrlArr = []
#jsonDict = {}
#jsonDict[SG_DICT_KEY_URL] = "http://fes-dev.silkwave.tv:11080/silkwave/sls"
#jsonDict[SG_DICT_KEY_URLTYPE] = SLTINETURL_TYPE_SLS
#sltInetUrlArr.append(jsonDict)
#jsonDict = {}
#jsonDict[SG_DICT_KEY_URL] = "http://192.168.10.53:10082/silkwave/sg"
#jsonDict[SG_DICT_KEY_URLTYPE] = 2
#sltInetUrlArr.append(jsonDict)
#jsonDict = {}
#jsonDict[SG_DICT_KEY_URL] = "http://192.168.10.53:10082/silkwave/spt"
#jsonDict[SG_DICT_KEY_URLTYPE] = 3
#sltInetUrlArr.append(jsonDict)

class ReferenceInfo:
	def __init__(self):
		self.sgsvcidx = None
		self.sgschidx = None
		self.sgconidx = None
		self.sltsvcidx = None
		self.slsidx = None
		self.vplctidx = None
		self.vplbfpidx = None
		self.vplvodidx = None
		self.vplucidx = None
		self.schconrefidx = None
		self.pwinidx = None
		self.resid = None
		self.restype = None
		self.pwinid = None
	
	def __str__(self):
		return 'sgsvcidx: '+str(self.sgsvcidx)+\
		' sgschidx: '+str(self.sgschidx)+\
		' sgconidx: '+str(self.sgconidx)+\
		' sltsvcidx: '+str(self.sltsvcidx)+\
		' slsidx: '+str(self.slsidx)+\
		' vplctidx: '+str(self.vplctidx)+\
		' vplbfpidx: '+str(self.vplbfpidx)+\
		' vplvodidx: '+str(self.vplvodidx)+\
		' vplucidx: '+str(self.vplucidx) +\
		' schconrefidx: '+str(self.schconrefidx) +\
		' pwinidx: '+str(self.pwinidx) +\
		' resid: '+str(self.resid) +\
		' restype: '+str(self.restype) +\
		' pwinid: '+str(self.pwinid)
		
	def setProgramInfo(self, programinfo):
		self.sgsvcidx = programinfo.sgsvcidx
		self.sgschidx = programinfo.sgschidx
		self.sltsvcidx = programinfo.sltsvcidx
		self.slsidx = programinfo.slsidx
	'''	
	def makeReferenceInfo(self, sgsvcidx = None, sgschidx = None, sgconidx = None, sltsvcidx = None, slsidx = None, 
			vplctidx = None, vplbfpidx = None, vplvodidx = None, vplucidx = None, 
			schconrefidx = None, pwinidx = None, resid = None, restype = None):
		self.sgsvcidx = sgsvcidx
		self.sgschidx = sgschidx
		self.sgconidx = sgconidx
		self.sltsvcidx = sltsvcidx
		self.slsidx = slsidx
		self.vplctidx = vplctidx
		self.vplbfpidx = vplbfpidx
		self.vplvodidx = vplvodidx
		self.vplucidx = vplucidx
		self.schconrefidx = schconrefidx
		self.pwinidx = pwinidx
		self.resid = resid
		self.restype = restype
	'''

class EsgGenerator(object):
	"""generate json of  esg,scene,and push stream info from csv"""

	def __init__(self, path, output, versions):
		self.path = path
		self.output = output
		self.versions = versions
		reader = csv.reader(open(self.path))
		self.csvItem = [row for row in reader]
		self.refList = []
		self.resTable = {}

	def generateAll(self):
		self.generateEsg(self.csvItem)
		#self.generateInfo(self.csvItem)
		#self.generateTagInfo(self.csvItem)

	def generateEsg(self, csvItem):
		global sltInetUrlArr
		
		slsJsonArr = []
		sltServiceArr = []
		sgServiceArr = []
		sgScheduleArr = []
		sgContentArr = []
		infoArr = []
		uriArr = []
		filePathArr = []
		sgServiceStreamUrl = None
		
		allLen = len(csvItem) - HEAD_ROW_NUM
		head = csvItem[HEAD_ROW_NUM - 1]
		handledNum = 0
		while handledNum < allLen:
			nextServiceIndex = HEAD_ROW_NUM + handledNum
			mainRow = csvItem[nextServiceIndex]
			handledNum += 1
			# pat
			onePat = self.__getOnePat(head, mainRow)
			
			# sdt
			oneSdt = self.__getOneSdt(head, mainRow)

			# found all event
			eitBeginIndex = self.__getEitStartIndex(head)
			# use start_time to determine event num
			#startTimeLine = csvItem[nextServiceIndex + 1]
			startTimeLine = csvItem[nextServiceIndex]	# use event_id to determine event num
			eventNum = self.__getEventNum(eitBeginIndex, startTimeLine)
			# eit content's first column is ""
			eventItemNum = 0
			nextLine = csvItem[HEAD_ROW_NUM + handledNum]
			while nextLine[0] is None or nextLine[0] == "":
				handledNum += 1
				eventItemNum += 1
				if handledNum >= allLen:
					break
				nextLine = csvItem[HEAD_ROW_NUM + handledNum]
			
			#print eventNum,onePat
			
			programResId = None
			if DATA_TABLE_DICT_KEY_RES_ID in onePat:
				programResId = onePat[DATA_TABLE_DICT_KEY_RES_ID]
			
			streamtype = onePat[DATA_TABLE_DICT_KEY_STREAM_TYPE]
			#if streamtype == 10 and programResId != 111 and programResId != 112:
			#if streamtype == 10:
			#	continue
			
			opentype = None
			if DATA_TABLE_DICT_KEY_OPEN_TYPE in oneSdt:
				opentype = oneSdt[DATA_TABLE_DICT_KEY_OPEN_TYPE]
			pagetype = None
			if DATA_TABLE_DICT_KEY_PAGE_TYPE in oneSdt:
				pagetype = oneSdt[DATA_TABLE_DICT_KEY_PAGE_TYPE]
			
			infoDict = {}
			
			serviceID = onePat[SG_DICT_KEY_SERVICEID]
			serviceStreamUrl = onePat[DATA_TABLE_DICT_KEY_STREAM_URL]
			serviceCategory = onePat[SG_DICT_KEY_SERVICECATEGORY]
			
			svcRefInfo = ReferenceInfo()
			svcRefInfo.resid = programResId
			svcRefInfo.restype = RES_TYPE_PROGRAM
			
			# slt
			jsonDict = {}
			jsonDict[SG_DICT_KEY_SERVICEID] = serviceID
			jsonDict[SG_DICT_KEY_SLTSVCSEQNUM] = onePat[SG_DICT_KEY_SLTSVCSEQNUM]
			jsonDict[SG_DICT_KEY_SERVICECATEGORY] = serviceCategory
			if DATA_TABLE_DICT_KEY_SERVICE_NAME in oneSdt:
				jsonDict[SG_DICT_KEY_SHORTSERVICENAME] = oneSdt[DATA_TABLE_DICT_KEY_SERVICE_NAME]
			if DATA_TABLE_DICT_KEY_FREE_CA_MODE in oneSdt:
				jsonDict[SG_DICT_KEY_PROTECTED] = oneSdt[DATA_TABLE_DICT_KEY_FREE_CA_MODE] != 0
				infoDict[DATA_TABLE_DICT_KEY_FREE_CA_MODE] = oneSdt[DATA_TABLE_DICT_KEY_FREE_CA_MODE]

			if DATA_TABLE_DICT_KEY_SLS_CTSID in onePat:
				bcsvcdict = {}
				bcsvcdict[SG_DICT_KEY_SLSPROTOCOL] = 3
				bcsvcdict[SG_DICT_KEY_CTSID] = onePat[DATA_TABLE_DICT_KEY_SLS_CTSID]
				bcsvcdict[SG_DICT_KEY_ISSID] = onePat[DATA_TABLE_DICT_KEY_SLS_ISSID]
				jsonDict[SG_DICT_KEY_BROADCASTSVCSIGNALING] = bcsvcdict
				
				infoArr.append({INFO_DICT_KEY_CTS_ID:onePat[DATA_TABLE_DICT_KEY_SLS_CTSID], INFO_DICT_KEY_ISS_ID:onePat[DATA_TABLE_DICT_KEY_SLS_ISSID]})
			
			svcRefInfo.sltsvcidx = len(sltServiceArr)
			sltServiceArr.append(jsonDict)
			
			sgServiceID = onePat[DATA_TABLE_DICT_KEY_SG_SERVICE_ID]
			if sgServiceID == '':
				sgServiceID = SG_URI_PREFIX + SG_URI_SERVICE_ID_PATH_PREFIX + SG_URI_PATH_SEPARATOR + str(serviceID)
			
			# sls
			usddict = {}
			usddict[SG_DICT_KEY_SERVICEID] = serviceID
			usddict[SG_DICT_KEY_SGSERVICEIDREF] = sgServiceID
			if DATA_TABLE_DICT_KEY_SERVICE_NAME in oneSdt:
				usddict[SG_DICT_KEY_NAME] = [{SG_DICT_KEY_TEXT:oneSdt[DATA_TABLE_DICT_KEY_SERVICE_NAME], SG_DICT_KEY_LANG:LANGUAGE_ZH_CN}]
			
			isNeedRecordCt = streamtype != STREAMTYPE_VOD and streamtype != STREAMTYPE_LIST
			ctctsid = None
			ctissid = None
			vpldict = {}
			if SG_DICT_KEY_CTSID in onePat:
				ctctsid = onePat[SG_DICT_KEY_CTSID]
				ctissid = onePat[SG_DICT_KEY_ISSID]
				
				bw = None
				if DATA_TABLE_DICT_KEY_BANDWIDTH in oneSdt:
					bw = oneSdt[DATA_TABLE_DICT_KEY_BANDWIDTH]
					infoDict[DATA_TABLE_DICT_KEY_BANDWIDTH] = bw
				cturl = onePat[SG_DICT_KEY_CTURL]
				
				inflatemode = None
				if DATA_TABLE_DICT_KEY_INFLATE_MODE in onePat:
					inflatemode = onePat[DATA_TABLE_DICT_KEY_INFLATE_MODE]
					infoDict[DATA_TABLE_DICT_KEY_INFLATE_MODE] = inflatemode
				
				ctdict = self.makeCtDict(ctctsid, ctissid, cturl, bw, inflatemode, serviceStreamUrl, sgserviceidref = sgServiceID)
				if isNeedRecordCt:
					vpldict[SG_DICT_KEY_CT] = [ctdict]
				vpldict[INNER_DICT_KEY_SERVICE_CT] = ctdict
				
				infoDict[DATA_TABLE_DICT_KEY_STREAM_TYPE] = serviceCategory	# use old key but carrying new category.
				infoDict[INFO_DICT_KEY_CTS_ID] = ctctsid
				infoDict[INFO_DICT_KEY_ISS_ID] = ctissid
				if DATA_TABLE_DICT_KEY_SEGMENTER_URL in oneSdt:
					infoDict[INFO_DICT_KEY_STREAM_OUTPUT_URL] = oneSdt[DATA_TABLE_DICT_KEY_SEGMENTER_URL]
				
				"""
				if streamtype != STREAMTYPE_VOD and streamtype != STREAMTYPE_LIST:
					#ctdict = {}
					#ctdict[SG_DICT_KEY_CTSID] = ctctsid
					#ctdict[SG_DICT_KEY_ISSID] = ctissid
					bw = None
					if DATA_TABLE_DICT_KEY_BANDWIDTH in oneSdt:
						bw = oneSdt[DATA_TABLE_DICT_KEY_BANDWIDTH]
						#ctdict[SG_DICT_KEY_BW] = bw
						infoDict[DATA_TABLE_DICT_KEY_BANDWIDTH] = bw
					#if serviceStreamUrl != '':
					#	ctdict[SG_DICT_KEY_PLAYURL] = [serviceStreamUrl]
					cturl = onePat[SG_DICT_KEY_CTURL]
					#ctdict[SG_DICT_KEY_CTURL] = [cturl]
					
					inflatemode = None
					if DATA_TABLE_DICT_KEY_INFLATE_MODE in onePat:
						inflatemode = onePat[DATA_TABLE_DICT_KEY_INFLATE_MODE]
						infoDict[DATA_TABLE_DICT_KEY_INFLATE_MODE] = inflatemode
					
					ctdict = self.makeCtDict(ctctsid, ctissid, cturl, bw, inflatemode, serviceStreamUrl, sgserviceidref = sgServiceID)
					vpldict[SG_DICT_KEY_CT] = [ctdict]
					
					#infoDict[DATA_TABLE_DICT_KEY_STREAM_TYPE] = streamtype
					infoDict[DATA_TABLE_DICT_KEY_STREAM_TYPE] = serviceCategory	# use old key but carrying new category.
					infoDict[INFO_DICT_KEY_CTS_ID] = ctctsid
					infoDict[INFO_DICT_KEY_ISS_ID] = ctissid
					#if DATA_TABLE_DICT_KEY_INFLATE_MODE in onePat:
					#	infoDict[DATA_TABLE_DICT_KEY_INFLATE_MODE] = onePat[DATA_TABLE_DICT_KEY_INFLATE_MODE]
					if DATA_TABLE_DICT_KEY_SEGMENTER_URL in oneSdt:
						infoDict[INFO_DICT_KEY_STREAM_OUTPUT_URL] = oneSdt[DATA_TABLE_DICT_KEY_SEGMENTER_URL]
				"""
				
			svcRefInfo.slsidx = len(slsJsonArr)
			slsJsonArr.append({SG_DICT_KEY_USERSERVICEDESCRIPTION:usddict, SG_DICT_KEY_VPL:vpldict})

			if not self.isVplProgram(streamtype, opentype, pagetype):
				vpldict[INNER_DICT_KEY_REMOVE_VPL] = 1
			
			vplBfpArr = []
			vplVodArr = []
			vplCtArr = []
			
			if len(infoDict) > 0 and isNeedRecordCt:
				infoArr.append(infoDict)
			
			# sg service
			sgservicedict = {}
			sgservicedict[SG_DICT_KEY_ID] = sgServiceID
			sgservicedict[SG_DICT_KEY_VERSION] = onePat[DATA_TABLE_DICT_KEY_SG_SERVICE_VERSION]
			sgservicedict[SG_DICT_KEY_SERVICETYPE] = [onePat[SG_DICT_KEY_SERVICETYPE]]
			if DATA_TABLE_DICT_KEY_SERVICE_NAME in oneSdt:
				namedict = {}
				namedict[SG_DICT_KEY_TEXT] = oneSdt[DATA_TABLE_DICT_KEY_SERVICE_NAME]
				
				if DATA_TABLE_DICT_KEY_SPEECH_SERVICE_NAME in oneSdt:
					namealtarr = oneSdt[DATA_TABLE_DICT_KEY_SPEECH_SERVICE_NAME].split(SPEECH_ALTERNATIVE_TEXT_SEPRATOR)
					namedict[SG_DICT_KEY_ALTERNATIVES] = namealtarr
				
				sgservicedict[SG_DICT_KEY_NAME] = [namedict]
				
			serviceDescription = oneSdt[DATA_TABLE_DICT_KEY_SERVICE_PROVIDER_NAME]
			if serviceDescription != '':
				sgservicedict[SG_DICT_KEY_DESCRIPTION] = [{SG_DICT_KEY_TEXT:serviceDescription}]
			
			iconuri = oneSdt[DATA_TABLE_DICT_KEY_ICON_URI]
			
			iconuripath = None
			iconurl = oneSdt[DATA_TABLE_DICT_KEY_ICON_URL]
			uriinfo = self.resourceUrl2Uri(iconurl)
			if uriinfo != None:
				iconuripath = uriinfo[1]
				if iconuri == '' and uriinfo[0] != '' and iconuripath != '':
					iconuri = uriinfo[0]
					
			#iconuri = oneSdt[DATA_TABLE_DICT_KEY_ICON_URI]
			#if iconuri != '':
			#	privateextdict = {}
			#	privateextdict[SG_DICT_KEY_SERVICEICON] = [{SG_DICT_KEY_URI:iconuri}]
			#	sgservicedict[SG_DICT_KEY_PRIVATEEXT] = privateextdict
			#else:
			#	if uriinfo != None:
			#		iconuri = uriinfo[0]
					
			if iconuri != '':
				privateextdict = {}
				privateextdict[SG_DICT_KEY_SERVICEICON] = [{SG_DICT_KEY_URI:iconuri}]
				sgservicedict[SG_DICT_KEY_PRIVATEEXT] = privateextdict
				
				self.addUriInfo(uriArr, filePathArr, iconuri, iconuripath)
				
			svcRefInfo.sgsvcidx = len(sgServiceArr)
			sgServiceArr.append(sgservicedict)
			
			sgScheduleID = onePat[DATA_TABLE_DICT_KEY_SG_SCHEDULE_ID]
			if sgScheduleID == '':
				sgScheduleID = SG_URI_PREFIX + SG_URI_SCHEDULE_ID_PATH_PREFIX + SG_URI_PATH_SEPARATOR + str(serviceID)
			
			# sg schedule, content
			sgscheduledict = {}
			sgscheduledict[SG_DICT_KEY_ID] = sgScheduleID
			sgscheduledict[SG_DICT_KEY_VERSION] = onePat[DATA_TABLE_DICT_KEY_SG_SCHEDULE_VERSION]
			sgscheduledict[SG_DICT_KEY_SERVICEREFERENCE] = {SG_DICT_KEY_IDREF:sgServiceID}

			svcRefInfo.sgschidx = len(sgScheduleArr)
			self.addRes(programResId, RES_TYPE_PROGRAM, svcRefInfo)
			
			vplweight = 0
			if eventNum > 0:
				contentrefarr = []
				for h in range(0, eventNum):
					sgcontentdict = {}
					sgcontentdict[SG_DICT_KEY_SERVICEREFERENCE] = [{SG_DICT_KEY_IDREF:sgServiceID}]
					
					evtRefInfo = ReferenceInfo()
					evtRefInfo.restype = RES_TYPE_EVENT
					evtRefInfo.setProgramInfo(svcRefInfo)
					
					contentrefdict = {}
					preswindowdict = {}
					movie = {}
					bfpdict = {}
					voddict = {}
					namealtarr = None
					streamurl = None
					iconuri = None
					iconuripath = None
					#namedict = None
					namedict = {SG_DICT_KEY_TEXT:''}	# name must exist.
					globalfileid = None
					starttime = None
					endtime = None
					duration = None
					contentid = None
					eventtype = None
					refresid = None
					resid = None
					isRef = False
					uriinfo = None
					eventid = int(mainRow[eitBeginIndex + 2 + h])  # eitId
					for m in range(1, eventItemNum + 1):
						eitLine = csvItem[nextServiceIndex + m]
						if eitLine[eitBeginIndex + 2 + h] == "":
							continue
						eitKey = eitLine[eitBeginIndex]
						eitVal = eitLine[eitBeginIndex + 2 + h]
						eitValDecoded = codecs.decode(eitVal, INPUT_CODEC)
						if eitKey == DATA_TABLE_DICT_KEY_SG_CONTENT_ID:
							contentid = eitValDecoded
						elif eitKey == DATA_TABLE_DICT_KEY_START_TIME:
							starttime = self.format_datatime(eitValDecoded, True)
							if starttime != None:
								preswindowdict[SG_DICT_KEY_STARTTIME] = starttime
						elif eitKey == SG_DICT_KEY_ENDTIME:
							endtime = self.format_datatime(eitValDecoded, True)
							if endtime != None:
								preswindowdict[eitKey] = endtime
						elif eitKey == SG_DICT_KEY_GENRE:
							sgcontentdict[eitKey] = [{SG_DICT_KEY_TEXT:eitValDecoded}]
						elif eitKey == DATA_TABLE_DICT_KEY_REGION or eitKey == DATA_TABLE_DICT_KEY_DIRECTOR \
							or eitKey == DATA_TABLE_DICT_KEY_STARRING:
							movie[eitKey] = eitValDecoded
						elif eitKey == DATA_TABLE_DICT_KEY_RATING:
							movie[eitKey] = float(eitVal)
						elif eitKey == DATA_TABLE_DICT_KEY_YEAR:
							movie[eitKey] = int(eitVal)
						elif eitKey == DATA_TABLE_DICT_KEY_SPEECH_EVENT_NAME:
							namealtarr = eitValDecoded.split(SPEECH_ALTERNATIVE_TEXT_SEPRATOR)
						elif eitKey == DATA_TABLE_DICT_KEY_STREAM_URL:
							streamurl = eitValDecoded
							bfpdict[SG_DICT_KEY_PLAYURL] = [eitValDecoded]
							voddict[SG_DICT_KEY_PLAYURL] = [eitValDecoded]
						elif eitKey == DATA_TABLE_DICT_KEY_ICON_URI:
							iconuri = eitValDecoded
						elif eitKey == DATA_TABLE_DICT_KEY_ICON_URL:
							uriinfo = self.resourceUrl2Uri(eitValDecoded)
							if uriinfo != None:
								iconuripath = uriinfo[1]
								if iconuri == None:
									iconuri = uriinfo[0]
						elif eitKey == SG_DICT_KEY_TEXT:
							sgcontentdict[SG_DICT_KEY_DESCRIPTION] = [{SG_DICT_KEY_TEXT:eitValDecoded}]
						elif eitKey == DATA_TABLE_DICT_KEY_EVENT_NAME:
							namedict = {SG_DICT_KEY_TEXT:eitValDecoded}
						elif eitKey == SG_DICT_KEY_DURATION:
							duration = int(eitVal)
							preswindowdict[eitKey] = duration
						elif eitKey == DATA_TABLE_DICT_KEY_SG_EVENT_VERSION:
							sgcontentdict[SG_DICT_KEY_VERSION] = int(eitVal)
						elif eitKey == SG_DICT_KEY_GLOBALFILEID:
							isFileID = (eitVal[0].lower() == 'f')
							if isFileID:
								fileid = int(eitVal[1:])
								globalfileid = self.calculateGlobalFileID(ctctsid, ctissid, fileid)
							else:
								globalfileid = int(eitVal)
							bfpdict[eitKey] = globalfileid
						elif eitKey == SG_DICT_KEY_TYPE:
							eventtype = int(eitVal)
						elif eitKey == DATA_TABLE_DICT_KEY_RES_ID:
							isRef = (eitVal[0].lower() == 'r')
							if isRef:
								refresid = int(eitVal[1:])
							else:
								resid = int(eitVal)
					
					if contentid == None:
						contentid = SG_URI_PREFIX + SG_URI_CONTENT_ID_PATH_PREFIX + SG_URI_PATH_SEPARATOR + str(serviceID) + SG_URI_PATH_SEPARATOR + str(eventid)
					
					contentrefdict[SG_DICT_KEY_IDREF] = contentid
					sgcontentdict[SG_DICT_KEY_ID] = contentid
					bfpdict[SG_DICT_KEY_SGCONTENTIDREF] = contentid
					voddict[SG_DICT_KEY_SGCONTENTIDREF] = contentid
					
					if endtime == None and starttime != None and duration != None:
						preswindowdict[SG_DICT_KEY_ENDTIME] = starttime + duration
					
					if len(preswindowdict) > 0:
					#if isRef or len(preswindowdict) > 0:
						preswindowdict[SG_DICT_KEY_ID] = eventid
						contentrefdict[SG_DICT_KEY_PRESENTATIONWINDOW] = [preswindowdict]
						evtRefInfo.pwinidx = 0

					isNeedDescExt = len(movie) > 0 and streamtype == STREAMTYPE_VOD
					if iconuri != None or isNeedDescExt:
						extdict = {}
						if iconuri != None:
							extdict[SG_DICT_KEY_CONTENTICON] = [{SG_DICT_KEY_URI:iconuri}]
							self.addUriInfo(uriArr, filePathArr, iconuri, iconuripath)
							if streamtype == STREAMTYPE_VOD:
								iconuriposter = self.makeFileNameWithSuffix(iconuri, BFP_MOVIE_ICON_POSTER_FILE_NAME_SUFFIX)
								extdict[SG_DICT_KEY_CONTENTICON] += [{SG_DICT_KEY_URI:iconuriposter}]
								self.addUriInfo(uriArr, filePathArr, iconuriposter, self.makeFileNameWithSuffix(iconuripath, BFP_MOVIE_ICON_POSTER_FILE_NAME_SUFFIX))
							if pagetype == PAGETYPE_JIQUN_APP_ENTERTAINMENT_TYPE:
								iconuriad = self.makeFileNameWithSuffix(iconuri, APP_ICON_AD_FILE_NAME_SUFFIX)
								extdict[SG_DICT_KEY_CONTENTICON] += [{SG_DICT_KEY_URI:iconuriad}]
								self.addUriInfo(uriArr, filePathArr, iconuriad, self.makeFileNameWithSuffix(iconuripath, APP_ICON_AD_FILE_NAME_SUFFIX))
							#if iconuri not in uriArr:
							#	uriArr.append(iconuri)
						if isNeedDescExt:
							#exttext = json.dumps(movie, indent=4, separators=(',', ': '), sort_keys=False, ensure_ascii=False)#.encode(OUTPUT_CODEC)
							exttext = json.dumps(movie, separators=(',', ': '), sort_keys=False)
							#exttext = exttext.replace('"','\"')
							#print exttext
							exttype = 1
							extdict[SG_DICT_KEY_DESCRIPTIONEXT] = [{SG_DICT_KEY_TEXT:exttext, SG_DICT_KEY_TYPE:exttype}]
						sgcontentdict[SG_DICT_KEY_PRIVATEEXT] = extdict

					if eventtype == EVENT_TYPE_BFP:
						#if globalfileid != None and streamtype == STREAMTYPE_VOD:
						if globalfileid != None:
							bfpdict[SG_DICT_KEY_WEIGHT] = h
							evtRefInfo.vplbfpidx = len(vplBfpArr)
							vplBfpArr.append(bfpdict)
					elif eventtype == EVENT_TYPE_PROGRAM:
						# use end time - start time as program play duration.
						if duration == None:
							stime = None
							etime = None
						else:
							stime = 0
							etime = stime + duration
							
						ctdict = self.makeCtDict(0, 0, '', bw = None, inflatemode = None, 
							playurl = streamurl, starttime = stime, endtime = etime, 
							sgserviceidref = None, weight = h)
						evtRefInfo.vplctidx = len(vplCtArr)
						vplCtArr.append(ctdict)
					else:
						if streamurl != None and streamtype != STREAMTYPE_VOD:
							voddict[SG_DICT_KEY_WEIGHT] = h
							evtRefInfo.vplvodidx = len(vplVodArr)
							vplVodArr.append(voddict)
					
					if namedict != None:
						if namealtarr != None:
							namedict[SG_DICT_KEY_ALTERNATIVES] = namealtarr
						sgcontentdict[SG_DICT_KEY_NAME] = [namedict]
					
					evtRefInfo.schconrefidx = len(contentrefarr)
					evtRefInfo.sgconidx = len(sgContentArr)
					contentrefarr.append(contentrefdict)
					sgContentArr.append(sgcontentdict)
					
					if resid != None:
						evtRefInfo.resid = resid
						self.addRes(resid, RES_TYPE_EVENT, evtRefInfo)
					
					if refresid != None:
						refevtresinfo = copy.copy(evtRefInfo)
						refevtresinfo.resid = refresid
						refevtresinfo.pwinid = eventid
						self.addReference(refresid, RES_TYPE_EVENT, refevtresinfo)
						
				sgscheduledict[SG_DICT_KEY_CONTENTREFERENCE] = contentrefarr

			sgScheduleArr.append(sgscheduledict)
			
			if len(vplBfpArr) > 0:
				vpldict[SG_DICT_KEY_BFP] = vplBfpArr
				
			if len(vplVodArr) > 0:
				vpldict[SG_DICT_KEY_VOD] = vplVodArr
			
			if len(vplCtArr) > 0:
				vpldict[SG_DICT_KEY_CT] = vplCtArr
		
			slttype = self.serviceCategory2SltUrlType(serviceCategory)
			if slttype != None:
				isnew = True
				for jsonDict in sltInetUrlArr:
					if jsonDict[SG_DICT_KEY_URLTYPE] == slttype:
						isnew = False
						break
						
				if isnew:
					jsonDict = {}
					jsonDict[SG_DICT_KEY_URL] = serviceStreamUrl
					jsonDict[SG_DICT_KEY_URLTYPE] = slttype
					sltInetUrlArr.append(jsonDict)

		# process res id reference.
		for ref in self.refList:
			resid = ref[0]
			srcinfo = self.findResInfoInResTable(resid)
			if srcinfo == None:
				continue
			self.processResIdReference(ref[2], srcinfo, sgServiceArr, sgScheduleArr, sgContentArr, sltServiceArr, slsJsonArr)
			
		# remove inner values.
		for sls in slsJsonArr:
			if INNER_DICT_KEY_SERVICE_CT in sls[SG_DICT_KEY_VPL]:
				del sls[SG_DICT_KEY_VPL][INNER_DICT_KEY_SERVICE_CT]
			if INNER_DICT_KEY_REMOVE_VPL in sls[SG_DICT_KEY_VPL]:
				sls[SG_DICT_KEY_VPL] = {}
		
		# remove duplicate contents.
		contentidinfo = {}
		idxi = 0
		cnt = len(sgContentArr)
		while idxi < cnt:
			contenticmp = copy.deepcopy(sgContentArr[idxi])
			contentidi = contenticmp[SG_DICT_KEY_ID]
			del contenticmp[SG_DICT_KEY_ID]
			del contenticmp[SG_DICT_KEY_SERVICEREFERENCE]
			
			idxj = idxi + 1
			while idxj < cnt:
				contentjcmp = copy.deepcopy(sgContentArr[idxj])
				contentidj = contentjcmp[SG_DICT_KEY_ID]
				del contentjcmp[SG_DICT_KEY_ID]
				del contentjcmp[SG_DICT_KEY_SERVICEREFERENCE]
				
				# python will do a deep compare and check all the k,vs recursively.
				if contenticmp == contentjcmp:
					contentidinfo[contentidj] = contentidi
					if SG_DICT_KEY_SERVICEREFERENCE in sgContentArr[idxj]:
						sgContentArr[idxi][SG_DICT_KEY_SERVICEREFERENCE] += sgContentArr[idxj][SG_DICT_KEY_SERVICEREFERENCE]
					del sgContentArr[idxj]
					#print contentjcmp, contentidj
					cnt -= 1
					continue
				idxj += 1
			idxi += 1

		# replace duplacated content id to the single one.
		for findid, replaceid in contentidinfo.items():
			#print findid
			for schedule in sgScheduleArr:
				if SG_DICT_KEY_CONTENTREFERENCE in schedule:
					for cr in schedule[SG_DICT_KEY_CONTENTREFERENCE]:
						if cr[SG_DICT_KEY_IDREF] == findid:
							#print 'schedule ',schedule
							cr[SG_DICT_KEY_IDREF] = replaceid
			for sls in slsJsonArr:
				if SG_DICT_KEY_VOD in sls[SG_DICT_KEY_VPL]:
					for vod in sls[SG_DICT_KEY_VPL][SG_DICT_KEY_VOD]:
						if SG_DICT_KEY_SGCONTENTIDREF in vod:
							if vod[SG_DICT_KEY_SGCONTENTIDREF] == findid:
								#print 'vod ',sls
								vod[SG_DICT_KEY_SGCONTENTIDREF] = replaceid
				if SG_DICT_KEY_BFP in sls[SG_DICT_KEY_VPL]:
					for bfp in sls[SG_DICT_KEY_VPL][SG_DICT_KEY_BFP]:
						if SG_DICT_KEY_SGCONTENTIDREF in bfp:
							if bfp[SG_DICT_KEY_SGCONTENTIDREF] == findid:
								#print 'bfp ',sls,findid,replaceid
								#print ''
								bfp[SG_DICT_KEY_SGCONTENTIDREF] = replaceid
		
					
		# process slt inet url sls.
		slsurl = None
		for jsonDict in sltInetUrlArr:
			if jsonDict[SG_DICT_KEY_URLTYPE] == SLTINETURL_TYPE_SG:
				sgServiceStreamUrl = jsonDict[SG_DICT_KEY_URL]
				slsurl = urlparse.urljoin(sgServiceStreamUrl, SLTINETURL_SUFFIX_SLS)
				break

		if slsurl != None:
			isnew = True
			for jsonDict in sltInetUrlArr:
				if jsonDict[SG_DICT_KEY_URLTYPE] == SLTINETURL_TYPE_SLS:
					isnew = False
					jsonDict[SG_DICT_KEY_URL] = slsurl
					break
			if isnew:
				jsonDict = {}
				jsonDict[SG_DICT_KEY_URL] = slsurl
				jsonDict[SG_DICT_KEY_URLTYPE] = SLTINETURL_TYPE_SLS
				sltInetUrlArr.append(jsonDict)
		
		sltJsonDict = {}
		sltJsonDict[SG_DICT_KEY_SERVICE] = sltServiceArr
		sltJsonDict[SG_DICT_KEY_SLTINETURL] = sltInetUrlArr
		
		jsonStr = json.dumps(sltJsonDict, indent=4, separators=(',', ': '), sort_keys=False,
							 ensure_ascii=False).encode(OUTPUT_CODEC)
		if self.output is not None:
			path = self.output + SLT_FILE_NAME
		else:
			path = "./" + SLT_FILE_NAME
		print "output slt file is:", path
		self.__saveFile(jsonStr, path)
		
		jsonStr = json.dumps(slsJsonArr, indent=4, separators=(',', ': '), sort_keys=False,
							 ensure_ascii=False).encode(OUTPUT_CODEC)
		if self.output is not None:
			path = self.output + SLS_FILE_NAME
		else:
			path = "./" + SLS_FILE_NAME
		print "output sls file is:", path
		self.__saveFile(jsonStr, path)
		
		sgJsonDict = {}
		sgJsonDict[SG_DICT_KEY_SERVICE] = sgServiceArr
		sgJsonDict[SG_DICT_KEY_SCHEDULE] = sgScheduleArr
		sgJsonDict[SG_DICT_KEY_CONTENT] = sgContentArr
		
		jsonStr = json.dumps(sgJsonDict, indent=4, separators=(',', ': '), sort_keys=False,
							 ensure_ascii=False).encode(OUTPUT_CODEC)
		if self.output is not None:
			path = self.output + SG_FILE_NAME
		else:
			path = "./" + SG_FILE_NAME
		print "output sg file is:", path
		self.__saveFile(jsonStr, path)

		jsonStr = json.dumps(infoArr, indent=4, separators=(',', ': '), sort_keys=False,
							 ensure_ascii=False).encode(OUTPUT_CODEC)
		if self.output is not None:
			path = self.output + INFO_FILE_NAME
		else:
			path = "./" + INFO_FILE_NAME
		print "output info file is:", path
		self.__saveFile(jsonStr, path)
		
		# save uri list.
		if self.output is not None:
			path = self.output + URI_LIST_FILE_NAME
		else:
			path = "./" + URI_LIST_FILE_NAME
		print "output uri file is:", path

		fp = codecs.open(path, "w", OUTPUT_CODEC)
		fp.writelines([uri + ' ' + path + '\n' for (uri, path) in zip(uriArr, filePathArr)])
		fp.close()

		# save duplicate id list.
		if self.output is not None:
			path = self.output + DUPLICATE_ID_LIST_FILE_NAME
		else:
			path = "./" + DUPLICATE_ID_LIST_FILE_NAME
		print "output duplicate id file is:", path

		jsonStr = json.dumps(contentidinfo, indent=4, separators=(',', ': '), sort_keys=False,
							 ensure_ascii=False).encode(OUTPUT_CODEC)
		fp = codecs.open(path, "w", OUTPUT_CODEC)
		fp.write(jsonStr)
		fp.close()
	
	@staticmethod
	def makeFileNameWithSuffix(filename, suffix):
		if filename == None:
			return None
		
		if suffix == None:
			return filename
		
		fnparts = os.path.splitext(filename)
		return fnparts[0] + suffix + fnparts[1]
	
	@staticmethod
	def addUriInfo(uriarr, filepatharr, uri, path = None):
		if uri == None or uriarr == None or filepatharr == None:
			return
			
		if uri not in uriarr:
			uriarr.append(uri)
			if path == None:
				path = ''
			filepatharr.append(path)
		
	# return tuple: (uri, path)
	@staticmethod
	def resourceUrl2Uri(url):
		if url == None:
			return None
		
		urlarr = url.split(RESOURCE_FOLDER_NAME, 1)

		uri = SG_URI_PREFIX + SG_URI_ICON_ID_PATH_PREFIX + SG_URI_PATH_SEPARATOR
		if len(urlarr) > 1:
			path = urlarr[1]
		else:
			path = url
		return (uri + path, path)
		
	# return appended index, if error return None.
	@staticmethod
	def appendKVArrayInDict(dict, key, val):
		if dict == None or val == None or key == None:
			return None
			
		if key not in dict:
			dict[key] = [val]
			return 0
		dict[key].append(val)
		return len(dict[key]) - 1
		
	
	@staticmethod
	def processResIdReference(destinfo, srcinfo, 
			sgsvcarr, sgscharr, sgconarr, sltsvcarr, slsarr):
		if srcinfo == None or destinfo == None:
			return
		
		sgsch = sgscharr[srcinfo.sgschidx]
		sgsvc = sgsvcarr[srcinfo.sgsvcidx]
		sls = slsarr[srcinfo.slsidx]
		sltsvc = sltsvcarr[srcinfo.sltsvcidx]
		
		destsgsch = sgscharr[destinfo.sgschidx]
		destsgsvc = sgsvcarr[destinfo.sgsvcidx]
		destsls = slsarr[destinfo.slsidx]
		destsltsvc = sltsvcarr[destinfo.sltsvcidx]

		vpl = sls[SG_DICT_KEY_VPL]
		destvpl = destsls[SG_DICT_KEY_VPL]
		
		pwin = None
		schconref = None
		sgcon = None
		
		destschconref = None
		destpwin = None
		destsgcon = None
		destsgconid = None
		
		destpwinarr = None
		
		if destinfo.restype == RES_TYPE_EVENT:
			if SG_DICT_KEY_CONTENTREFERENCE in destsgsch:
				destschconrefarr = destsgsch[SG_DICT_KEY_CONTENTREFERENCE]
				destschconref = destschconrefarr[destinfo.schconrefidx]
				if SG_DICT_KEY_PRESENTATIONWINDOW in destschconref:
					destpwinarr = destschconref[SG_DICT_KEY_PRESENTATIONWINDOW]
					destpwin = destpwinarr[destinfo.pwinidx]
			destsgcon = sgconarr[destinfo.sgconidx]
			destsgconid = destsgcon[SG_DICT_KEY_ID]

			if srcinfo.restype == RES_TYPE_EVENT:
				if SG_DICT_KEY_CONTENTREFERENCE in sgsch:
					schconrefarr = sgsch[SG_DICT_KEY_CONTENTREFERENCE]
					schconref = schconrefarr[srcinfo.schconrefidx]
					if SG_DICT_KEY_PRESENTATIONWINDOW in schconref:
						pwinarr = schconref[SG_DICT_KEY_PRESENTATIONWINDOW]
						pwin = pwinarr[srcinfo.pwinidx]
				sgcon = sgconarr[srcinfo.sgconidx]

				ct = None
				if srcinfo.vplctidx != None:
					ctarr = vpl[SG_DICT_KEY_CT]
					ct = ctarr[srcinfo.vplctidx]
					ctcopy = copy.deepcopy(ct)
					
					destctarr = destvpl[SG_DICT_KEY_CT]
					destct = destctarr[destinfo.vplctidx]
					
					if SG_DICT_KEY_WEIGHT in destct:
						ctcopy[SG_DICT_KEY_WEIGHT] = destct[SG_DICT_KEY_WEIGHT]
					destctarr[destinfo.vplctidx] = ctcopy
					
				uc = None
				if srcinfo.vplucidx != None:
					ucarr = vpl[SG_DICT_KEY_UC]
					uc = ucarr[srcinfo.vplucidx]
					uccopy = copy.deepcopy(uc)
					
					destucarr = destvpl[SG_DICT_KEY_UC]
					destuc = destucarr[destinfo.vplucidx]
					
					if SG_DICT_KEY_WEIGHT in destuc:
						uccopy[SG_DICT_KEY_WEIGHT] = destuc[SG_DICT_KEY_WEIGHT]
					destucarr[destinfo.vplucidx] = uccopy
					
				vod = None
				if srcinfo.vplvodidx != None:
					vodarr = vpl[SG_DICT_KEY_VOD]
					vod = vodarr[srcinfo.vplvodidx]
					vodcopy = copy.deepcopy(vod)
					
					vodcopy[SG_DICT_KEY_SGCONTENTIDREF] = destsgconid
					
					if destinfo.vplvodidx == None:
						EsgGenerator.appendKVArrayInDict(destvpl, SG_DICT_KEY_VOD, vodcopy)
					else:
						destvodarr = destvpl[SG_DICT_KEY_VOD]
						destvod = destvodarr[destinfo.vplvodidx]
						
						# merge dest data.
						isDestEmpty = (len(destvod[SG_DICT_KEY_PLAYURL]) == 1 and destvod[SG_DICT_KEY_PLAYURL][0] == '')
						if not isDestEmpty:
							vodcopy[SG_DICT_KEY_PLAYURL] = destvod[SG_DICT_KEY_PLAYURL]
						
						if SG_DICT_KEY_WEIGHT in destvod:
							vodcopy[SG_DICT_KEY_WEIGHT] = destvod[SG_DICT_KEY_WEIGHT]
						destvodarr[destinfo.vplvodidx] = vodcopy
					
				bfp = None
				if srcinfo.vplbfpidx != None:
					bfparr = vpl[SG_DICT_KEY_BFP]
					bfp = bfparr[srcinfo.vplbfpidx]
					bfpcopy = copy.deepcopy(bfp)
					
					bfpcopy[SG_DICT_KEY_SGCONTENTIDREF] = destsgconid

					if destinfo.vplbfpidx == None:
						EsgGenerator.appendKVArrayInDict(destvpl, SG_DICT_KEY_BFP, bfpcopy)
					else:
						destbfparr = destvpl[SG_DICT_KEY_BFP]
						destbfp = destbfparr[destinfo.vplbfpidx]
						
						# merge dest data.
						isDestEmpty = (len(destbfp[SG_DICT_KEY_PLAYURL]) == 1 and destbfp[SG_DICT_KEY_PLAYURL][0] == '')
						if not isDestEmpty:
							bfpcopy[SG_DICT_KEY_PLAYURL] = destbfp[SG_DICT_KEY_PLAYURL]
						
						if SG_DICT_KEY_WEIGHT in destbfp:
							bfpcopy[SG_DICT_KEY_WEIGHT] = destbfp[SG_DICT_KEY_WEIGHT]
						destbfparr[destinfo.vplbfpidx] = bfpcopy
					
				if pwin != None:
					pwincopy = copy.deepcopy(pwin)
					if destpwin != None:
						pwincopy[SG_DICT_KEY_ID] = destpwin[SG_DICT_KEY_ID]
						if SG_DICT_KEY_STARTTIME in destpwin:
							pwincopy[SG_DICT_KEY_STARTTIME] = destpwin[SG_DICT_KEY_STARTTIME]
						if SG_DICT_KEY_ENDTIME in destpwin:
							pwincopy[SG_DICT_KEY_ENDTIME] = destpwin[SG_DICT_KEY_ENDTIME]
						if SG_DICT_KEY_DURATION in destpwin:
							pwincopy[SG_DICT_KEY_DURATION] = destpwin[SG_DICT_KEY_DURATION]
					elif SG_DICT_KEY_ID in pwincopy:
						#del pwincopy[SG_DICT_KEY_ID]
						#print destschconref,destinfo.pwinidx
						pwincopy[SG_DICT_KEY_ID] = destinfo.pwinid
					
					if destinfo.pwinidx == None:
						#EsgGenerator.appendPresentationWindowInContentReference(destschconref, pwincopy)
						EsgGenerator.appendKVArrayInDict(destschconref, SG_DICT_KEY_PRESENTATIONWINDOW, pwincopy)
					else:
						destpwinarr[destinfo.pwinidx] = pwincopy
				
				sgconcopy = copy.deepcopy(sgcon)
				sgconcopy[SG_DICT_KEY_ID] = destsgconid
				if SG_DICT_KEY_SERVICEREFERENCE in destsgcon:
					sgconcopy[SG_DICT_KEY_SERVICEREFERENCE] = destsgcon[SG_DICT_KEY_SERVICEREFERENCE]
				elif SG_DICT_KEY_SERVICEREFERENCE in sgconcopy:
					del sgconcopy[SG_DICT_KEY_SERVICEREFERENCE]
				
				isDestEmpty = (len(destsgcon[SG_DICT_KEY_NAME]) == 1 and destsgcon[SG_DICT_KEY_NAME][0][SG_DICT_KEY_TEXT] == '')
				if not isDestEmpty:
					sgconcopy[SG_DICT_KEY_NAME] = destsgcon[SG_DICT_KEY_NAME]
				
				if SG_DICT_KEY_DESCRIPTION in destsgcon:
					sgconcopy[SG_DICT_KEY_DESCRIPTION] = destsgcon[SG_DICT_KEY_DESCRIPTION]
				elif SG_DICT_KEY_DESCRIPTION in sgconcopy:
					del sgconcopy[SG_DICT_KEY_DESCRIPTION]
				
				sgconarr[destinfo.sgconidx] = sgconcopy
			else:	# if srcinfo.restype == RES_TYPE_PROGRAM:
				# src is program.
				if INNER_DICT_KEY_SERVICE_CT in vpl:
					ct = vpl[INNER_DICT_KEY_SERVICE_CT]
					ctcopy = copy.deepcopy(ct)
				#if SG_DICT_KEY_CT in vpl:
				#	ctarr = vpl[SG_DICT_KEY_CT]
				#	ct = ctarr[0]
				#	ctcopy = copy.deepcopy(ct)
				else:
					sgsvcid = None
					if SG_DICT_KEY_SGSERVICEIDREF in sls[SG_DICT_KEY_USERSERVICEDESCRIPTION]:
						sgsvcid = sls[SG_DICT_KEY_USERSERVICEDESCRIPTION][SG_DICT_KEY_SGSERVICEIDREF]
					ctcopy = EsgGenerator.makeCtDict(0, 0, '', bw = None, inflatemode = None, 
							playurl = None, starttime = None, endtime = None, 
							sgserviceidref = sgsvcid, weight = None)
				
				if destinfo.vplctidx == None:
					EsgGenerator.appendKVArrayInDict(destvpl, SG_DICT_KEY_CT, ctcopy)
				else:
					destctarr = destvpl[SG_DICT_KEY_CT]
					destct = destctarr[destinfo.vplctidx]
					
					if SG_DICT_KEY_WEIGHT in destct:
						ctcopy[SG_DICT_KEY_WEIGHT] = destct[SG_DICT_KEY_WEIGHT]
					destctarr[destinfo.vplctidx] = ctcopy
				
				# build presentation window.
				if destpwin != None:
					pwincopy = destpwin
				else:
					pwincopy = {}
					
				if SG_DICT_KEY_ID not in pwincopy:
					pwincopy[SG_DICT_KEY_ID] = destinfo.pwinid
				
				if destinfo.pwinidx == None:
					EsgGenerator.appendKVArrayInDict(destschconref, SG_DICT_KEY_PRESENTATIONWINDOW, pwincopy)
				else:
					destpwinarr[destinfo.pwinidx] = pwincopy
				
				# merge service info to content.
				isDestEmpty = (len(destsgcon[SG_DICT_KEY_NAME]) == 1 and destsgcon[SG_DICT_KEY_NAME][0][SG_DICT_KEY_TEXT] == '')
				if SG_DICT_KEY_NAME in sgsvc and isDestEmpty:
					destsgcon[SG_DICT_KEY_NAME] = copy.deepcopy(sgsvc[SG_DICT_KEY_NAME])
					
				isDestEmpty = SG_DICT_KEY_DESCRIPTION not in destsgcon
				if SG_DICT_KEY_DESCRIPTION in sgsvc and isDestEmpty:
					destsgcon[SG_DICT_KEY_DESCRIPTION] = copy.deepcopy(sgsvc[SG_DICT_KEY_DESCRIPTION])
					
				if SG_DICT_KEY_PRIVATEEXT in sgsvc:
					priext = sgsvc[SG_DICT_KEY_PRIVATEEXT]
					if SG_DICT_KEY_SERVICEICON in priext:
						svcico = priext[SG_DICT_KEY_SERVICEICON]
						icocopy = copy.deepcopy(svcico)
						if SG_DICT_KEY_PRIVATEEXT not in destsgcon:
							dicttmp = {SG_DICT_KEY_CONTENTICON:icocopy}
							destsgcon[SG_DICT_KEY_PRIVATEEXT] = dicttmp
						else:
							destsgconpriext = destsgcon[SG_DICT_KEY_PRIVATEEXT]
							if SG_DICT_KEY_CONTENTICON not in destsgconpriext:
								destsgconpriext[SG_DICT_KEY_CONTENTICON] = []
							destsgconpriext[SG_DICT_KEY_CONTENTICON] += icocopy
				
			
	def addReference(self, resid, restype, destinfo):
		self.refList.append((resid, restype, destinfo))
		
	def addRes(self, resid, restype, info):
		self.resTable[resid] = (resid, restype, info)

	def findResInfoInResTable(self, resid):
		tableobj = self.resTable[resid]
		if tableobj == None:
			return None
		return tableobj[2]
		
	@staticmethod
	def isVplProgram(streamtype, opentype, pagetype):
		if streamtype != STREAMTYPE_LIST:
			#return False
			return True
			
		if opentype == OPENTYPE_PLAY_ONLY:
			return True
			
		if pagetype in VPL_PAGETYPE_LIST:
			return True
			
		return False
	
	@staticmethod
	def makeCtDict(ctsid, issid, cturl, \
			bw = None, inflatemode = None, playurl = None, starttime = None, endtime = None, sgserviceidref = None, weight = None):
		ctdict = {}
		ctdict[SG_DICT_KEY_CTSID] = ctsid
		ctdict[SG_DICT_KEY_ISSID] = issid
		ctdict[SG_DICT_KEY_CTURL] = [cturl]
		if bw != None:
			ctdict[SG_DICT_KEY_BW] = bw
		if inflatemode != None:
			ctdict[SG_DICT_KEY_INFLATEMODE] = inflatemode
		if playurl != None and playurl != '':
			ctdict[SG_DICT_KEY_PLAYURL] = [playurl]
		if starttime != None:
			ctdict[SG_DICT_KEY_STARTTIME] = starttime
		if endtime != None:
			ctdict[SG_DICT_KEY_ENDTIME] = endtime
		if sgserviceidref != None and sgserviceidref != '':
			ctdict[SG_DICT_KEY_SGSERVICEIDREF] = sgserviceidref
		if weight != None:
			ctdict[SG_DICT_KEY_WEIGHT] = weight
		return ctdict
		
		
	# is_timestamp: return ntp timestamp.
	@staticmethod
	def format_datatime(str_datetime, is_timestamp):
		#str_datetime = "2017-09-25T12:00:00+08:00"
		#str_datetime = "2017-9-25 12:00:00"
		#str_datetime = "2017-9-25 2:00"
		if str_datetime is not None:
			# check if a lest length datetime string.
			#if len(str_datetime) < 17:
			if len(str_datetime) < 14:
				return None
			
			str_datetime = str_datetime.replace('/', '-')
			
			if str_datetime[4] != '-':
				return None
			
			strdt = str_datetime
			# check if month no 0 padding.
			if str_datetime[6] == '-':
				strdt = str_datetime[:5] + '0' + str_datetime[5:]

			strdtlen = len(str_datetime)
			tzsignidx = strdtlen - 6
			tzsepidx = strdtlen - 3
			if (str_datetime[tzsignidx] == '+' or str_datetime[tzsignidx] == '-') and str_datetime[tzsepidx] == ':':
				strdt = str_datetime[:tzsignidx]

			# check and complete time.
			if strdt.count(':') < 2:
				strdt += ':00'
			
			try:
				ori_dt = datetime.strptime(strdt, '%Y-%m-%dT%H:%M:%S')
			except ValueError, ve:
				try:
					ori_dt = datetime.strptime(strdt, '%Y-%m-%d %H:%M:%S')
				except ValueError, ve:
					#print "The input datatime is invalid: %s" % strdt
					return None

			if is_timestamp:
				utcdt = ori_dt + timedelta(hours=-8)	# convert from bjt to utc
				#print ori_dt,dt,calendar.timegm(ori_dt.timetuple()),calendar.timegm(dt.utctimetuple())
				timestamp = calendar.timegm(utcdt.utctimetuple())
				return EsgGenerator.__unix_to_ntp(timestamp)
				
			new_dt = ori_dt.strftime('%Y-%m-%dT%H:%M:%S')
			return new_dt
		return None
	
	@staticmethod
	def serviceCategory2SltUrlType(category):
		type = None
		if category == SG_SERVICECATEGORY_SG:
			type = SLTINETURL_TYPE_SG
		elif category == SG_SERVICECATEGORY_SPT:
			type = SLTINETURL_TYPE_SPT
		return type
	
	# https://github.com/igors/time2time
	@staticmethod
	def __unix_to_ntp(unixtime):
		ntptime = int(unixtime) + NTP2UNIX
		return ntptime
		
	@staticmethod
	def calculateGlobalFileID(ctsid, issid, fid):
		if ctsid == None or issid == None or fid == None:
			return None
		return ctsid*2**28 + issid*2**20 + fid
	
	def streamTypeToSltType(streamType, pageType):
		type = -1
		if streamType == 1:
			type = 1	# video
		elif streamType == 3:
			type = 2	# audio
		elif streamType == 10:
			if pageType == 10:	# xingyun cd
				type = 6	# BFP
			else:
				type = 3	# PL/App-based
		elif streamType == 6:
			type = 6	# BFP
		elif streamType == 5:
			type = 7	# RT
		elif streamType == 8:
			type = 8	# EMM
		elif streamType == 0 or streamType == 2 or streamType == 4:	# reserved
			type = 0
		# leave slt type 4:SG,5:EAS,9:SPT, stream type 7
	
	@staticmethod
	def __saveFile(jsonStr, savePath):
		fp = open(savePath, "w")
		fp.write(jsonStr)
		fp.close()
	
	@staticmethod
	def __getOneSdt(head, mainRow):
		oneSdt = collections.OrderedDict()
		for k in range(PAT_ITEM_NUM, PAT_ITEM_NUM + SDT_ITEM_NUM):
			oneSdt[head[0]] = int(mainRow[0])  # program number
			if head[k] == "program_number" or head[k] == "free_ca_mode" \
				or head[k] == DATA_TABLE_DICT_KEY_OPEN_TYPE or head[k] == DATA_TABLE_DICT_KEY_PAGE_TYPE or head[k] == "emergency" \
				or head[k] == DATA_TABLE_DICT_KEY_BANDWIDTH:
				if mainRow[k] != "":
					oneSdt[head[k]] = int(mainRow[k])
			elif head[k] == DATA_TABLE_DICT_KEY_SPEECH_SERVICE_NAME or head[k] == DATA_TABLE_DICT_KEY_SPEECH_SERVICE_PROVIDER_NAME:
				if mainRow[k] != "":
					eline = codecs.decode(mainRow[k], INPUT_CODEC)
					#oneSdt[head[k]] = eline.split(SPEECH_ALTERNATIVE_TEXT_SEPRATOR)
					oneSdt[head[k]] = eline
			else:
				oneSdt[head[k]] = codecs.decode(mainRow[k], INPUT_CODEC)
		return oneSdt

	@staticmethod
	def __getOnePat(head, mainRow):
		onePat = collections.OrderedDict()
		for j in range(0, PAT_ITEM_NUM):
			if head[j] == DATA_TABLE_DICT_KEY_STREAM_URL \
				or head[j] == DATA_TABLE_DICT_KEY_SG_SERVICE_ID \
				or head[j] == DATA_TABLE_DICT_KEY_SG_SCHEDULE_ID \
				or head[j] == SG_DICT_KEY_CTURL:
				onePat[head[j]] = codecs.decode(mainRow[j], INPUT_CODEC)
			else:
				if mainRow[j] != "":
					onePat[head[j]] = int(mainRow[j])
		return onePat

	@staticmethod
	def __getEventNum(eitBeginIndex, startTimeLine):
		eitNum = 0
		for tl in range(eitBeginIndex + 2, len(startTimeLine)):
			if startTimeLine[tl] is not None and startTimeLine[tl] != "":
				eitNum += 1
			else:
				break
		return eitNum

	@staticmethod
	def __getEitStartIndex(head):
		eitBeginIndex = PAT_ITEM_NUM + SDT_ITEM_NUM
		for col in range(PAT_ITEM_NUM + SDT_ITEM_NUM, len(head)):
			if head[col] == "eit_event_arr":
				eitBeginIndex = col
				break
		return eitBeginIndex
		
def printHelp():
	print "generate 0.json,info.json,tag.json from esg.csv"
	print "usage:",
	print "python EsgGenerator.py inputCsvFile [-o outputFile -i oldEsg]"
	print "  -o: output dir path,default is: ./"
	print "  -i: the old esg json file path,use this to determine pat,sdt,eit versions,default versions are 0"
	print "  -h: show the help"

def main(argv):
	path = None
	output = None
	oldEsg = None
	if len(argv) < 2:
		printHelp()
		return
	else:
		path = argv[1]
		parNum = 0
		showHelp = False
		for arg in argv:
			parNum += 1
			if arg == "-o":
				if len(argv) < parNum + 1:
					print "-o must follow with output file"
					return
				output = argv[parNum]
			elif arg == "-i":
				if len(argv) < parNum + 1:
					print "-o must follow with an old esg json file"
					return
				oldEsg = argv[parNum]
			elif arg == "-h":
				showHelp = True
		if showHelp:
			printHelp()
			return
	versions = None
	esgGenerator = EsgGenerator(path, output, versions)
	esgGenerator.generateAll()


if __name__ == "__main__":
	main(sys.argv)
