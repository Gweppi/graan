# import pandas

# range = pandas.date_range(start="2020-01-01T00:00:000Z", end="2020-01-10T00:00:000Z", freq="D")
# print("2020-01-10T00:00:000Z" in range)

def translate(value, leftMin, leftMax, rightMin, rightMax):
# Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

print(translate(256, 0, 512, 0, 1))