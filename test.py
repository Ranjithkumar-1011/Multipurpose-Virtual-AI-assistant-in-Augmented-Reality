print("START")

import sounddevice as sd

print("IMPORTED")

devices = sd.query_devices()
print("DEVICES FOUND:")
print(devices)
