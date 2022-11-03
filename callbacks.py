from threading import Thread
import binance as bnb


class Callbacks:

    def __init__(self, layout, chart):
        self.layout = layout
        self.chart = chart
        self.__set_callbacks()

    def __set_callbacks(self):
        self.layout.set_callbacks(
            on_click_seek=self.on_click_seek,
            on_click_asset=self.on_click_asset,
            on_press_enter=self.on_press_enter,
            on_selected_option=self.on_selected_option,
            on_select_fav=self.on_select_fav,
        )

    def on_click_seek(self, id_seek):
        asset_1, last_1 = self.layout.get_seek(id_seek=Layout.SEEK_1)
        asset_2, last_2 = self.layout.get_seek(id_seek=Layout.SEEK_2)
        if ((id_seek == Layout.SEEK_1) and (asset_2 == last_2) and (asset_1 != '')) or\
                ((id_seek == Layout.SEEK_2) and (asset_1 == last_1) and (asset_2 != '')):
            self.layout.show_dialog()
            return

        asset_to = asset_2 if id_seek == Layout.SEEK_1 else asset_1
        l_filt_assets = filter_assets(asset_to)
        if l_filt_assets:
            self.layout.set_dialog_content(l_texts=l_filt_assets)
            self.layout.show_dialog()
        else:
            pass
            # show no match

    def on_press_enter(self):
        self.load_plot()

    def on_click_asset(self, asset):
        if self.layout.current_seek == Layout.SEEK_1:
            self.layout.sv_asset_1.set(asset)
        else:
            self.layout.sv_asset_2.set(asset)
        self.layout.hide_dialog()

        self.load_plot()

    def on_selected_option(self, option):
        if option == self.layout.FAV:
            asset_1, asset_2 = self.layout.get_assets()
            result = bnb.get_pair(asset_1, asset_2)
            if result:
                pair_sym, pair_name = result
                self.layout.add_favourite(pair_name)

    def on_select_fav(self, pair_name):
        asset_1, asset_2 = pair_name.split('-')
        self.load_plot(l_assets=(asset_1, asset_2))

    # M E T H O D S

    def load_plot(self, l_asset_pair=None):
        def task():
            if l_asset_pair is None:
                asset_1, asset_2 = self.layout.get_assets()
            else:
                asset_1, asset_2 = l_asset_pair

            result = bnb.get_pair(asset_1, asset_2)
            if result:
                pair_sym, pair_name = result
                l_ts, l_closes = bnb.get_last_closes(pair=pair_sym, interval='1h')
                self.chart.set_data(title=pair_name, x_data=l_ts, y_data=l_closes)
                self.layout.set_message(pair_name)
            else:
                self.layout.set_message('Pair No Exist')

        self.layout.set_message('LOADING...')
        Thread(target=task, args=()).start()

    @staticmethod
    def filter_assets(asset_from):
        if asset_from == '':
            return bnb.l_assets

        l_assets_to = bnb.get_to_assets(asset_from)
        return l_assets_to
