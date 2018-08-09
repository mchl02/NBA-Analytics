
# coding: utf-8

# In[26]:


get_ipython().magic(u'matplotlib inline')

import numpy as np
import jinja2
import os
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from nba_py import shotchart, player
from matplotlib.patches import Circle, Rectangle, Arc
import json
from six.moves import urllib
from matplotlib.offsetbox import  OffsetImage
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
from PIL import Image


# In[2]:


os.chdir('/home/matt/ShotCharts') 


# In[3]:


def draw_court(ax=None, color='black', lw=2, outer_lines=False):
	# If an axes object isn't provided to plot onto, just get current one
	if ax is None:
	    ax = plt.gca()

	# Create the various parts of an NBA basketball court

	# Create the basketball hoop
	# Diameter of a hoop is 18" so it has a radius of 9", which is a value
	# 7.5 in our coordinate system
	hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

	# Create backboard
	backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

	# The paint
	# Create the outer box 0f the paint, width=16ft, height=19ft
	outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
	                      fill=False)
	# Create the inner box of the paint, widt=12ft, height=19ft
	inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
	                      fill=False)

	# Create free throw top arc
	top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
	                     linewidth=lw, color=color, fill=False)
	# Create free throw bottom arc
	bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
	                        linewidth=lw, color=color, linestyle='dashed')
	# Restricted Zone, it is an arc with 4ft radius from center of the hoop
	restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
	                 color=color)

	# Three point line
	# Create the side 3pt lines, they are 14ft long before they begin to arc
	corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
	                           color=color)
	corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
	# 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
	# I just played around with the theta values until they lined up with the 
	# threes
	three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
	                color=color)

	# Center Court
	center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
	                       linewidth=lw, color=color)
	center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
	                       linewidth=lw, color=color)

	# List of the court elements to be plotted onto the axes
	court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
	                  bottom_free_throw, restricted, corner_three_a,
	                  corner_three_b, three_arc, center_outer_arc,
	                  center_inner_arc]

	if outer_lines:
	    # Draw the half court line, baseline and side out bound lines
	    outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
	                            color=color, fill=False)
	    court_elements.append(outer_lines)

	# Add the court elements onto the axes
	for element in court_elements:
	    ax.add_patch(element)

	return ax


# In[4]:


def get_players():
	players = player.PlayerList()
	players_df = players.info()
	players_data = {}
	for index, row in players_df.iterrows():
		players_data[row['DISPLAY_FIRST_LAST']] = row['PERSON_ID']
	player_file = open('players.json','w')
	player_file.write(json.dumps(players_data))
	player_file.close()

def load_players():
	player_file = open('players.json','r')
	return json.load(player_file)


# In[5]:


player_data = load_players()


# In[53]:



def player_shots(player_id, season = '2017-18'):
	russ = shotchart.ShotChart(player_id=player_id, season=season)
	shot_df = russ.shot_chart()
	player_name = shot_df['PLAYER_NAME'][0]
	sns.set_style("white")
	sns.set_color_codes()
	pic = urllib.request.urlretrieve("https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/1610612747/2017/260x190/1628366.png")
	harden_pic = plt.imread(pic[0])
    
	fig = plt.figure(figsize=(12,11))
	plt.scatter(shot_df.LOC_X, shot_df.LOC_Y, c = 'gold', marker = 'h', alpha = 0.5)
	draw_court()
	# Adjust plot limits to just fit in half court
	plt.xlim(-250,250)
	# Descending values along th y axis from bottom to top
	# in order to place the hoop by the top of plot
	plt.ylim(422.5, -47.5)
	# get rid of axis tick labels
	# plt.tick_params(labelbottom=False, labelleft=False)
	plt.title(player_name+' FGA - '+season, y=1.01, fontsize=18)

	img = OffsetImage(harden_pic, zoom=0.6)
	img.set_offset((556,55))
	ax = plt.gca()
	ax.add_artist(img)
	ax.set_xlabel('')
	ax.set_ylabel('')
	plt.show()
#	canvas=FigureCanvas(fig)
#	png_output = BytesIO()
#	canvas.print_png(png_output)
#	response=make_response(png_output.getvalue())
#	response.headers['Content-Type'] = 'image/png'
#	return response
	#return render_template("index.html")def player_shots(player_id, season = '2016-17'):
	season = '2017-18'  
	russ = shotchart.ShotChart(player_id=player_id, season=season)
	shot_df = russ.shot_chart()
	player_name = shot_df['PLAYER_NAME'][0]
	sns.set_style("white")
	sns.set_color_codes()
	pic = urllib.request.urlretrieve("")
	harden_pic = Image.open('bald.png')
	harden_pic = harden_pic.resize((260,190))

	harden_pic = np.asarray(harden_pic)
	fig = plt.figure(figsize=(12,11))
	plt.scatter(shot_df.LOC_X, shot_df.LOC_Y, c = 'purple', marker = 'h', alpha = 0.5)
	draw_court()
	# Adjust plot limits to just fit in half court
	plt.xlim(-250,250)
	# Descending values along th y axis from bottom to top
	# in order to place the hoop by the top of plot
	plt.ylim(422.5, -47.5)
	# get rid of axis tick labels
	# plt.tick_params(labelbottom=False, labelleft=False)
	plt.title('Baldzo Ball'+' FGA - '+season, y=1.01, fontsize=18)

	img = OffsetImage(harden_pic, zoom=0.6)
	img.set_offset((550,55))
	ax = plt.gca()
	ax.add_artist(img)
	ax.set_xlabel('')
	ax.set_ylabel('')
	plt.show()
#	canvas=FigureCanvas(fig)
#	png_output = BytesIO()
#	canvas.print_png(png_output)
#	response=make_response(png_output.getvalue())
#	response.headers['Content-Type'] = 'image/png'
#	return response
	#return render_template("index.html")


# In[54]:


player_shots("1628366")

