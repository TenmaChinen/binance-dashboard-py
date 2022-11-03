from callbacks import Callbacks
from layout import Layout
from chart import Chart

if __name__ == '__main__' :
	layout = Layout()
	root, fig = layout.root, layout.fig
	chart = Chart(fig)
	chart.select_axis(chart.ax_1)

	callbacks = Callbacks(layout, chart)

	# Test
	layout.sv_asset_1.set('BNB')
	layout.sv_asset_2.set('USDT')
	# load_plot()

	root.mainloop()