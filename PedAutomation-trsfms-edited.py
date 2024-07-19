# PYTHON script
import os
import ansa
import csv
from ansa import constants 
from ansa.base import PedSafety as ps
from ansa.base import GetEntity as ge
from ansa.base import GetEntityCardValues as gecv


deck = constants.PAMCRASH
ext_id = 2000003
head_id = 2000005
head_coord1 = 9902
ws_id = 2000004
bonnet_id = 9
bumper_id = 14
grnd_1 = (0, 0, -186)
app_reg = "EUPHASE_2"
test_type = "HEADFORM"


def main():
	print("Emil's Pedestrian Crash Automation Script V1-2022\n******************************************\n\n")
	tobe_compressed = ['GRID', 'ELEMENT', 'EDGE', 'GEOMETRY']
	ansa.base.Compress(tobe_compressed)
	print('Entities Compressed\n')
	
	to_del = []
	target_entities = ansa.base.CollectEntities(deck, None, 'TARGET_POINT')
	if target_entities:	
		for ent in target_entities:
			to_del.append(ent)
	#print(to_del)
	ansa.base.DeleteEntity(to_del, True)
	
	ext_parts = ge(deck, 'GROUP', ext_id)
	head = ge(deck, 'GROUP', head_id)
	windscreen = ge(deck, 'GROUP', ws_id)
	coord = ge(deck, 'FRAME_3NODES_IAXIS_1', head_coord1)
	bonnet = ge(deck, 'GROUP', bonnet_id)
	trsfm_group = ge(deck, 'GROUP', 28)
	head_include = ge(deck, 'INCLUDE', 12)
	
	print('external set name: ' + str(ext_parts._name))
	print('head set name: ' + str(head._name))
	print('head coord set name: ' + str(coord._name))
	print('')
	
#	DB = ansa.base.CollectEntities(deck, search_types = '__ALL_ENTITIES__')
#	for i in DB:
#		print(i)
	
	### Deleting Previously created Geometry ------------------------------------------------
	curves = ansa.base.CollectEntities(deck, None, 'CURVE')
	if curves:
		ansa.base.DeleteEntity(curves, True)
		print('curves deleted: ' + str(len(curves)))
	else:
		print('no curves to delete\n')
		
	
	points = ansa.base.CollectEntities(deck, None, 'POINT')
	if points:
		ansa.base.DeleteEntity(points, True)
		print('points deleted: ' + str(len(points)))
	else:
		print('no points to delete\n')

### Deleting existing head shell elements -----------------------------------------------------
	shell_entities = ansa.base.CollectEntities(deck, None, 'PART_SHELL')
	shell_entities_partids=[]
	shal = ['IMAT', 'Name']
	for i in range(len(shell_entities)):
		if gecv(deck = deck, entity = shell_entities[i], fields = shal):
			shell_entities_partids.append(gecv(deck = deck, entity = shell_entities[i], fields = shal))
		else:
			shell_entities.pop(i)
	counter = 0
	shells_to_del = []
	if shell_entities_partids:
		for i, part in enumerate(shell_entities_partids):
			if part['Name'] == "RBRL_Spheres_Property":
				shells_to_del.append(shell_entities[i])
				counter+=1
		ansa.base.DeleteEntity(shells_to_del, True)					
		print('Shell entities deleted: ' + str(counter))
	
	### Defining the pedsafety class, marking and rasterizing-----------------------------------------------------------------------------------------------------------------------------
	ped_obj = ps(external_parts=ext_parts,windscreen = windscreen, device=head, ground_1 = grnd_1, device_type='HEADFORM', raster_zone = "CHILD", raster_length=100, apply_reg=app_reg, coord_sys=coord)
	target_points = ped_obj.mark()
	ped_obj.create_raster()
	
	### deleting adults
	target_entities = ansa.base.CollectEntities(deck, None, 'TARGET_POINT')
	if target_entities:	
		for ent in target_entities:
			#print(ent._name)
			if ent._name[0]=='A':
				to_del.append(ent)
	#print(to_del)
	ansa.base.DeleteEntity(to_del, True)
		
		
	### Collecting Target Point data--------------------------------------------------------------------
	target_entities = ansa.base.CollectEntities(deck, None, 'TARGET_POINT')
	ent_count = len(target_entities)
	print('\nnumber of target points:')
	print(ent_count)
	val = ('__id__','Name','X','Y','Z', 'IMPACT ANGLE','MOVE BACK','SUBTYPE') 
	cards = [0]*ent_count
	target_xyz = [0]*ent_count
	impact_angle = [0]*ent_count
	move_back = [0]*ent_count
	positioning_type = [0]*ent_count
	positioned = [0]*ent_count
	Trans = [0]*ent_count
	transform = [0]*ent_count
	
	### Deleting existing transformations-----------------------------------------------------------
	trsfm_entities = ansa.base.CollectEntities(deck, None, 'TRSFM')
	to_del = []
	if trsfm_entities:	
		ansa.base.DeleteEntity(trsfm_entities, True)
		print('trsfms deleted: ' + str(len(trsfm_entities)))
	else:
		print('no trsfms to delete')

	### Positioning---------------------------------------------------------------------------------------------------
	for i, pnt in enumerate(target_entities):
		cards[i] = gecv(deck = deck, entity = pnt, fields = val)
		target_xyz[i] = (cards[i]['X'], cards[i]['Y'], cards[i]['Z'])
		impact_angle[i] = cards[i]['IMPACT ANGLE'] 
		move_back[i] = cards[i]['MOVE BACK'] 
		positioning_type[i] = cards[i]['SUBTYPE'] 
		Trans[i] = ped_obj.position(target_xyz=target_xyz[i], impact_angle=50, move_back=5, positioning_type='TARGET', get_all_contact_points=False, undo=True)
		print('head positioned at target point ' + str(pnt._id))
		transform[i] = ansa.base.TransformCreate(str(pnt._id), head_include)
		valsm1 = {"deck": deck, "type": "Move", "Tx":1, "Ty":0, "Tz":0, "Distance": Trans[i][10]}
		valsm2 = {"deck": deck, "type": "Move", "Tx":0, "Ty":1, "Tz":0, "Distance": Trans[i][11]}
		valsm3 = {"deck": deck, "type": "Move", "Tx":0, "Ty":0, "Tz":1, "Distance": Trans[i][12]}
		valsR = {"deck":deck, "type":"Rotate", 'Ry':1.0, "Angle":130}
		ansa.base.TransformInsertLine(transform[i], valsm1, 0)
		ansa.base.TransformInsertLine(transform[i], valsm2, 0)
		ansa.base.TransformInsertLine(transform[i], valsm3, 0)
		#ansa.base.TransformInsertLine(transform[i], valsR, 0)	
	
		
	### Checking Transformations-----------------------------------------------------------------------------------
	trsfm_info = {}
	#trsfm_entities = ansa.base.CollectEntities(deck, None, 'TRSFM')
	vals = ['id', 'name', 'entity', 'matrix', ]
	#trsfm_info = ansa.base.TransformInfo(trsfm_entities[0], vals)
	#print(trsfm_info)
	
#	print('\nTransformations:')
#	print(Trans)

	with open("Transformations.csv", 'w', encoding='utf-8', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(Trans)
		print('csv written\n')
		
	#print(ansa.base.TransformInfo(transform[0], 'matrix'))	
	trsfms_all = ansa.base.CollectEntities(deck, None, "TRSFM")
	print(trsfms_all)
	for i, t in enumerate(trsfms_all):	
		outres = ansa.base.OutputPamCrash(filename='D:/pedestrian/trsfms/trsfm' + str(i) +'.pc', mbcontainer = t, mode="costum_mbcontainer")
	
if __name__ == '__main__':
	main()


