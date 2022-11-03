from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure
from datetime import datetime

class Chart:

    def __init__(self, parent):
        self.parent = parent
        self.fig = self.__create_fig()
        self.canvas = self.fig.canvas.get_tk_widget()
        self.__create_plots()
        self.__create_hlines()
        self.fig.tight_layout()
        self.fig.subplots_adjust(wspace=0, hspace=0.15, left=0.02, bottom=0.05, right=0.95)
        self.__set_events()

    def __create_fig(self):
        fig = Figure()
        canvas_tk_agg = FigureCanvasTkAgg(fig, master=self.parent)
        return fig

    def __create_plots(self):
        self.ax_1 = self.fig.add_subplot(211)
        self.ax_2 = self.fig.add_subplot(212)
        self.lines_1, = self.ax_1.plot([], [], lw=0.6, color='#62D1FF')
        self.lines_2, = self.ax_2.plot([], [], lw=0.6, color='#62FF66')

    def __create_hlines(self):
        self.pct_tool_1 = PercentTool(ax=self.ax_1, color='cyan')
        self.pct_tool_2 = PercentTool(ax=self.ax_2, color='lime')

    def __set_events(self):
        self.fig.canvas.mpl_connect('button_press_event', self.__on_btn_press)
        self.fig.canvas.mpl_connect(
            'button_release_event', self.__on_btn_release)

    def __on_btn_press(self, event):
        self.select_axis(event.inaxes)
        self.cid_mouse_move = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.__on_mouse_move)
        self.pct_tool.set_start(x=event.xdata, y=event.ydata)
        self.fig.canvas.draw_idle()

    def __on_mouse_move(self, event):
        self.pct_tool.set_moving(x=event.xdata, y=event.ydata)
        self.fig.canvas.draw_idle()

    def __on_btn_release(self, event):
        self.fig.canvas.mpl_disconnect(self.cid_mouse_move)
        self.pct_tool.set_ending(x=event.xdata, y=event.ydata)
        self.fig.canvas.draw_idle()

    def clear_axes_border_color(self):
        for ax in self.fig.axes:
            self.set_ax_border_color(ax, 'black')

    def select_axis(self, ax):
        self.clear_axes_border_color()
        if ax:
            self.set_ax_border_color(ax, 'white')
            self.selected_axis = ax
            if ax == self.ax_1:
                self.pct_tool = self.pct_tool_1
            else:
                self.pct_tool = self.pct_tool_2
            self.fig.canvas.draw()

    def set_data(self, title, x_data, y_data, ax=None):
        if ax is None:
            ax = self.selected_axis

        self.pct_tool.clear()

        ax.set_title(title, x=0.01, y=0.94, ha='left', va='top')
        lines = ax.get_lines()[0]
        lines.set_data(x_data, y_data)

        length = len(x_data)
        step = length // 10
        x_ticks = [x_data[x] for x in range(0, length, step)][1:]
        x_tick_labels = [self.format_time(ts) for ts in x_ticks]

        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_tick_labels)

        x_min, x_max = min(x_data), max(x_data)

        y_min, y_max = min(y_data), max(y_data)
        y_delta = y_max-y_min
        y_min = y_min - y_delta * 0.01
        y_max = y_max + y_delta * 0.01

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        self.fig.canvas.draw_idle()

    @staticmethod
    def set_ax_border_color(ax, color):
        for part in ['bottom', 'top', 'left', 'right']:
            ax.spines[part].set_color(color)

    @staticmethod
    def format_time(ts):
        dt = datetime.fromtimestamp(ts//1000)
        return dt.strftime('%d-%m-%y')


d_text = dict(
    size=14, color='w', ha='center', va='center',
    bbox=dict(boxstyle='round', ec='k', fc='k', linewidth=3))


class PercentTool:

    def __init__(self, ax, color):
        self.ax = ax
        self.line_1 = ax.axhline(linestyle='--', lw=0.5, color=color)
        self.line_2 = ax.axhline(linestyle='--', lw=0.5, color=color)
        self.text = ax.text(x=0, y=0, s=None, **d_text)

    def update_xdelta(self):
        self.x_min, self.x_max = self.ax.get_xlim()
        self.x_delta = (self.x_max-self.x_min)

    def x_min_max(self, x):
        margin = self.x_delta * 0.05
        x_l, x_r = x - margin, x + margin
        x_l = (x_l - self.x_min)/(self.x_delta)
        x_r = (x_r - self.x_min)/(self.x_delta)
        return (x_l, x_r)

    def set_start(self, x, y):
        self.update_xdelta()
        self.line_1.set_xdata(self.x_min_max(x))
        self.line_1.set_ydata(y)
        self.line_1.set_visible(True)
        self.line_2.set_visible(False)

    def set_moving(self, x, y):
        self.line_2.set_visible(True)
        self.line_2.set_xdata(self.x_min_max(x))
        self.line_2.set_ydata(y)

    def set_ending(self, x, y):
        self.line_2.set_xdata(self.x_min_max(x))
        self.line_2.set_ydata(y)
        self.set_text_pos(x, y)
        self.update_text()

    def set_text_pos(self, x, y):
        y_min, y_max = self.ax.get_ylim()
        y_delta = (y_max-y_min)
        if y > (y_min + y_delta * 0.9):
            y = self.line_1.get_ydata() - y_delta * 0.1
        else:
            y = y + y_delta * 0.1

        self.text.set_position((x, y))

    def update_text(self):
        pct_change = self.get_pct_change()
        self.text.set_text(f'{pct_change:0.2f} %')

    def get_pct_change(self):
        y_1 = self.line_1.get_ydata()
        y_2 = self.line_2.get_ydata()
        y_min, y_max = sorted((y_1, y_2))
        return (y_max - y_min) / y_min * 100

    def clear(self):
        self.text.set_text(None)
        self.line_1.set_visible(False)
        self.line_2.set_visible(False)