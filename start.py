import skyv_flask as skyvision
from skyv_operations import getOperations

skyvision.setResolution(0.5)
skyvision.run(getOperations())