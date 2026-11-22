import cv2
import numpy as np

## DRAWS ALL CORNERS FOUND ON THE FRAME

def draw_points(corners, image) :
    for i in range(0,corners.shape[0]) :
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


## RETURNS (x, y) OF THE CHESSBOARD CENTRE AS FRACTIONS OF FRAME WIDTH/HEIGHT (0..1),
## OR None IF NO CHESSBOARD IS IN THE FRAME.
## pattern_size = NUMBER OF INNER CORNERS (cols, rows) OF YOUR BOARD

def detect_chessboard(frame, pattern_size=(7, 7)) :
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(grey, pattern_size, flags=cv2.CALIB_CB_FAST_CHECK)
    if not found :
        return None
    h, w = grey.shape
    return np.median(corners[:,:,0]) / w, np.median(corners[:,:,1]) / h


#MAIN PART OF CODE (ONLY RUNS WHEN THIS FILE IS EXECUTED DIRECTLY)

if __name__ == "__main__" :
    vid = cv2.VideoCapture("data/Tello_video.mp4")
    print(vid.get(cv2.CAP_PROP_FPS))

    while True :
        ok, frame = vid.read()
        if not ok :
            break

        hit = detect_chessboard(frame)
        if hit :
            print(f"Chessboard at x={hit[0]:.3f}, y={hit[1]:.3f}")

        cv2.imshow("First FRame", frame)
        if cv2.waitKey(20) & 0xFF == ord("q") :
            break

    vid.release()
    cv2.destroyAllWindows()