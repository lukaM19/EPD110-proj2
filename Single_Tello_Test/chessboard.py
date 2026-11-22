import cv2
import numpy as np

## DRAWS ALL CORNERS FOUND ON THE FRAME

def draw_points(corners, image) :
    for i in range(0,corners.shape[0]-1) :
            corner = corners[i,:,:]
            x = corner.astype(int)[0,0]
            y = corner.astype(int)[0,1]
            cv2.circle(image,(x,y),3,(0,255,0),-1)
    return image


## DRAWS THE CENTRE OF CHESSBOARD ON THE FRAME AND PRINTS THE COORDINATES OF THE 
## CENTRE TO THE TERMINAL

def draw_centre(corners, image) :
    mid_x = np.median(corners[:,:,0])
    mid_y = np.median(corners[:,:,1])
    print(int(np.round(mid_x)),int(np.round(mid_y)))
    cv2.circle(image,(int(np.round(mid_x)),int(np.round(mid_y))),5,(255,0,0),-1)
    return image     


#MAIN PART OF CODE

vid = cv2.VideoCapture("data/Tello_video.mp4")
total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
print(vid.get(cv2.CAP_PROP_FPS))

#TAKES EACH FRAME FROM THE VIDEO AND APPLIES USERS REQUESTS
for j in range(0,total_frames-1) :

    frame = vid.read()[1]
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    board_corners = cv2.goodFeaturesToTrack(grey_frame,300, 0.1, 2)    

#   frame = draw_points(board_corners, frame)
   
    frame_with_centre = draw_centre(board_corners, frame)        
    
    cv2.imshow("First FRame", frame_with_centre)
    cv2.waitKey(20) #FPS is 30 frames must be played approx. every 33ms. Take off 10ms for processing time. 

vid.release()