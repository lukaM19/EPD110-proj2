import math, threading
import cv2
from tello import Tello
from tello_test_py3 import KeepAlive
from occupancy import build_occupancy_matrix
from planner import plan_route
from chessboard import detect_chessboard

# Assumes the drone starts facing +row and never rotates.
DIRS = {(1, 0): "forward", (-1, 0): "back", (0, 1): "right", (0, -1): "left"}

def route_to_commands(route, cell_size_cm):
    assert cell_size_cm >= 20, "Tello minimum move is 20 cm"
    moves = []
    for (r0, c0), (r1, c1) in zip(route, route[1:]):
        d = DIRS.get((r1 - r0, c1 - c0))
        if d is None:
            raise ValueError(f"Non-adjacent step {(r0, c0)} -> {(r1, c1)}")
        if moves and moves[-1][0] == d:
            moves[-1][1] += cell_size_cm          # merge straight runs
        else:
            moves.append([d, cell_size_cm])
    cmds = []
    for d, dist in moves:                          # Tello max is 500 cm per move
        k = math.ceil(dist / 500)
        cmds += [f"{d} {dist // k}"] * k
    return cmds

def fly_route(tello, cmds):
    for c in ["command", "streamon", "takeoff", *cmds]:
        tello.send_command(c)

def detect_loop():
    cap = cv2.VideoCapture("udp://@0.0.0.0:11111", cv2.CAP_FFMPEG)
    try:
        if not cap.isOpened():
            print("Could not open Tello video stream on UDP 11111")
            return
        while True:
            ok, img = cap.read()
            if not ok:
                continue

            hit = detect_chessboard(img)
            if hit:
                print(f"Chessboard at x={hit[0]:.3f}, y={hit[1]:.3f}")
            cv2.imshow("Tello", img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

def main():
    start, end = (0, 0), (1, 1)
    grid = build_occupancy_matrix(2, 2, start, end, obstacles=[])#(1, 1), (2, 3)])
    #temp , forward 1 rught one
    route = [(0, 0), (1, 0), (1, 1)]
    cmds = route_to_commands(route, cell_size_cm=100)
    print(cmds)
    #cmds = route_to_commands(plan_route(grid, start, end), cell_size_cm=50)
    tello = Tello()
    fly_route(tello, cmds)
    keep = KeepAlive(tello)
    t = threading.Thread(target=keep, daemon=True)
    t.start()
    try:
        detect_loop()
    finally:
        keep.shutdown()
        t.join()
        tello.send_command("streamoff")
        tello.send_command("land")

if __name__ == "__main__":
    main()