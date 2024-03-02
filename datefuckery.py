import pandas

range = pandas.date_range(start="2020-01-01T00:00:000Z", end="2020-01-10T00:00:000Z", freq="D")
print("2020-01-10T00:00:000Z" in range)