# -*- coding: utf-8 -*-
import collections
import json
import sys
import csv
import codecs
import time

HEAD_ROW_NUM = 2
PROTOCOL_VERSION = 6

# version根据旧的esg自动升级，0-9999回滚
MAX_VERSION = 10000
PAT_DEFAULT_VERSION = 0
SDT_DEFAULT_VERSION = 0
EIT_DEFAULT_VERSION = 0

PAT_ITEM_NUM = 6
SDT_ITEM_NUM = 9

# INPUT_CODEC = "gb2312"
INPUT_CODEC = "gb2312"
OUTPUT_CODEC = "utf8"

DICT_KEY_REFERENCE_ID_INNER = '_refid'
DICT_KEY_RES_ID = 'res_id'
SPEECH_ALTERNATIVE_TEXT_SEPRATOR = ','

PAGE_TYPE_CATEGORY_MAINPAGE = 2
PAGE_TYPE_GROUPCHANNEL_MAINPAGE = 3


class EsgGenerator(object):
    """generate json of  esg,scene,and push stream info from csv"""

    def __init__(self, path, output, versions):
        self.path = path
        self.output = output
        self.versions = versions
        reader = csv.reader(open(self.path))
        self.csvItem = [row for row in reader]
        # for row in self.csvItem:
        #     print row

    def generateAll(self):
        self.generateEsg(self.csvItem)
        self.generateInfo(self.csvItem)
        self.generateTagInfo(self.csvItem)

    def generateEsg(self, csvItem):
        """gengerate 0.json from csvItem,0.json is used to send to the satellite as esg"""
        jsonMap = collections.OrderedDict()
        jsonMap["protocol_version"] = PROTOCOL_VERSION
        jsonMap["timestamp"] = (int)(time.time())

        pat = collections.OrderedDict()
        pat_version = PAT_DEFAULT_VERSION
        if self.versions is not None:
            pat_version = (self.versions[0] + 1) % MAX_VERSION
        pat["version_number"] = pat_version
        pat["pat_arr"] = []
        pat_arr = pat["pat_arr"]

        sdt = collections.OrderedDict()
        sdt_version = SDT_DEFAULT_VERSION
        if self.versions is not None:
            sdt_version = (self.versions[1] + 1) % MAX_VERSION
        sdt["version_number"] = sdt_version
        sdt["sdt_arr"] = []
        sdt_arr = sdt["sdt_arr"]

        resIdMax = -1
        arrange = {}
        eit_arr = []
        allLen = len(csvItem) - HEAD_ROW_NUM
        head = csvItem[HEAD_ROW_NUM - 1]
        handledNum = 0
        while handledNum < allLen:
            nextServiceIndex = HEAD_ROW_NUM + handledNum
            mainRow = csvItem[nextServiceIndex]
            handledNum += 1
            # pat
            onePat = self.__getOnePat(head, mainRow)
            pat_arr.append(onePat)
            # sdt
            oneSdt = self.__getOneSdt(head, mainRow)
            sdt_arr.append(oneSdt)

            # arrange
            if DICT_KEY_RES_ID in onePat and 'page_type' in oneSdt:
                resid = onePat[DICT_KEY_RES_ID]
                if oneSdt['page_type'] == PAGE_TYPE_CATEGORY_MAINPAGE:
                    arrange['category_mainpage'] = resid
                if oneSdt['page_type'] == PAGE_TYPE_GROUPCHANNEL_MAINPAGE:
                    arrange['groupchannel_mainpage'] = resid

                if resid > resIdMax:
                    resIdMax = resid

            # eit
            oneEit = collections.OrderedDict()
            oneEit[head[0]] = int(mainRow[0])  # program_number
            eitVersion = EIT_DEFAULT_VERSION
            if self.versions is not None and self.versions[2].has_key(mainRow[0]):
                eitVersion = (self.versions[2][mainRow[0]] + 1) % MAX_VERSION
            oneEit["version_number"] = eitVersion
            eit_event_arr = []
            oneEit["eit_event_arr"] = eit_event_arr

            # found all event
            eitBeginIndex = self.__getEitStartIndex(head)
            # use start_time to determine event num
            startTimeLine = csvItem[nextServiceIndex + 1]
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

            # print "program num:%s,eit num is:%d,eit item num is:%d" % (mainRow[0], eventNum, eventItemNum)
            for h in range(0, eventNum):
                # one event in eit+
                oneEitEvent = collections.OrderedDict()
                oneEitEvent[mainRow[eitBeginIndex]] = int(mainRow[eitBeginIndex + 2 + h])  # eitId
                eit_event_arr.append(oneEitEvent)
                movie = {}
                for m in range(1, eventItemNum + 1):
                    eitLine = csvItem[nextServiceIndex + m]
                    try:
                        if eitLine[eitBeginIndex] == "event_id" or eitLine[eitBeginIndex] == "duration" \
                                or eitLine[eitBeginIndex] == "running_status" or eitLine[
                            eitBeginIndex] == "content_nibble_level_1" \
                                or eitLine[eitBeginIndex] == "content_nibble_level_2" \
                                or eitLine[eitBeginIndex] == "type":
                            if eitLine[eitBeginIndex + 2 + h] is not None and eitLine[eitBeginIndex + 2 + h] != "":
                                oneEitEvent[eitLine[eitBeginIndex]] = int(eitLine[eitBeginIndex + 2 + h])
                        elif eitLine[eitBeginIndex] == "rating":
                            if eitLine[eitBeginIndex + 2 + h] is not None and eitLine[eitBeginIndex + 2 + h] != "":
                                movie[eitLine[eitBeginIndex]] = float(eitLine[eitBeginIndex + 2 + h])
                        elif eitLine[eitBeginIndex] == "year":
                            if eitLine[eitBeginIndex + 2 + h] is not None and eitLine[eitBeginIndex + 2 + h] != "":
                                movie[eitLine[eitBeginIndex]] = int(eitLine[eitBeginIndex + 2 + h])
                        elif eitLine[eitBeginIndex] == "director" or eitLine[eitBeginIndex] == "starring" \
                                or eitLine[eitBeginIndex] == "raptor":
                            if eitLine[eitBeginIndex + 2 + h] is not None and eitLine[eitBeginIndex + 2 + h] != "":
                                movie[eitLine[eitBeginIndex]] = codecs.decode(eitLine[eitBeginIndex + 2 + h],
                                                                              INPUT_CODEC)
                        elif eitLine[eitBeginIndex] == "tag" or eitLine[eitBeginIndex] == "" \
                                or eitLine[eitBeginIndex] is None:
                            continue
                        elif eitLine[eitBeginIndex] == DICT_KEY_RES_ID:
                            resid = eitLine[eitBeginIndex + 2 + h]
                            if resid is not None and resid != "":
                                isRef = (resid[0].lower() == 'r')
                                if isRef:
                                    resid = resid[1:]
                                    oneEitEvent[DICT_KEY_REFERENCE_ID_INNER] = int(resid)
                                else:
                                    iresid = int(resid)
                                    oneEitEvent[eitLine[eitBeginIndex]] = iresid
                                    if iresid > resIdMax:
                                        resIdMax = iresid
                        elif eitLine[eitBeginIndex] == "speech_event_name":
                            if eitLine[eitBeginIndex + 2 + h] is not None and eitLine[eitBeginIndex + 2 + h] != "":
                                eline = codecs.decode(eitLine[eitBeginIndex + 2 + h], INPUT_CODEC)
                                oneEitEvent[eitLine[eitBeginIndex]] = eline.split(SPEECH_ALTERNATIVE_TEXT_SEPRATOR)
                        else:
                            oneEitEvent[eitLine[eitBeginIndex]] = codecs.decode(eitLine[eitBeginIndex + 2 + h],
                                                                                INPUT_CODEC)
                    except Exception, e:
                        print >> sys.stderr, "eit has exception:", eitLine
                        raise e
                if len(movie.keys()) != 0:
                    oneEitEvent["movie"] = movie
            # eit of one program
            eit_arr.append(oneEit)

        eventReferenceTable = []
        # find event's reference object which have reference res id.
        for eaidx in range(0, len(eit_arr)):
            oneEit = eit_arr[eaidx]
            eit_event_arr = oneEit["eit_event_arr"]
            for idx in range(0, len(eit_event_arr)):
                event = eit_event_arr[idx]
                if DICT_KEY_REFERENCE_ID_INNER in event:
                    refid = event[DICT_KEY_REFERENCE_ID_INNER]
                    obj = EsgGenerator.findObjectByResID(refid, pat_arr, sdt_arr, eit_arr)
                    # print refid,obj,sdt_arr
                    if obj != None:
                        eventReferenceTable.append((eaidx, idx, obj))

        # replace reference found.
        for eventRef in eventReferenceTable:
            eaidx = eventRef[0]
            idx = eventRef[1]
            obj = eventRef[2]

            oneEit = eit_arr[eaidx]
            eit_event_arr = oneEit["eit_event_arr"]
            event = eit_event_arr[idx]

            if len(obj) == 1:
                # if an event matches.
                evt = obj[0].copy()
                evt['event_id'] = event['event_id']
                eit_event_arr[idx] = evt
            else:
                # if a program matches.
                patobj = obj[0]
                sdtobj = obj[1]

                if 'service_name' in sdtobj:
                    event['event_name'] = sdtobj['service_name']
                if 'service_provider_name' in sdtobj:
                    event['text'] = sdtobj['service_provider_name']
                if 'icon_url' in sdtobj:
                    event['icon_url'] = sdtobj['icon_url']

                if 'stream_url' in patobj:
                    event['stream_url'] = patobj['stream_url']
                if DICT_KEY_RES_ID in patobj:
                    event[DICT_KEY_RES_ID] = patobj[DICT_KEY_RES_ID]

                if DICT_KEY_REFERENCE_ID_INNER in event:
                    del event[DICT_KEY_REFERENCE_ID_INNER]

        print "Maximum res id: " + str(resIdMax)

        jsonMap["pat"] = pat
        jsonMap["sdt"] = sdt
        jsonMap["eit_arr"] = eit_arr
        jsonMap["arrange"] = arrange
        if not self.__checkEsg(jsonMap):
            return
        # for eit in eit_arr:
        #     for key in eit:
        #         test = eit["eit_event_arr"]
        #         print test
        #         for event in test:
        #             print event
        #             for eventId in event:
        #                 print "id is:",eventId
        #                 print event[eventId]
        #                 try:
        #                     jsonStr = json.dumps(event[eventId], indent=4, separators=(',', ': '), sort_keys=False, ensure_ascii=False) \
        #                     .encode(OUTPUT_CODEC)
        #                 except Exception, e:
        #                     print Exception, ":", e
        #                     raise e
        jsonStr = json.dumps(jsonMap, indent=4, separators=(',', ': '), sort_keys=False,
                             ensure_ascii=False).encode(OUTPUT_CODEC)
        # print jsonStr
        if self.output is not None:
            path = self.output + "0.json"
        else:
            path = "./0.json"
        print "output file is:", path
        self.__saveFile(jsonStr, path)

    def generateInfo(self, csvItem):
        """generate info.json from csv,info.json is used by the swServer to push stream"""
        jsonMap = {}
        allLen = len(csvItem) - HEAD_ROW_NUM
        head = csvItem[HEAD_ROW_NUM - 1]
        handledNum = 0
        stream_pid = None
        stream_output_url = None
        program_number = None
        handledNum = 0
        bandwidth = 0
        while handledNum < allLen:
            oneService = collections.OrderedDict()
            nextServiceIndex = HEAD_ROW_NUM + handledNum
            mainRow = csvItem[nextServiceIndex]
            handledNum += 1
            if mainRow[0] is None or mainRow[0] == "":
                # handledNum += 1
                continue
            for i in range(0, len(head)):
                if head[i] == "stream_pid":
                    stream_pid = int(mainRow[i])
                elif head[i] == "segmenter_url":
                    stream_output_url = codecs.decode(mainRow[i], INPUT_CODEC)
                elif head[i] == "program_number":
                    program_number = codecs.decode(mainRow[i], INPUT_CODEC)
                elif head[i] == "bandwidth":
                    if mainRow[i] == "":
                        bandwidth = 0
                    else:
                        bandwidth = int(mainRow[i])
            oneService["stream_pid"] = stream_pid
            oneService["stream_output_url"] = stream_output_url
            oneService["bandwidth"] = bandwidth
            jsonMap[program_number] = oneService
        jsonStr = json.dumps(jsonMap, indent=4, separators=(',', ': '), sort_keys=False, ensure_ascii=False) \
            .encode(OUTPUT_CODEC)
        # print jsonStr
        if self.output is not None:
            path = self.output + "info.json"
        else:
            path = "./info.json"
        print "output file is:", path
        self.__saveFile(jsonStr, path)

    def generateTagInfo(self, csvItem):
        """ generate tag.json from csvItem,tag.json is used by the swServer to update scene database"""
        jsonMap = []
        allLen = len(csvItem) - HEAD_ROW_NUM
        head = csvItem[HEAD_ROW_NUM - 1]
        handledNum = 0
        while handledNum < allLen:
            nextServiceIndex = HEAD_ROW_NUM + handledNum
            mainRow = csvItem[nextServiceIndex]
            handledNum += 1
            program_number = None
            for i in range(0, len(head)):
                if head[i] == "program_number":
                    program_number = int(mainRow[i])
                    break
            # begin to find eit
            eitBeginIndex = self.__getEitStartIndex(head)
            startTimeLine = csvItem[nextServiceIndex + 1]
            eventNum = self.__getEventNum(eitBeginIndex, startTimeLine)
            eventItemNum = 1
            nextLine = csvItem[HEAD_ROW_NUM + handledNum]
            while nextLine[0] is None or nextLine[0] == "":
                handledNum += 1
                eventItemNum += 1
                if handledNum >= allLen:
                    break
                nextLine = csvItem[HEAD_ROW_NUM + handledNum]
            # print "eit num is:eit item num is:", (eitNum, eitItemNum)
            for h in range(0, eventNum):
                oneItem = collections.OrderedDict()
                oneItem["program_number"] = program_number
                for m in range(0, eventItemNum):
                    eitLine = csvItem[nextServiceIndex + m]
                    try:
                        if eitLine[eitBeginIndex] == "event_id":
                            oneItem["event_id"] = int(eitLine[eitBeginIndex + 2 + h])
                        elif eitLine[eitBeginIndex] == "tag":
                            oneItem["tags"] = []
                            if eitLine[eitBeginIndex + 2 + h] != "":
                                tags = eitLine[eitBeginIndex + 2 + h].split("/")
                                for tag in tags:
                                    oneItem["tags"].append(int(tag))
                    except Exception, e:
                        print "exception:%s" % e,
                        print eitLine
                        continue;
                jsonMap.append(oneItem)
        jsonStr = json.dumps(jsonMap, indent=4, separators=(',', ': '), sort_keys=False, ensure_ascii=False) \
            .encode(OUTPUT_CODEC)
        # print jsonStr
        if self.output is not None:
            path = self.output + "tag.json"
        else:
            path = "./tag.json"
        print "output file is:", path
        self.__saveFile(jsonStr, path)

    @staticmethod
    def findObjectFromArrayByProgramNumber(programNumber, arr):
        if arr != None:
            for dict in arr:
                if "program_number" in dict:
                    if dict["program_number"] == programNumber:
                        return dict

        return None

    @staticmethod
    def findObjectByResID(resid, pat_arr, sdt_arr, eit_arr):
        if pat_arr != None:
            for pat in pat_arr:
                if DICT_KEY_RES_ID in pat:
                    if pat[DICT_KEY_RES_ID] == resid:
                        programNum = pat["program_number"]
                        sdt = EsgGenerator.findObjectFromArrayByProgramNumber(programNum, sdt_arr)
                        return (pat, sdt)

        if eit_arr != None:
            for eit in eit_arr:
                if 'eit_event_arr' in eit:
                    eit_event_arr = eit['eit_event_arr']
                    for event in eit_event_arr:
                        if DICT_KEY_RES_ID in event:
                            if event[DICT_KEY_RES_ID] == resid:
                                return (event,)

        return None

    @staticmethod
    def __getOneSdt(head, mainRow):
        oneSdt = collections.OrderedDict()
        for k in range(PAT_ITEM_NUM, PAT_ITEM_NUM + SDT_ITEM_NUM):
            oneSdt[head[0]] = int(mainRow[0])  # program number
            if head[k] == "program_number" or head[k] == "free_ca_mode" \
                    or head[k] == "open_type" or head[k] == "page_type" or head[k] == "emergency":
                if mainRow[k] != "":
                    oneSdt[head[k]] = int(mainRow[k])
            elif head[k] == "speech_service_name" or head[k] == "speech_service_provider_name":
                if mainRow[k] != "":
                    eline = codecs.decode(mainRow[k], INPUT_CODEC)
                    oneSdt[head[k]] = eline.split(SPEECH_ALTERNATIVE_TEXT_SEPRATOR)
            else:
                oneSdt[head[k]] = codecs.decode(mainRow[k], INPUT_CODEC)
                # print  oneSdt[head[k]]
        return oneSdt

    @staticmethod
    def __getOnePat(head, mainRow):
        onePat = collections.OrderedDict()
        for j in range(0, PAT_ITEM_NUM):
            if head[j] == "stream_url":
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

    @staticmethod
    def __saveFile(jsonStr, savePath):
        fp = open(savePath, "w")
        fp.write(jsonStr)
        fp.close()

    def __checkEsg(self, jsonMap):
        ret = True
        pat_arr = jsonMap["pat"]["pat_arr"]
        for pat in pat_arr:
            if pat["program_number"] is None or pat["stream_pid"] is None or pat["stream_type"] is None \
                    or pat["inflate_mode"] is None or DICT_KEY_RES_ID not in pat:
                print >> sys.stderr, "pat program_number or stream_pid  or stream_type or inflate_mode or " + DICT_KEY_RES_ID + " empty"
                ret = False
            if pat["stream_url"] is None or (pat["stream_url"] == "" and pat["stream_type"] <= 4):
                print >> sys.stderr, "pat  stream_url is empty for program:%d" % pat["program_number"]
                ret = False
        sdt_arr = jsonMap["sdt"]["sdt_arr"]
        for sdt in sdt_arr:
            if sdt["program_number"] is None:
                print >> sys.stderr, "sdt program_number empty "
                ret = False
            if sdt["service_provider_name"] is None or (sdt["service_provider_name"] == ""):
                print >> sys.stderr, "sdt  service_provider_name is empty for program_number:%d" % sdt["program_number"]
                ret = False
            if sdt["service_name"] is None or (sdt["service_name"] == ""):
                print >> sys.stderr, "sdt  service_name is empty for program:%d" % sdt["program_number"]
                ret = False
        eit_arr = jsonMap["eit_arr"]
        for eit in eit_arr:
            if eit["program_number"] is None or eit["version_number"] is None:
                print >> sys.stderr, "eit is invalid for program number:%d" % eit["program_number"]
                ret = False
            if eit["eit_event_arr"] is None or len(eit["eit_event_arr"]) == 0:
                print >> sys.stderr, "eit is invalid for program number:%d" % eit["program_number"]
                ret = False
            for event in eit["eit_event_arr"]:
                if event["event_id"] is None or event["duration"] is None or DICT_KEY_RES_ID not in event:
                    print >> sys.stderr, "eit event event_id  or duration or " + DICT_KEY_RES_ID + " is empty for  program:%d" % \
                                                                                                   eit[
                                                                                                       "program_number"]
                    ret = False
                if event["start_time"] is None or event["start_time"] == "":
                    print >> sys.stderr, "eit event start_time is empty for  program:%d event is:%d" \
                                         % (eit["program_number"], event["event_id"])
                    ret = False
                if event["event_name"] is None or event["event_name"] == "":
                    print >> sys.stderr, "eit event event_name is empty  for  program:%d event is:%d" \
                                         % (eit["program_number"], event["event_id"])
                    ret = False
                if event["text"] is None or event["text"] == "":
                    print >> sys.stderr, "eit event text is empty for  program:%d event is:%d" \
                                         % (eit["program_number"], event["event_id"])
                    ret = False
        return True


class EsgParser:
    """ this class is used for pase a esg json file"""

    def open(self, esgjson):
        fd = open(esgjson)
        strEsg = fd.read()
        self.esg = json.loads(strEsg, encoding="utf-8")
        fd.close()

    def getVersion(self):
        eitVersion = {}
        if self.esg["eit_arr"] is None:
            pass
        else:
            for eit in self.esg["eit_arr"]:
                eitVersion[str(eit["program_number"])] = eit["version_number"]
        return self.esg["pat"]["version_number"], self.esg["sdt"]["version_number"], eitVersion


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
        # return
        path = "./../gvmedia_esg_lab_1483.csv"
        # oldEsg = "./../0.json"
        output = "./../"
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
    try:
        if oldEsg is not None:
            esgParser = EsgParser()
            esgParser.open(oldEsg)
            versions = esgParser.getVersion()
            print versions
    except Exception, e:
        print >> sys.stderr, Exception, ":", e
    esgGenerator = EsgGenerator(path, output, versions)
    esgGenerator.generateAll()


if __name__ == "__main__":
    main(sys.argv)
