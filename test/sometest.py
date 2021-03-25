import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
df = pd.read_csv(url, delimiter=',', header='infer')
df_interest = df.loc[
    df['Country/Region'].isin(['United Kingdom', 'US', 'Italy', 'Germany'])
    & df['Province/State'].isna()]
# df_interest.rename(
#     index=lambda x: df_interest.at[x, 'Country/Region'], inplace=True)
df1 = df_interest.transpose()
df1 = df1.drop(['Province/State', 'Country/Region', 'Lat', 'Long'])
df1 = df1.loc[(df1 != 0).any(1)]
df1.index = pd.to_datetime(df1.index)

print(df1)





# color = ['red', 'green', 'blue', 'orange']
# fig = plt.figure()
# plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
# plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
# plt.ylabel('No of Deaths')
# plt.xlabel('Dates')
#
# def buildmebarchart(i=int):
#     plt.legend(df1.columns)
#     p = plt.plot(df1[:i].index, df1[:i].values) #note it only returns the dataset, up to the point i
#     for i in range(0,4):
#         p[i].set_color(color[i]) #set the colour of each curve
# import matplotlib.animation as ani
# animator = ani.FuncAnimation(fig, buildmebarchart, interval = 100)
# plt.show()




# import numpy as np
# import matplotlib.pyplot as plt
# fig,ax = plt.subplots()
# explode=[0.01,0.01,0.01,0.01] #pop out each slice from the pie
# def getmepie(i):
#     def absolute_value(val): #turn % back to a number
#         a  = np.round(val/100.*df1.head(i).max().sum(), 0)
#         return int(a)
#     ax.clear()
#     plot = df1.head(i).max().plot.pie(y=df1.columns,autopct=absolute_value, label='',explode = explode, shadow = True)
#     plot.set_title('Total Number of Deaths\n' + str(df1.index[min( i, len(df1.index)-1 )].strftime('%y-%m-%d')), fontsize=12)
# import matplotlib.animation as ani
# animator = ani.FuncAnimation(fig, getmepie, interval = 200)
# plt.show()










# fig = plt.figure()
# bar = ''
# def buildmebarchart(i=int):
#     iv = min(i, len(df1.index)-1) #the loop iterates an extra one time, which causes the dataframes to go out of bounds. This was the easiest (most lazy) way to solve this :)
#     objects = df1.max().index
#     y_pos = np.arange(len(objects))
#     performance = df1.iloc[[iv]].values.tolist()[0]
#     if bar == 'vertical':
#         plt.bar(y_pos, performance, align='center', color=['red', 'green', 'blue', 'orange'])
#         plt.xticks(y_pos, objects)
#         plt.ylabel('Deaths')
#         plt.xlabel('Countries')
#         plt.title('Deaths per Country \n' + str(df1.index[iv].strftime('%y-%m-%d')))
#     else:
#         plt.barh(y_pos, performance, align='center', color=['red', 'green', 'blue', 'orange'])
#         plt.yticks(y_pos, objects)
#         plt.xlabel('Deaths')
#         plt.ylabel('Countries')
# animator = ani.FuncAnimation(fig, buildmebarchart, interval=100)
# plt.show()


import random
fig = plt.figure()
bar = ''
def buildmebarchart(i=int):
    prices = ['Nuclear', 'Hydro', 'Gas', 'Oil', 'Coal', 'Biofuel']
    energy = []
    variance = [1, 2, 7, 4, 2, 3]

    x_pos = [i for i, _ in enumerate(prices)]


    while True:
        energy.append(random.randint(1,1000))
        if len(energy) == 6:
            break
    plt.clf()
    plt.barh(x_pos, energy, color=['green','green','green','red','red','red'], xerr=None)
    plt.ylabel("Energy Source")
    plt.xlabel("Energy Output (GJ)")
    plt.title("Energy output from various fuel sources")
    plt.yticks(x_pos, prices)
animator = ani.FuncAnimation(fig, buildmebarchart, interval=1000)
plt.show()




#
# import random
# from itertools import count
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
#
# plt.style.use('fivethirtyeight')
#
# x_values = []
# y_values = []
#
# index = count()
#
#
# def animate(i):
#     x_values.append(next(index))
#     y_values.append(random.randint(0, 5))
#     plt.cla()
#     plt.plot(x_values, y_values)
#
#
# ani = FuncAnimation(plt.gcf(), animate, 1000)
#
#
# plt.tight_layout()
# plt.show()