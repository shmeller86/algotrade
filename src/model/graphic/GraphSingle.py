class GraphSingle:
	fig = None

	def __init__(self):
		self.fig = make_subplots(specs=[[{"secondary_y": True}]])

	def addCandlePrimary(self, df):
		level_min = str(df.loc[:,["Low"]].min())
		trace = go.Candlestick(
			x=df.index, 
			open=df["Open"], 
			high=df["High"],
			low=df["Low"], 
			close=df["Close"], 
			name="OHLC"
		)
		
		self.fig.add_trace(trace)

	def addCandleSlave(self, signal):
		trace = go.Scatter(
				x=signals['dodge_signal_x'],
				y=signals['dodge_signal_y'],
				name='Dodge pattern',
				mode='markers',
				marker=dict(size=5, color='#000000'),
				yaxis='y2'
			)
		self.fig.add_trace(trace,secondary_y=True)

	def prepare(self, x, y, name='AutoGraph'):
		self.fig['layout'].update(height = y, width = x, title = name, xaxis=dict(tickangle=-90))

		

	def save(self, img = True):
		if img:
			self.fig.write_image("./image.png")
		else:
			py.iplot(self.fig)


	def graphic(df, signals=None):
		level_min = str(df.loc[:,["Low"]].min())
		trace1 = go.Candlestick(
			x=df.index, 
			open=df["Open"], 
			high=df["High"],
			low=df["Low"], 
			close=df["Close"], 
			name="OHLC"
		)
		
		fig = make_subplots(specs=[[{"secondary_y": True}]])
		fig.add_trace(trace1)


		if signals:
			trace2 = go.Scatter(
				x=signals['dodge_signal_x'],
				y=signals['dodge_signal_y'],
				name='Dodge pattern',
				mode='markers',
				marker=dict(size=5, color='#000000'),
				yaxis='y2'
			)
			fig.add_trace(trace2,secondary_y=True)

		# trace2 = px.scatter(x=dodge_signal_x, y=dodge_signal_y)


		# trace3 = go.Scatter(x=['2021-03-13 00:00','2021-03-13 01:05'],
		# y=['Low	29.2\ndtype: float64','Low	32.2\ndtype: float64'],
		# name='Cumulative Percentage'
		# )

		# fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
		#				  size='petal_length', hover_data=['petal_width'])

		
		
		# fig.add_trace(trace3,secondary_y=True)
		fig['layout'].update(height = 800, width = 1000, title = 'canndle',xaxis=dict(tickangle=-90))
		#py.iplot(fig)
		fig.write_image("./fig1.png")
