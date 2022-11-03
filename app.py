from controller import Controller
from view import View

class App:
	def __init__(self):
		self.view = View()
		self.controller = Controller(self.view)
		self.view.set_controller(self.controller)

		# Default
		self.view.sv_asset_1.set('BNB')
		self.view.sv_asset_2.set('USDT')
		# load_plot()		

	def run(self):
		self.view.root.mainloop()

if __name__ == '__main__' :
	app = App()
	app.run()