import pandas as pd
import requests
from datetime import datetime
import plotly.offline as py
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots

pio.orca.config.executable = 'C:\\Users\\Rogachevich_IA\\AppData\\Local\\Programs\\orca\\orca.exe'
class GraphMulti:
	fig = None

	def __init__(self, x, y, title, width):
		self.fig = make_subplots(rows=y, cols=x, shared_xaxes=False, vertical_spacing=0.03, subplot_titles=title, row_width=width)

	def addCandle(self, df, x, y):
		self.fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],low=df["Low"], close=df["Close"], name="OHLC"), row=x, col=y)

	def addScater(self, df, x, y):
		self.fig.add_trace(go.Scatter(x=df.index, y=df['y']), row=x, col=y)

	def prepare(self, x, y, name='AutoGraph'):
		self.fig.update(layout_xaxis_rangeslider_visible=False)
		self.fig['layout'].update(height = y, width = x, title = name, xaxis=dict(tickangle=-90))
		
	def save(self, img = True):
		if img:
			self.fig.write_image("./image.png")
		else:
			# py.iplot(self.fig)
			self.fig.show()

