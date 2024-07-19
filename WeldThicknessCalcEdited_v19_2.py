# PYTHON script
import os
import ansa
import csv
from ansa import constants 
from ansa.base import PedSafety as ps
from ansa.base import GetEntity as ge
from ansa.base import GetEntityCardValues as gecv

deck = constants.PAMCRASH
ids=[]
welds = []
sums = []
weld_ids = []
shell_ids=[]
temp = []
val = [0]*5

def main():	
	weld_thicks = []
	thicks=[]
	sum=0
	plinks = ansa.base.CollectEntities(deck, None, 'PLINK')
	if plinks:
		vals = ['NLAYER'] 
		part_vals = ['PART1', 'PART2', 'PART3', 'PART4', 'PART5']
		for link in plinks:
			layers = gecv(deck, link, vals)['NLAYER']
			if layers>2:
				link_part_ids = gecv(deck, link, part_vals)
				#print(link_part_ids)
				temp = list(link_part_ids.values())
				val[0] = temp[2]
				val[1] = temp[1]
				val[2] = temp[0]
				val[3] = temp[4]
				val[4] = temp[3]
				#print(val)
				ids.append(val[0:layers])
				weld_ids.append(link._id)
		print(ids)
		shell_ents = ansa.base.CollectEntities(deck, None, 'PART_SHELL')
		for ent in shell_ents:
			h = gecv(deck, ent, 'h')
			shell_ids.append(ent._id)
			welds.append(h['h'])
		for link in ids:
			for id in link:
				index = shell_ids.index(id)
				sum = sum + welds[index]
				thicks.append(welds[index])
			sums.append(sum)
			weld_thicks.append(thicks)
			thicks=[]
			sum=0
		print(weld_thicks)
		
		with open('./thicknesses.txt', 'w') as f:
			for r,i in enumerate(sums):
				if i>2.5:	
					print(weld_ids[r])
					f.write('id: ' + str(weld_ids[r]) + '\n')
					print(i)
					f.write('thickness: '+ str(i)+'\n')
					print(max(weld_thicks[r]))
					f.write('ratio: ' + str(max(weld_thicks[r])/min(weld_thicks[r])) + '\n\n')
					print('\n')
			print(os.getcwd())
if __name__=='__main__':
	main()