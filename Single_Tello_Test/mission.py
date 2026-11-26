import math, threading
import cv2
from tello import Tello
from tello_test_py3 import KeepAlive
from occupancy import build_occupancy_matrix, world_to_cell, cell_to_world
from planner import plan_route
from chessboard import detect_chessboard

# Assumes the drone starts facing +row and never rotates.
# Drone starts at drone_start facing +x. +y is to its left.
AXIS_TO_CMD = {(1, 0): "forward", (-1, 0): "back", (0, 1): "left", (0, -1): "right"}

def route_to_commands(route, x_min, y_min, cell_cm):
    pts = [cell_to_world(c, x_min, y_min, cell_cm) for c in route]
    moves = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        step = (int(math.copysign(1, x1 - x0)) if x1 != x0 else 0,
                int(math.copysign(1, y1 - y0)) if y1 != y0 else 0)
        if step not in AXIS_TO_CMD or abs(x1 - x0) + abs(y1 - y0) != cell_cm:
            raise ValueError(f"Non-adjacent step {(x0, y0)} -> {(x1, y1)}")
        d = AXIS_TO_CMD[step]
        if moves and moves[-1][0] == d:
            moves[-1][1] += cell_cm
        else:
            moves.append([d, cell_cm])
    cmds = []
    for d, dist in moves:
        if dist < 20:
            raise ValueError(f"'{d} {dist}' is below the Tello 20 cm minimum")
        k = math.ceil(dist / 500)              # Tello max is 500 cm per move
        q, rem = divmod(dist, k)
        cmds += [f"{d} {q + 1}"] * rem + [f"{d} {q}"] * (k - rem)
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

# All measurements in cm
X_MIN, X_MAX = -200, 900
Y_MIN, Y_MAX = -200, 400
CELL_CM = 50
OBSTACLES_XY_CM = [(350, y) for y in range(-100, 101, 10)]
DRONE_START = (200, -100)
DRONE_FINISH = (500, 0)

def main():
    grid, start, end = build_occupancy_matrix(
        X_MIN, X_MAX, Y_MIN, Y_MAX, DRONE_START, DRONE_FINISH, OBSTACLES_XY_CM, CELL_CM)
    print(grid)
    route = plan_route(grid, start, end)
    cmds = route_to_commands(route, X_MIN, Y_MIN, CELL_CM)
    print(cmds)
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
