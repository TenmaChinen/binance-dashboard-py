from threading import Thread
import binance as bnb
from view import View

class Controller:

    def __init__(self, view):
        self.view = view
        self.chart = view.chart

    ################################################
    ############   C A L L B A C K S   #############
    ################################################

    def on_click_seek(self, id_seek):
        asset_1, last_1 = self.view.get_seek(id_seek=View.SEEK_1)
        asset_2, last_2 = self.view.get_seek(id_seek=View.SEEK_2)
        if ((id_seek == View.SEEK_1) and (asset_2 == last_2) and (asset_1 != '')) or\
                ((id_seek == View.SEEK_2) and (asset_1 == last_1) and (asset_2 != '')):
            self.view.show_dialog()
            return

        asset_to = asset_2 if id_seek == View.SEEK_1 else asset_1
        l_filt_assets = self.filter_assets(asset_to)
        if l_filt_assets:
            self.view.set_dialog_content(l_texts=l_filt_assets)
            self.view.show_dialog()
        else:
            pass
            # show no match

    def on_press_enter(self):
        self.load_plot()

    def on_click_asset(self, asset):
        if self.view.current_seek == View.SEEK_1:
            self.view.sv_asset_1.set(asset)
        else:
            self.view.sv_asset_2.set(asset)
        self.view.hide_dialog()

        self.load_plot()

    def on_selected_option(self, option):
        if option == self.view.FAV:
            asset_1, asset_2 = self.view.get_assets()
            result = bnb.get_pair(asset_1, asset_2)
            if result:
                pair_sym, pair_name = result
                self.view.add_favourite(pair_name)

    def on_click_fav(self, pair_name):
        asset_1, asset_2 = pair_name.split('-')
        self.load_plot(l_asset_pair=(asset_1, asset_2))

    ################################################
    ##############   M E T H O D S   ###############
    ################################################

    def load_plot(self, l_asset_pair=None):
        def task():
            if l_asset_pair is None:
                asset_1, asset_2 = self.view.get_assets()
            else:
                asset_1, asset_2 = l_asset_pair

            result = bnb.get_pair(asset_1, asset_2)
            if result:
                pair_sym, pair_name = result
                l_ts, l_closes = bnb.get_last_closes(pair=pair_sym, interval='1h')
                self.chart.set_data(title=pair_name, x_data=l_ts, y_data=l_closes)
                self.view.set_message(pair_name)
            else:
                self.view.set_message('Pair No Exist')

        self.view.set_message('LOADING...')
        Thread(target=task, args=()).start()

    @staticmethod
    def filter_assets(asset_from):
        if asset_from == '':
            return bnb.l_assets

        l_assets_to = bnb.get_to_assets(asset_from)
        return l_assets_to
