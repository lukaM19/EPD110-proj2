
#!/bin/bash

# ========================================
# Run Tello Python dev container on macOS
# ========================================

CONTAINER_NAME="tello-container"
IMAGE_NAME="tello-dev"

# Directory containing this script
WORKING_DIRECTORY="$(cd "$(dirname "$0")" && pwd)"

echo "Starting container $CONTAINER_NAME from image $IMAGE_NAME"
echo "Mounting $WORKING_DIRECTORY to /workspace"

docker run -it --rm \
    --name "$CONTAINER_NAME" \
    --network host \
    -e DISPLAY=host.docker.internal:0 \
    --mount "type=bind,source=$WORKING_DIRECTORY,target=/workspace" \
    -w /workspace \
    "$IMAGE_NAME"
