import argparse
import json
import math

parser = argparse.ArgumentParser(prog='Gy Calculator', description='Calculate grain yield through the use of weather data and satellite imagery')

parser.add_argument('-f', '--filename')
parser.add_argument('-p', '--practical-yield', type=float)
args = parser.parse_args()

previous_evi = 0

def calc_apar(date):
    global previous_evi

    closest_evi = previous_evi
    if 'EVI' in date:
        closest_evi = date['EVI']
        previous_evi = date['EVI']

    k = 0.5 # K is the Light Interception Coefficient, it is a constant value
    lai = 3.618 * (closest_evi) - 0.118 # LAI is the Leaf Area Index, it is calculated by multiplying the Enhanced Vegetation Index (EVI) by 3.618 and subtracting 0.118. EVI is calculated via satellite imagery
    ec = 0.48 # EC is the Climate Coefficient, it is a constant value
    rg = date['Q'] * 0.01 # Rg is the global radiation per day in J/cm² provided by the KNMI, this alogritm uses MJ/m²

    apar = (1.0 - math.exp(-k * lai)) * ec * rg
    return apar

def calc_ft(t):
    t_min = 0 # t_min is the minimum temperature at which wheat can grow
    t_max = 30 # t_max is the maximum temperature at which wheat can grow
    t_opt = 17 # t_opt is the optimal temperature at which wheat grows

    if t > t_min and t < t_opt:
        return 1 - ((t_opt - t) / (t_opt - t_min))**2
    elif t > t_opt and t < t_max:
        return 1 - ((t - t_opt) / (t_max - t_opt))**2
    elif t == 17:
        return 1
    else:
        return 0

with open(args.filename, 'r') as json_file:
    dates = json.load(json_file)

    gy = 0

    for date in dates:
        py = 0.0051
        stt = 1008 # STT is the Soil Temperature Threshold, it is a constant value. Once STT has been reached by summing the daily average temperatures, the wheat will start growing grain granules
        dam = 0

        total_temp = 0

        for step in range(dates.index(date) + 1): # Add one in order to include the current date
            total_temp += dates[step]['TG'] * 0.1 # TG is the average temperature for the day in 0,1 degrees Celsius provided by the KNMI

            elue = 2.617 # ELUE is the Effective Light Use Efficiency, it is calulated by deviding the Dry Above Pytomass (DAM) by the global radiation (Rg)
            apar = calc_apar(dates[step])
            ft = calc_ft(dates[step]['TG'] * 0.1)

            d_dam = elue * apar * ft
            dam += d_dam
        
        if total_temp > stt:
            d_gy = (dam * py)
            gy += d_gy

    json_file.close()

    print('gy:', (gy * 0.01), 't/ha') # The grain yield is calculated by multiplying the total Dry Above Pytomass (DAM) by the Pytomass Yield (PY) and multiplied by 0.01 to convert it to t/ha