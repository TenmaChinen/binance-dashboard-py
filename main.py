from threading import Thread
from layout import Layout
from chart import Chart
import binance as bnb

def on_click_seek(id_seek):
	asset_1, last_1 = layout.get_seek(id_seek=Layout.SEEK_1)
	asset_2, last_2 = layout.get_seek(id_seek=Layout.SEEK_2)
	if (( id_seek == Layout.SEEK_1 ) and (asset_2 == last_2) and (asset_1 != '')) or\
		(( id_seek == Layout.SEEK_2 ) and (asset_1 == last_1) and (asset_2 != '')):
		layout.show_dialog()
		return

	asset_to = asset_2 if id_seek == Layout.SEEK_1 else asset_1
	l_filt_assets = filter_assets(asset_to)
	if l_filt_assets:
		layout.set_dialog_content(l_texts=l_filt_assets)
		layout.show_dialog()
	else:
		pass
		# show no match

def filter_assets(asset_from):
	if asset_from == '':
		return bnb.l_assets

	l_assets_to = bnb.get_to_assets(asset_from)
	return l_assets_to

def on_click_asset(asset):
	if layout.current_seek == Layout.SEEK_1:
		layout.sv_asset_1.set(asset)
	else:
		layout.sv_asset_2.set(asset)
	layout.hide_dialog()

	load_plot()

def load_plot(l_assets=None):
	def task():
		if l_assets is None:
			asset_1, asset_2 = layout.get_assets()
		else:
			asset_1, asset_2 = l_assets

		print(asset_1, asset_2)
		result = bnb.get_pair(asset_1,asset_2)
		if result:
			pair_sym, pair_name = result
			l_ts, l_closes = bnb.get_last_closes(pair=pair_sym, interval='1h')
			chart.set_data(title=pair_name, x_data = l_ts, y_data = l_closes)
			layout.set_message(pair_name)
		else:
			layout.set_message('Pair No Exist')

	layout.set_message('LOADING...')
	Thread(target=task, args=()).start()


def on_selected_option(option):
	if option == layout.FAV:
		asset_1, asset_2 = layout.get_assets()
		result = bnb.get_pair(asset_1,asset_2)
		if result:
			pair_sym, pair_name = result
			layout.add_favourite(pair_name)

def on_select_fav(pair_name):
	asset_1, asset_2 = pair_name.split('-')
	load_plot(l_assets=(asset_1,asset_2))

if __name__ == '__main__' :
	layout = Layout()
	layout.set_callbacks(
		on_click_seek = on_click_seek,
		on_click_asset = on_click_asset,
		on_press_enter = load_plot,
		on_selected_option = on_selected_option,
		on_select_fav = on_select_fav,
		)
	root, fig = layout.root, layout.fig

	chart = Chart(fig)
	chart.select_axis(chart.ax_1)

	# Test
	layout.sv_asset_1.set('BNB')
	layout.sv_asset_2.set('USDT')
	# load_plot()

	root.mainloop()