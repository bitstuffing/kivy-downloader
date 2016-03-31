#-*- coding: utf-8 -*-

import threading, os, subprocess

import urllib,urllib2
import time
import socket
import traceback # for download problems

from core import logger
from core.decoder import Decoder

from kivy.app import App

# Download in background
class DownloadThread(threading.Thread):

    def __init__(self,link,folder,screen,progressDialog,progressDialogLabel):
        logger.debug("init download thread...")
        self.url = link
        self.screen = screen
        self.folder = folder
        self.running = False
        self.aborted = False
        self.progressDialog = progressDialog
        self.progressDialogLabel = progressDialogLabel

        threading.Thread.__init__(self)

    def run(self):
        logger.debug("DownloadThread.run")

        self.running = True

        app = App.get_running_app()

        self.progressDialog.value = 0
        self.progressDialogLabel.text = "decoding link: "+self.url

        decoded_link = Decoder.decodeLink(self.url)

        #copy to clipboard
        app.copy(decoded_link)

        if decoded_link!='' and decoded_link.find("http")>-1:
            app.message("Info","Link has been decoded (from "+self.url+"):\n"+decoded_link+" has been decoded and copied to clipboard.\nDownload should be started/resumed.")
            app.download_screen.ids.label_text_message.text=decoded_link
        elif self.aborted:
            app.message("Error","File "+app.target_file+" has not been downloaded, please try again and make sure remote url exists.")

        separationChar = '/'
        fileName = ''
        if self.url.find("/")>-1:
            fileName = self.url[self.url.rfind("/")+1:]
            if fileName.find(".")==-1 and decoded_link.find("/"):
                fileName = decoded_link[decoded_link.rfind("/")+1:]

        self.downloadfile(decoded_link,self.folder+separationChar+fileName,[],False,True,self.progressDialog,self.progressDialogLabel)

        self.running = False
        app.download_screen.ids.loading.opacity=0

        if self.aborted:
            app.message("Info","Download proccess has been stopped for file: \n "+app.target_file)

    def abort(self):
        logger.debug("DownloadThread.abort")

        if self.running:
            self.aborted = True
            self.p.kill()

    def sec_to_hms(self,seconds):
        m,s = divmod(int(seconds), 60)
        h,m = divmod(m, 60)
        return ("%02d:%02d:%02d" % (h, m, s))

    def downloadfile(self,url,fileName,headers=[],silent=False,notStop=False,progressDialog=None,progressDialoglabel=None):
        logger.debug("Download thread -> downloadfile: url="+url)
        logger.debug("Download thread -> downloadfile: fileName="+fileName)

        try:

            try:
                fileName = fileName.encode("utf-8")
            except:
                pass
            logger.debug("using download file: "+fileName)

            if os.path.exists(fileName) and notStop:
                f = open(fileName, 'r+b')
                existSize = os.path.getsize(fileName)

                logger.info("[downloadtools.py] downloadfile: file exists, size=%d" % existSize)
                recordedSize = existSize
                f.seek(existSize)

            elif os.path.exists(fileName) and not notStop:
                logger.info("[downloadtools.py] downloadfile: file exists, dont re-download")
                return

            else:
                existSize = 0
                logger.info("[downloadtools.py] downloadfile: file doesn't exists")

                f = open(fileName, 'wb')
                recordedSize = 0

            if not silent:
                progressDialog.value=10
            else:
                progressDialog.value=1000

            socket.setdefaulttimeout(30) #Timeout

            h=urllib2.HTTPHandler(debuglevel=0)
            remoteFile = url
            params = None
            '''
            if remoteFile.find("?"):
                remoteFile = url[:url.find("?")]
            request = urllib2.Request(remoteFile, params, headers)
            logger.info("request created to "+url)
            '''
            request = urllib2.Request(url)
            logger.info("checking headers...")
            logger.info("type: "+str(type(headers)))
            if len(headers)>0:
                logger.info("adding headers...")
                for key in headers.keys():
                    logger.info("[downloadtools.py] Header="+key+": "+headers.get(key))
                    request.add_header(key,headers.get(key))
            else:
                logger.info("headers are 0")

            logger.info("checking resume...")
            if existSize > 0: #restart
                logger.info("resume is detected")
                request.add_header('Range', 'bytes=%d-' % (existSize, ))

            opener = urllib2.build_opener(h)
            urllib2.install_opener(opener)
            try:
                logger.info("opening request...")
                connection = opener.open(request)
            except: # End
                logger.error("something fatal happened")
                logger.error("ERROR: "+traceback.format_exc())
                f.close()
                if not silent:
                    progressDialog.close()
            logger.info("detecting download size...")

            try:
                totalFileSize = int(connection.headers["Content-Length"])
            except:
                totalFileSize = 1

            logger.info("total file size: "+str(totalFileSize))

            if existSize > 0:
                totalFileSize = totalFileSize + existSize

            logger.info("Content-Length=%s" % totalFileSize)

            blockSize = 100*1024 #Buffer size

            bufferReadedSize = connection.read(blockSize)
            logger.info("Starting download, readed=%s" % len(bufferReadedSize))

            maxRetries = 5

            while len(bufferReadedSize)>0 and self.aborted==False:
                try:
                    f.write(bufferReadedSize)
                    recordedSize = recordedSize + len(bufferReadedSize)
                    percent = int(float(recordedSize)*100/float(totalFileSize))
                    totalMB = float(float(totalFileSize)/(1024*1024))
                    downloadedMB = float(float(recordedSize)/(1024*1024))

                    retries = 0
                    while retries <= maxRetries:
                        try:
                            before = time.time()
                            bufferReadedSize = connection.read(blockSize)
                            after = time.time()
                            if (after - before) > 0:
                                speed=len(bufferReadedSize)/((after - before))
                                remainingSize=totalFileSize-recordedSize
                                if speed>0:
                                    remainingTime=remainingSize/speed
                                else:
                                    remainingTime=0 #infinite

                                if not silent:
                                    progressDialoglabel.text = "%.2fMB/%.2fMB (%d%%) %.2f Kb/s %s remaining " % ( downloadedMB , totalMB , percent , speed/1024 , self.sec_to_hms(remainingTime)) #respect syntax in translations
                                    progressDialog.value= (percent*10)
                            break
                        except:
                            retries = retries + 1
                            logger.info("ERROR downloading buffer, retry %d" % retries)
                            logger.error( traceback.print_exc() )

                    # if the user stops download proccess...
                    try:
                        if progressDialog.iscanceled():
                            logger.info("Download was canceled by user action")
                            f.close()
                            progressDialog.close()
                            return -1
                    except:
                        pass

                    # Something wrong happened
                    if retries > maxRetries:
                        logger.info("ERROR, something happened in download proccess")
                        f.close()
                        if not silent:
                            progressDialog.close()

                        return -2

                except:
                    logger.error( traceback.print_exc() )

                    f.close()
                    if not silent:
                        progressDialog.close()

                    return -2

        except:
            pass

        try:
            f.close()
        except:
            pass

        if not silent:
            try:
                progressDialog.text = "Finished"
            except:
                pass

        logger.info("Finished download proccess")