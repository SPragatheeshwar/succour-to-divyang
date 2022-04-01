import cv2
import pyttsx3

def speak(output):
    engine = pyttsx3.init()
    sound = engine.getProperty('voices')
    engine.setProperty('voice', sound[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 130)
    engine.say(output)
    engine.runAndWait()
def reco():
    thres = 0.65  # Threshold to detect object

    check = []
    cap = cv2.VideoCapture('D:\pragatheeshwar\Smart India Hack\VID20220308103414.mp4')
    cap.set(3, 1280)
    cap.set(4, 720)
    cap.set(10, 70)
    classNames = []
    classFile = 'coco.names.txt'
    distance = []
    distance_file = 'D:\pragatheeshwar\Smart India Hack\others\distance'
    danger = []
    danger_file = 'D:\pragatheeshwar\Smart India Hack\others\danger'

    with open(danger_file, 'rt') as f:
        danger = f.read().rstrip('\n').split('\n')

    with open(distance_file,'rt') as f:
        distance = f.read().rstrip('\n').split('\n')

    with open(classFile,'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

        configPath = 'D:\pragatheeshwar\Smart India Hack\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt.txt'
        weightsPath = 'D:\\pragatheeshwar\\Smart India Hack\\frozen_inference_graph.pb'

        net = cv2.dnn_DetectionModel(weightsPath, configPath)
        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        count = 0

        while True:
            success, img = cap.read()
            classIds, confs, bbox = net.detect(img, confThreshold=thres)
            #print(classIds, bbox)

            if len(classIds) != 0:
                for classId, confidence, box,i in zip(classIds.flatten(), confs.flatten(), bbox,bbox):
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    #cv2.putText(img, str(i), (box[0] + 10, box[1] + 30),
                                #cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    check.append(classIds[0])


                    start_point = (14000,0)
                    end_point = (0,250)
                    color = (0, 255, 0)
                    thickness = 2
                    cv2.line(img,start_point,end_point,color,thickness)

                if str(classNames[classIds[0]-1]) in danger:
                    speak("Danger ahead be careful")
                    count+=1
                    if count > 3:
                        break
                    else:
                        continue
                if check.count(classIds[0]) <= 2:
                    speak(str(classNames[classIds[0] - 1])+" detected in '{}' meters".format(str(distance[classIds[0]-1])))
            #cv2.putText(img,str(fps),(50,50),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Output", img)
            cv2.waitKey(1)
reco()