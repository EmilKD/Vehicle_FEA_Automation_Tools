# Automatic curve data extractor for beta software meta by Emil Keshishian
# To use this script in meta, open the script editor and open this file then enter the path to the folder in which the
# Files will be extracted.

import os
import meta 
from meta import plot2d as p2d

def main():
	os.chdir("Path to your fav folder")

################################################
	with open("Curve_Coords.txt", 'w') as f:
		plts = p2d.ActivePlots()
		crvs = p2d.Curves()
	
		max_coords = []
		filtered_pnts = []
		maxys = []
		maxy = 0
		maxx = 0
		flag = 1
		flagR = 1
		
		for plt in plts:
			print(plt.id, plt.window_name, plt.page_id, plt.active, plt.type)
			window_name = plt.window_name
			plot_id = plt.id
			plot_axes = p2d.PlotAxesOfPlot(window_name, plot_id)
			print('\n')
			
		
		for i,c in enumerate(crvs):
			window_name = c.window_name
			cid = c.id
			maxp = p2d.MaxPointYOfCurve(window_name, cid, "real")
			xrange = [2.5, 18]
			yrange = [0, maxp.y]
			
			fpnts = p2d.FilterPointsOfCurve(window_name, cid, xrange[0], xrange[1], yrange[0], yrange[1])
			filtered_pnts.append(fpnts)
			
			for p in fpnts:
				if maxy<p.y:
					maxy = p.y
				if maxx<p.x:
					maxx = p.x
					
			maxys.append(maxy)
			x,y = maxp.x, maxp.y
			if flag == 1:
				f.write("\nMaximum Global Values: \n")
				flag = 0
			f.write(str(cid) + ' ' + str(c.name) + ' ' + str(x) + ",	" + str(y) +"\n")
			max_coords.append([x, y])		
			
			if flagR == 1:
				f.write("\nMaximum Ranged Values: \n")
				flagR = 0	
			f.write(str(cid) + ' ' + str(c.name) + ' ' + str(window_name) + ' ' + str(maxx) + ",	" + str(maxy) +"\n")
			maxy = 0
			maxx = 0
			
			#print(type(p2d.FilterPointsOfCurve(window_name, cid, xrange[0], xrange[1], yrange[0], yrange[1])))
			#print(filtered_pnts[i])
		
		print('\nGlobal Maximum Values:')
		print(max_coords)	
		print("\nRanged Maximum Values:")
		print(maxys)
		print("\n")
#################################################
if __name__ == '__main__':
	main()


