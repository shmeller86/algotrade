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
    # iv = min(i, len([1,2,3,4,5,6,7,8,9,10])-1)
    # objects = [1,2,3,4,5,6,7,8,9,10]
    # y_pos = np.arange(len(objects))
    # performance = [1,2,3,4,5,6,7,8,9,10]
    # if bar == 'vertical':
    #     plt.bar(y_pos, performance, align='center', color=['green'])
    #     plt.xticks(y_pos, objects)
    #     plt.ylabel('Deaths')
    #     plt.xlabel('Countries')
    #     plt.title('Deaths per Country \n' + str(df1.index[iv].strftime('%y-%m-%d')))
    # else:
    # print(y_pos)

    b = []
    c = []
    while True:
        b.append(random.randint(1,11))
        c.append(random.randint(1,11))
        if len(b) == 10:
            break
    # c = [x for x in [randrange(0, 10)]]
    print(b)
    print([x for x in range(1,11)])

    plt.barh(b, ['Объем 1', 'Объем 2', 'Объем 3', 'Объем 4', 'Объем 5', 'Объем 6', 'Объем 7', 'Объем 8', 'Объем 9', 'Объем 10'], align='center', color=['red'])
    plt.yticks(c, ['Цена 1', 'Цена 2', 'Цена 3', 'Цена 4', 'Цена 5', 'Цена 6', 'Цена 7', 'Цена 8', 'Цена 9', 'Цена 10'])
    plt.xlabel('Deaths')
    plt.ylabel('Countries')
animator = ani.FuncAnimation(fig, buildmebarchart, interval=100)
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