import cv2
import numpy as np
import util as ut
import signal
import sys
import ssl
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser
import base64
# import ASL as asl
import svm_train as st

STABILIZATION_QTY=20
NUM_SAMPLES=15
FORMAT='JPG'

model,word_map=st.trainSVM(NUM_SAMPLES,FORMAT)


class SimpleEcho(WebSocket):

    count = 0
    temp=0
    previouslabel=None
    previousText=" "
    label = None

    def process(self,img):
    # _,img=cap.read()
        cv2.rectangle(img,(900,100),(1300,500),(255,0,0),3) # bounding box which captures ASL sign to be detected by the system
        img1=img[100:500,900:1300]
        img_ycrcb = cv2.cvtColor(img1, cv2.COLOR_BGR2YCR_CB)
        blur = cv2.GaussianBlur(img_ycrcb,(11,11),0)
        skin_ycrcb_min = np.array((0, 138, 67))
        skin_ycrcb_max = np.array((255, 173, 133))
        mask = cv2.inRange(blur, skin_ycrcb_min, skin_ycrcb_max)  # detecting the hand in the bounding box using skin detection
        contours,hierarchy = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL, 2)
        cnt=ut.getMaxContour(contours,4000)                       # using contours to capture the skin filtered image of the hand
        if cnt!=None:
            gesture,label=ut.getGestureImg(cnt,img1,mask,model,word_map,FORMAT)   # passing the trained model for prediction and fetching the result
            if(label!=None):
                if(self.temp==0):
                    previouslabel=label
                if previouslabel == label:
                    previouslabel=label
                    self.temp+=1
                else :
                    temp=0
                if(temp==STABILIZATION_QTY):
                    # if(label=='P'):

                    #     label=" "
                    # text= text + label
                    # if(label=='Q'):
                        # words = re.split(" +",text)
                        # words.pop()
                        # text = " ".join(words)
                        #text=previousText
            # cv2.imshow('PredictedGesture',gesture)                # showing the best match or prediction
            # cv2.putText(img,label,(50,150), font,8,(0,125,155),2)  # displaying the predicted letter on the main screen
            # cv2.putText(img,text,(50,450), font,3,(0,0,255),2)
                    print label
                    self.sendMessage(label)



    def handleMessage(self):
    #    self.sendMessage(self.data)print self.data
    #    self.count += 1
        print 'Handling message....'
        imgdata = base64.b64decode(self.data)
        self.process(imgdata)

    #    filename = 'some_image' + str(self.count) + '.jpg'
    #    with open(filename, 'wb') as f:
    #        f.write(imgdata)

    def handleConnected(self):
       print self.address[0] + " connected!"
       # self.sendMessage('Hello')

       self.sendMessage(recognizedPhrase)

    def handleClose(self):
      pass

clients = []
class SimpleChat(WebSocket):

   def handleMessage(self):
      for client in clients:
         if client != self:
            client.sendMessage(self.address[0] + u' - ' + self.data)

   def handleConnected(self):
      print (self.address, 'connected')
      for client in clients:
         client.sendMessage(self.address[0] + u' - connected')
      clients.append(self)

   def handleClose(self):
      clients.remove(self)
      print (self.address, 'closed')
      for client in clients:
         client.sendMessage(self.address[0] + u' - disconnected')


if __name__ == "__main__":

    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
    parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
    parser.add_option("--example", default='echo', type='string', action="store", dest="example", help="echo, chat")
    parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
    parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
    parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")
    (options, args) = parser.parse_args()

    cls = SimpleEcho
    if options.example == 'chat':
      cls = SimpleChat

    if options.ssl == 1:
      server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
    else:
      server = SimpleWebSocketServer(options.host, options.port, cls)

    def close_sig_handler(signal, frame):
      server.close()
      sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)
    print 'Starting server...'
    server.serveforever()
