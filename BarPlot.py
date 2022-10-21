import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os



class BarPlot:

	color = "black"
	bar_thickness = 0.5
	figsize = (10, 6)
	fontsize = 10
	tight_layout_flag = True
	
	xlabel = "x-axis"
	ylabel = "y-axis"
	title = "Bar Plot"
	rotation = 0
	label_order = None
	xlim, ylim = -1, -1

	# location values = ['upper left', 'upper right', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center']
	# font values = {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
	legend = False
	legend_loc = "best"
	legend_cols = 1
	legend_fontsize = "medium"
	legend_title = "Legend"
	bbox_to_anchor=(0.8, 1.2)

	# axis: {'both', 'x', 'y'}
	plot_grid = False
	grid_color = "lightgray"
	grid_linstyle = "-"
	grid_linewidth = 0.5
	grid_axis = "both"

	# scales can have values like{"linear", "log", "symlog", "logit", ...} [https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xscale.html]
	xscale = "linear"
	yscale = "linear"

	data_type = "dict"
	output_path = "Display"



	def __init__(self, data, xlabel, ylabel, output_path=output_path, rotation=rotation, label_order=None,
				 legend=False, legend_title=None, legend_location=legend_loc, legend_columns=legend_cols, legend_fontsize=legend_fontsize, bbox_to_anchor=bbox_to_anchor,
				 plot_grid=plot_grid, grid_axis=grid_axis, grid_color=grid_color, grid_linstyle=grid_linstyle, grid_linewidth=grid_linewidth,
				 figsize=None, color=color, tight_layout_flag=True, title=None, xscale=xscale, yscale=yscale,
				 thickness=bar_thickness, xlim=-1, ylim=-1):
		
		self.color = color
		self.xscale = xscale
		self.yscale = yscale
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.label_order = label_order if not(legend_title is None) else None
		self.title = title
		self.rotation = rotation
		
		self.bar_thickness = thickness
		self.figsize = figsize
		self.tight_layout_flag = tight_layout_flag
		self.output_path = output_path
		
		self.legend = legend
		self.legend_loc = legend_location
		self.legend_cols = int(legend_columns)
		self.legend_fontsize = legend_fontsize
		self.legend_title = legend_title if not(legend_title is None) else BarPlot.legend_title
		self.bbox_to_anchor = bbox_to_anchor
		
		self.plot_grid = plot_grid
		self.grid_axis = grid_axis
		self.grid_color = grid_color
		self.grid_linstyle = grid_linstyle
		self.grid_linewidth = grid_linewidth

		if isinstance(data, pd.DataFrame):
			self.data = data
			self.data_type = "DataFrame"
		elif isinstance(data, dict):
			self.data = data
			self.data_type = "dict"
		else:
			self.Data = BarPlot.data
			self.data_type = "dict"

		return


	def standard_bar_plot(self, df_xcolumn=None, df_ycloumn=None, orientation="vertical"):

		x, y = [], []
		if self.data_type == "DataFrame":
			if not(self.label_order is None):
				for label in self.label_order:
					for i in range(len(self.data)):
						temp_x = self.data.iloc[i][df_xcolumn]
						temp_y = self.data.iloc[i][df_ycolumn]
						if (temp_x == label) and (temp_x not in x):
							x.append(temp_x)
							y.append(temp_y)
			else:
				for i in range(len(self.data)):
					temp_x = self.data.iloc[i][df_xcolumn]
					temp_y = self.data.iloc[i][df_ycolumn]
					if temp_x not in x:
						x.append(temp_x)
						y.append(temp_y)
		else:
			if not(self.label_order is None):
				for label in self.label_order:
					for key in self.data.keys():
						if (key == label) and (key not in x):
							x.append(key)
							y.append(self.data[key])
			else:
				x = list(self.data.keys())
				y = list(self.data.values())
		
		if self.figsize is None:
			fig = plt.figure()
		else:
			fig = plt.figure(figsize=self.figsize)

		if self.xscale != "linear":
			plt.xscale(self.xscale)
		if self.yscale != "linear":
			plt.yscale(self.yscale)
		
		if orientation == "horizontal":
			plt.barh(x, y, color=self.color, zorder=3)
			plt.xlabel(self.ylabel)
			plt.ylabel(self.xlabel)
		else:
			plt.bar(x, y, color=self.color, width=self.bar_thickness, zorder=3)
			plt.xlabel(self.xlabel)
			plt.ylabel(self.ylabel)

		if self.xlim > 0:
			plt.xlim(self.xlim)
		if self.ylim > 0:
			plt.ylim(self.ylim)

		if self.rotation != 0:
			plt.setp(ax.get_xticklabels(), rotation=self.rotation, ha='right')

		if not(self.title is None):
			plt.title(self.title)

		if self.legend:
			plt.legend(title=self.legend_title, loc=self.legend_loc, ncol=self.legend_cols, fontsize=self.legend_fontsize)

		if self.plot_grid:
			plt.rcParams['axes.axisbelow'] = True
			plt.grid(axis=self.grid_axis, color=self.grid_color, linestyle=self.grid_linstyle, linewidth=self.grid_linewidth, zorder=0)

		if self.tight_layout_flag:
			plt.tight_layout()

		if self.output_path != "Display":
			plt.savefig(self.output_path, bbox_inches="tight")
		plt.show()
		
		return



	def stacked_bar_plot(self, category_column, positive_label, negative_label, orientation="vertical",
						 positive_color="gray", negative_color="black", plot_text=False,
						 bar_alignment="center"):

		categories, positives, negatives, totals = [], [], [], []
		if self.data_type == "DataFrame":
			for i in range(len(self.data)):
				temp_cat = self.data.iloc[i][category_column]
				temp_pos = self.data.iloc[i][positive_label]
				temp_neg = self.data.iloc[i][df_ycolumn]
				if temp_cat not in categories:
					categories.append(temp_cat)
					positives.append(temp_pos)
					negatives.append(negative_label)
					totals.append(temp_pos+temp_neg)
		else:
			for key in self.data.keys():
				if key not in categories:
					categories.append(key)
					positives.append(self.data[key][positive_label])
					negatives.append(self.data[key][negative_label])
					totals.append(self.data[key][positive_label]+self.data[key][negative_label])

		if self.figsize is None:
			fig = plt.figure()
		else:
			fig = plt.figure(figsize=self.figsize)
		ax = fig.add_subplot(111)

		if orientation == "horizontal":
			ax.barh(categories, negatives, align=bar_alignment, height=self.bar_thickness, label=negative_label, color=negative_color)
			ax.barh(categories, positives, align=bar_alignment, height=self.bar_thickness, left=negatives, label=positive_label, color=positive_color)
			ax.set_yticks(categories)
			ax.set_xlabel(self.ylabel)
			ax.set_ylabel(self.xlabel)
			ax.set_yticklabels(categories, rotation=self.rotation, ha='right')
		else:
			ax.bar(categories, negatives, align=bar_alignment, width=self.bar_thickness, label=negative_label, color=negative_color)
			ax.bar(categories, positives, align=bar_alignment, width=self.bar_thickness, bottom=negatives, label=positive_label, color=positive_color)
			ax.set_xticks(categories)
			ax.set_xlabel(self.xlabel)
			ax.set_ylabel(self.ylabel)
			ax.set_xticklabels(categories, rotation=self.rotation, ha='right')

		if self.xlim > 0:
			plt.xlim(self.xlim)
		if self.ylim > 0:
			plt.ylim(self.ylim)
		
		if plot_text:
			if orientation == "horizontal":
				for index, value in enumerate(totals):
					ax.text(value + 0.2, index - 0.1, totals[index], color=negative_color, fontweight='bold')
			else:
				for index, value in enumerate(totals):
					ax.text(index - 0.1, value + 0.2, totals[index], color=negative_color, fontweight='bold')

		if not(self.title is None):
			plt.title(self.title)

		if self.legend:
			plt.legend(title=self.legend_title, loc=self.legend_loc, ncol=self.legend_cols, fontsize=self.legend_fontsize)

		if self.plot_grid:
			plt.rcParams['axes.axisbelow'] = True
			plt.grid(axis=self.grid_axis, color=self.grid_color, linestyle=self.grid_linstyle, linewidth=self.grid_linewidth)

		if self.tight_layout_flag:
			plt.tight_layout()

		if self.output_path != "Display":
			plt.savefig(self.output_path, bbox_inches="tight")
		plt.show()

		return



	def full_or_multi_stacked_bar_plot(self, stacking_flag=True, normalization_flag=True, orientation="vertical",
									   colorlist=["black", "gray", "silver"]):

		if self.data_type == "dict":
			index = 0
			df = pd.DataFrame(columns=['category', 'sub_category'])
			for key in self.data.keys():
				for sub_key in self.data[key].keys():
					if self.data[key][sub_key] <= 0:
						continue
					for k in range(self.data[key][sub_key]):
						df.loc[index] = [key] + [sub_key]
						index += 1

		x_var, y_var = "category", "sub_category"
		df_grouped = df.groupby(x_var)[y_var].value_counts(normalize=normalization_flag).unstack(y_var)

		xlabel_order = ["B", "A", "R", "P", "L", "O", "T"]
		if orientation == "horizontal":
			df_grouped.loc[xlabel_order].plot.barh(stacked=stacking_flag, color=colorlist, rot=self.rotation, zorder=3)
		else:
			df_grouped.loc[xlabel_order].plot.bar(stacked=stacking_flag, color=colorlist, rot=self.rotation, zorder=3)
		
		# Plot text within the bars
		for category in xlabel_order:
			for cat_index in df_grouped.index:
				if cat_index != category:
					continue
				sub_df = df_grouped.loc[cat_index]
				# print(sub_df, type(sub_df))
				index = xlabel_order.index(category)
				cumulative = 0
				for sub_category, element_value in sub_df.items():
					if element_value > 0.1:
						if orientation == "horizontal":
							# print(cumulative + (element_value / 2), index, cumulative, element_value)
							plt.text(cumulative + (element_value / 2), index, f"{int(element_value * 100)} %", fontsize=8, va="center", ha="center")
						else:
							# print(index, cumulative + (element_value / 2), cumulative, element_value)
							plt.text(index, cumulative + (element_value / 2), f"{int(element_value * 100)} %", fontsize=8, va="center", ha="center")
					cumulative += element_value

		plt.xlabel(self.xlabel)	
		plt.ylabel(self.ylabel)

		if self.xlim > 0:
			plt.xlim(self.xlim)
		if self.ylim > 0:
			plt.ylim(self.ylim)

		if not(self.title is None):
			plt.title(self.title)

		if self.legend:
			plt.legend(title=self.legend_title, loc=self.legend_loc, ncol=self.legend_cols, fontsize=self.legend_fontsize, bbox_to_anchor=self.bbox_to_anchor)

		if self.plot_grid:
			plt.rcParams['axes.axisbelow'] = True
			plt.grid(axis=self.grid_axis, color=self.grid_color, linestyle=self.grid_linstyle, linewidth=self.grid_linewidth, zorder=0)

		if self.tight_layout_flag:
			plt.tight_layout()

		if self.output_path != "Display":
			plt.savefig(self.output_path, bbox_inches="tight")
		plt.show()

		return



	def grouped_bar_plot(self, df_xcolumn=None, df_ycloumn=None, orientation="vertical", bar_group_colors=["black","gray"]):
		
		if self.data_type == "DataFrame":
			# <Enter custom function here, if needed>
			return "Pass <dict> type object as exampled in the main function or write your custom function to update self.data object to expected <dict> format"
		
		num_groups = len(self.data.keys())
		group_size = 2
		group_categories = []
		for key in self.data.keys():
			if self.label_order is None:
				self.label_order = list(self.data.keys())
			group_categories = list(self.data[key].keys())
			group_size = len(group_categories)
			break

		self.bar_thickness = 0.25 if self.bar_thickness > 0.3 else self.bar_thickness

		# bar1, bar2 (for default group_size)
		bars = [[], []]
		# Set position of bar on X axis
		pos1 = np.arange(len(self.label_order))
		pos2 = [x + self.bar_thickness for x in pos1]
		
		if group_size == 3:
			# bar1, bar2, bar3
			bars = [[], [], []]
			pos3 = [x + self.bar_thickness for x in pos2]
			bar_group_colors = ["black", "gray", "silver"] if bar_group_colors == ["black", "gray"] else bar_group_colors
		elif group_size == 4:
			# bar1, bar2, bar3, bar4
			bars = [[], [], [], []]
			pos3 = [x + self.bar_thickness for x in pos2]
			pos4 = [x + self.bar_thickness for x in pos3]
			bar_group_colors = ["maroon", "red", "orange", "yellow"] if bar_group_colors == ["black", "gray"] else bar_group_colors

		for sub_category in group_categories:
			index = group_categories.index(sub_category)
			for axis_label_category in self.label_order:
				if sub_category not in self.data[axis_label_category].keys():
					bars[index].append(0)
					continue
				bars[index].append(self.data[axis_label_category][sub_category])

		if self.figsize is None:
			fig = plt.figure()
		else:
			fig = plt.figure(figsize=self.figsize)

		if self.xscale != "linear":
			plt.xscale(self.xscale)
		if self.yscale != "linear":
			plt.yscale(self.yscale)
		
		if orientation == "horizontal":
			if group_size == 2:
				plt.barh(pos1, bars[0], color=bar_group_colors[0], height=self.bar_thickness, edgecolor='black', label=group_categories[0], zorder=3)
				plt.barh(pos2, bars[1], color=bar_group_colors[1], height=self.bar_thickness, edgecolor='black', label=group_categories[1], zorder=3)
			elif group_size == 3:
				plt.barh(pos1, bars[0], color=bar_group_colors[0], height=self.bar_thickness, edgecolor='black', label=group_categories[0], zorder=3)
				plt.barh(pos2, bars[1], color=bar_group_colors[1], height=self.bar_thickness, edgecolor='black', label=group_categories[1], zorder=3)
				plt.barh(pos3, bars[2], color=bar_group_colors[2], height=self.bar_thickness, edgecolor='black', label=group_categories[2], zorder=3)
			elif group_size == 4:
				plt.barh(pos1, bars[0], color=bar_group_colors[0], height=self.bar_thickness, edgecolor='black', label=group_categories[0], zorder=3)
				plt.barh(pos2, bars[1], color=bar_group_colors[1], height=self.bar_thickness, edgecolor='black', label=group_categories[1], zorder=3)
				plt.barh(pos3, bars[2], color=bar_group_colors[2], height=self.bar_thickness, edgecolor='black', label=group_categories[2], zorder=3)
				plt.barh(pos4, bars[3], color=bar_group_colors[3], height=self.bar_thickness, edgecolor='black', label=group_categories[3], zorder=3) 
			plt.xlabel(self.ylabel)
			plt.ylabel(self.xlabel)
		else:
			if group_size == 2:
				plt.bar(pos1, bars[0], color=bar_group_colors[0], width=self.bar_thickness, edgecolor='black', label=group_categories[0], zorder=3)
				plt.bar(pos2, bars[1], color=bar_group_colors[1], width=self.bar_thickness, edgecolor='black', label=group_categories[1], zorder=3)
				plt.xticks([x+(self.bar_thickness/2) for x in pos1], labels=self.label_order)
			elif group_size == 3:
				plt.bar(pos1, bars[0], color=bar_group_colors[0], width=self.bar_thickness, edgecolor='black', label=group_categories[0], zorder=3)
				plt.bar(pos2, bars[1], color=bar_group_colors[1], width=self.bar_thickness, edgecolor='black', label=group_categories[1], zorder=3)
				plt.bar(pos3, bars[2], color=bar_group_colors[2], width=self.bar_thickness, edgecolor='black', label=group_categories[2], zorder=3)
				plt.xticks(pos2, labels=self.label_order)
			elif group_size == 4:
				plt.bar(pos1, bars[0], color=bar_group_colors[0], width=self.bar_thickness, edgecolor='black', label=group_categories[0], zorder=3)
				plt.bar(pos2, bars[1], color=bar_group_colors[1], width=self.bar_thickness, edgecolor='black', label=group_categories[1], zorder=3)
				plt.bar(pos3, bars[2], color=bar_group_colors[2], width=self.bar_thickness, edgecolor='black', label=group_categories[2], zorder=3)
				plt.bar(pos4, bars[3], color=bar_group_colors[3], width=self.bar_thickness, edgecolor='black', label=group_categories[3], zorder=3)
				plt.xticks([x+(self.bar_thickness/2) for x in pos2], labels=self.label_order)
			plt.xlabel(self.xlabel)
			plt.ylabel(self.ylabel)

		if self.xlim > 0:
			plt.xlim(self.xlim)
		if self.ylim > 0:
			plt.ylim(self.ylim)

		if self.rotation != 0:
			plt.setp(ax.get_xticklabels(), rotation=self.rotation, ha='right')

		if not(self.title is None):
			plt.title(self.title)

		if self.legend:
			plt.legend(title=self.legend_title, loc=self.legend_loc, ncol=self.legend_cols, fontsize=self.legend_fontsize)

		if self.plot_grid:
			plt.rcParams['axes.axisbelow'] = True
			plt.grid(axis=self.grid_axis, color=self.grid_color, linestyle=self.grid_linstyle, linewidth=self.grid_linewidth, zorder=0)

		if self.tight_layout_flag:
			plt.tight_layout()

		if self.output_path != "Display":
			plt.savefig(self.output_path, bbox_inches="tight")
		plt.show()
		
		return



	def separate_bar_plots(self, dict1, dict2, xlabel1, ylabel1, xlabel2, ylabel2, color1='gray', color2='black',
						   label_order1=None, label_order2=None, plot_text=False):

		self.figsize = (10,9) if self.figsize == (10, 6) else self.figsize
		fig, ((ax1), (ax2)) = plt.subplots(2, 1, figsize=self.figsize)

		if label_order1 is None:
			data1 = dict1
		else:
			data1 = {}
			for label in label_order1:
				data1[label] = dict1[label]
		
		if label_order2 is None:
			data2 = dict2
		else:
			data2 = {}
			for label in label_order2:
				data2[label] = dict2[label]

		if self.rotation == 0:
			alignment = "center"
		else:
			alignment = "right"


		# ##### Sub-Figure 1 #####
		# Save the chart so that bars can be looped through later.
		bars = ax1.bar(x=range(len(data1.keys())), height=list(data1.values()), tick_label=data1.keys(), width=self.bar_thickness, color=color1)

		# Axis formatting:
		ax1.spines['top'].set_visible(False)
		ax1.spines['right'].set_visible(False)
		ax1.spines['left'].set_visible(False)
		ax1.spines['bottom'].set_color('#DDDDDD')
		ax1.tick_params(bottom=False, left=False)
		ax1.set_axisbelow(True)
		ax1.xaxis.grid(False)
		ax1.yaxis.grid(True, color='#EEEEEE')
		
		if plot_text:
			# Grab the color of the bars so we can make the text the same color.
			bar_color = bars[0].get_facecolor()

			# Add text annotations to the top of the bars. Note, you'll have to adjust this slightly (the 0.3) with different data.
			for bar in bars:
				ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, round(bar.get_height(), 1), 
						 horizontalalignment='center', color=bar_color, size=7.5, weight='bold')
		
		ax1.set_xticklabels(labels=data1.keys(), rotation=self.rotation, ha=alignment)
		ax1.set_xlabel(xlabel1)
		ax1.set_ylabel(ylabel1)


		# ##### Sub-Figure 2 #####
		# Save the chart so that bars can be looped through later.
		bars = ax2.bar(x=range(len(data2.keys())), height=list(data2.values()), tick_label=data2.keys(), width=self.bar_thickness, color=color2)

		# Axis formatting:
		ax2.spines['top'].set_visible(False)
		ax2.spines['right'].set_visible(False)
		ax2.spines['left'].set_visible(False)
		ax2.spines['bottom'].set_color('#DDDDDD')
		ax2.tick_params(bottom=False, left=False)
		ax2.set_axisbelow(True)
		ax2.xaxis.grid(False)
		ax2.yaxis.grid(True, color='#EEEEEE')

		if plot_text:
			# Grab the color of the bars so we can make the text the same color.
			bar_color = bars[0].get_facecolor()

			# Add text annotations to the top of the bars. Note, you'll have to adjust this slightly (the 0.3) with different data.
			for bar in bars:
				ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, round(bar.get_height(), 1), 
						 horizontalalignment='center', color=bar_color, size=7.5, weight='bold')
		
		ax2.set_xticklabels(labels=data2.keys(), rotation=self.rotation, ha=alignment)
		ax2.set_xlabel(xlabel2)
		ax2.set_ylabel(ylabel2)

		if self.tight_layout_flag:
			plt.tight_layout()

		if self.output_path != "Display":
			plt.savefig(self.output_path, bbox_inches="tight")
		plt.show()
		
		return



def main():

	sample_data_standard = {"B": 4, "A": 7, "R": 2, "P": 5, "L": 10, "O": 8, "T": 3}

	sample_data_stacked = {"B": {"Used": 4, "Unused": 2}, "A": {"Used": 7, "Unused": 5}, "R": {"Used": 2, "Unused": 1}, "P": {"Used": 5, "Unused": 1}, "L": {"Used": 10, "Unused": 3}, "O": {"Used": 8, "Unused": 6}, "T": {"Used": 3, "Unused": 1}}

	sample_multi_stacked = {"B": {"Used": 4, "Unused": 2, "Unknown": 1}, 
							"A": {"Used": 7, "Unused": 5, "Unknown": 2}, 
							"R": {"Used": 2, "Unused": 1, "Unknown": 3}, 
							"P": {"Used": 5, "Unused": 1, "Unknown": 3}, 
							"L": {"Used": 10, "Unused": 3, "Unknown": 4}, 
							"O": {"Used": 8, "Unused": 6, "Unknown": 2}, 
							"T": {"Used": 3, "Unused": 1, "Unknown": 1}}
	# Dataframe should have 1 col of keys (i.e., barplot labels) and 1 col of stacking categories (i.e., legend labels)
	
	sample_data_grouped = {"B": {"Used": 4, "Unused": 2, "Unknown": 1}, 
						   "A": {"Used": 7, "Unused": 5, "Unknown": 2}, 
						   "R": {"Used": 2, "Unused": 1, "Unknown": 3}, 
						   "P": {"Used": 5, "Unused": 1, "Unknown": 3}, 
						   "L": {"Used": 10, "Unused": 3, "Unknown": 4}, 
						   "O": {"Used": 8, "Unused": 6, "Unknown": 2}, 
						   "T": {"Used": 3, "Unused": 1, "Unknown": 1}}
	# Dataframe should be converted it into the above form and then passed to the function

	sample1 = {"1995": 300, "2000": 200, "2005": 500, "2010": 100, "2015": 250, "2020": 50, "2025": 450}
	sample2 = {"1995": 4, "2000": 7, "2005": 2, "2010": 5, "2015": 10, "2020": 8, "2025": 3}

	
	# BarPlot Class: constructor args
	'''
	data, xlabel, ylabel, output_path=output_path, rotation=rotation, label_order=None,
	legend=False, legend_title=None, legend_location=legend_loc, legend_columns=legend_cols, legend_fontsize=legend_fontsize, bbox_to_anchor=bbox_to_anchor,
	plot_grid=plot_grid, grid_axis=grid_axis, grid_color=grid_color, grid_linstyle=grid_linstyle, grid_linewidth=grid_linewidth,
	figsize=None, color=color, tight_layout_flag=True, title=None, xscale=xscale, yscale=yscale,
	thickness=bar_thickness, xlim=-1, ylim=-1
	'''

	
	# Standard bar plot args
	'''
	df_xcolumn=None, df_ycloumn=None, orientation="vertical" [if data being passed is a dataframe]
	'''
	bar = BarPlot(sample_data_standard, "Categories", "Values", output_path="./sample-bar-plots/sample_standard_bar.pdf")
	bar.standard_bar_plot(orientation="vertical")

	
	# Stacked bar plot args
	'''
	category_column, positive_label, negative_label, orientation="vertical", 
	positive_color="gray", negative_color="black", plot_text=False, bar_alignment="center"
	'''
	bar = BarPlot(sample_data_stacked, "Categories", "Values", output_path="./sample-bar-plots/sample_stacked_bar.pdf", legend=True)
	bar.stacked_bar_plot("Categories", "Used", "Unused", plot_text=True, orientation="vertical")


	# Multi-Stacked or Full-stacked bar plot args
	'''
	stacking_flag=True, normalization_flag=True, orientation="vertical", colorlist=["black", "gray", "silver"]
	'''
	bar = BarPlot(sample_multi_stacked, "Categories", "Distribution", output_path="./sample-bar-plots/sample_multi_full_stacked_bar.pdf", legend=True, legend_columns=3, legend_title="Usage Categories")
	bar.full_or_multi_stacked_bar_plot(orientation="vertical")


	# Grouped bar plot args
	'''
	df_xcolumn=None, df_ycloumn=None, orientation="vertical", bar_group_colors=["black","gray"]
	'''
	bar = BarPlot(sample_multi_stacked, "Categories", "Distribution", output_path="./sample-bar-plots/sample_grouped_bar.pdf", legend=True, legend_title="Usage Categories", legend_location="upper left")
	bar.grouped_bar_plot(orientation="vertical")

	
	# 2 Separate bar charts of similar data in same plot
	'''
	Pass dummy values to constructor for this function
	dict1, dict2, xlabel1, ylabel1, xlabel2, ylabel2, color1='blue', color2='red',
	label_order1=None, label_order2=None, plot_text=False
	'''
	bar = BarPlot(sample1, "Years", "Values", output_path="./sample-bar-plots/sample_separate_bar.pdf")
	bar.separate_bar_plots(sample1, sample2, "Years", "Trend A", "Years", "Trend B")
	
	return



if __name__ == "__main__":

	main()