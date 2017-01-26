# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/roopireddy/.spyder2/.temp.py
"""

#!/usr/bin/python

#import sys
import os

ca3caxonalvoxelslistpath = "/home/roopireddy/Hipp3DProj/Data/AxonalVoxels/CA3c/"
ca3baxonalvoxelslistpath = "/home/roopireddy/Hipp3DProj/Data/AxonalVoxels/CA3b/"
ca3axonalvoxelslistpath = "/home/roopireddy/Hipp3DProj/Data/AxonalVoxels/CA3a/"

pcstplaneslicespath="/home/roopireddy/Hipp3DProj/Data/Normals_Sorted_STPlaneSlices/PC/"
hippvoxeldbfile="/home/roopireddy/Hipp3DProj/Data/VoxelDB/hippocampus-voxeldb.txt"

hippvoxelList = []
PCVoxelList = []
hippmappedVoxels = []


class hippVoxel(object):
    def __init__(self, index, x, y, z, stpos, transpos, bregma, lamda, dv, type):
        self.index = index
        self.x = x
        self.y = y
        self.z = z
        self.stpos = stpos
        self.transpos = transpos
        self.bregma = bregma
        self.lamda = lamda
        self.dv = dv
        self.type = type
    
class PCVoxel(object):
    def __init__(self, voxelindex, x, y, z):
        self.voxelindex = voxelindex
        self.x = x
        self.y = y
        self.z = z
        
def load_PCVoxels(filenumber):
    #returns all the pc voxels in a list
    stplanesnormalfile=pcstplaneslicespath + "pcvoxels_normalsonplane_" + (filenumber) + ".txt"
    values = []
    PCVoxelList[:] = []
    with open(stplanesnormalfile) as input_file:
        for line in input_file:
            for number in line.split():
                values.append(number)
            PCVoxelObj = PCVoxel(values[0], values[1], values[2], values[3])
            PCVoxelList.append(PCVoxelObj)
            values[:] = []    
        input_file.close()        
    
def list_files(path):
    # returns a list of names (with extension, without full path) of all files 
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files 
    
def read_axonalvoxels(filename):
    values = []
    voxelindices = []
    with open(filename) as input_file:
        for line in input_file:
            for number in line.split():
                values.append(number)
            voxelindices.append(values[0])
            values[:] = []
        input_file.close()
    return voxelindices            

def getXYZCoords(voxelindex):
    coords = []
    for PCVoxelObj in PCVoxelList:
        if(voxelindex == PCVoxelObj.voxelindex):
            coords.append(PCVoxelObj.x)
            coords.append(PCVoxelObj.y)
            coords.append(PCVoxelObj.z)
            return coords

def matchHippVoxelDB(coords):
    #print coords
    #print len(hippvoxelList)
    for hippVoxelObj in hippvoxelList:
        if(abs(float(coords[0])-float(hippVoxelObj.x)) < 0.001):
            if(abs(float(coords[1])-float(hippVoxelObj.y)) < 0.001):
                if(abs(float(coords[2])-float(hippVoxelObj.z)) < 0.001):
                   return hippVoxelObj                                                                    

def mapVoxels(filenumber, voxelindices):
    #read stplanenormalfile
    load_PCVoxels(filenumber)
    #print len(PCVoxelList)
    for voxelindex in voxelindices:
        coords = getXYZCoords(voxelindex)
        #print coords
        hippVoxel = matchHippVoxelDB(coords)
        #print hippVoxel.index
        hippmappedVoxels.append(hippVoxel)
                        
def extract_mappedvoxels(filenames):
    #print len(filenames)
    file = filenames[0]
    
    for file in filenames:
        print file
        filenumberdot = file.split("_")
    #print filenumberdot
        filenumber = filenumberdot[2].split(".")
    #print filenumber
    #extract filenumber
        voxelindexfilename = ca3axonalvoxelslistpath + file
    #print voxelindexfilename
        voxelindices = read_axonalvoxels(voxelindexfilename)
        #print voxelindices
        mapVoxels(filenumber[0], voxelindices)
    write_file("ca3a")
    #write hippvoxelindex to file

def write_file(filetype):
    if(filetype == "ca3a"):
        filename = "/home/roopireddy/Hipp3DProj/Data/AxonalVoxels/ca3aaxonalvoxels.txt"
    output_file = open(filename, 'w')
    for mapppedvoxel in hippmappedVoxels:
        outputstr = str(mapppedvoxel.index) + " " + str(mapppedvoxel.x) + " " + str(mapppedvoxel.y) + " " + str(mapppedvoxel.z)
        outputstr =  outputstr + " " + str(mapppedvoxel.stpos) + " " + str(mapppedvoxel.transpos) + " " + str(mapppedvoxel.bregma) + " " 
        outputstr = outputstr +  str(mapppedvoxel.lamda) + " " + str(mapppedvoxel.dv) + " " + str(mapppedvoxel.type) + "\n"  
                    
        output_file.write(outputstr)
        #output_file.write(mapppedvoxel.index, mapppedvoxel.x, mapppedvoxel.y, mapppedvoxel.z, mapppedvoxel.stpos, 
         #                 mapppedvoxel.transpos, mapppedvoxel.bregma, mapppedvoxel.lamda, mapppedvoxel.dv, mapppedvoxel.type)
    
    
def start_process(filepath):
    axonalfiles = sort(list_files(filepath))
    #print axonalfiles
    extract_mappedvoxels(axonalfiles)    

def load_hippvoxels():
    hippvoxeldbfile="/home/roopireddy/Hipp3DProj/Data/VoxelDB/hippocampus-voxeldb.txt"
    print hippvoxeldbfile
    values = []
    index = 1
    with open(hippvoxeldbfile) as input_file:
        for line in input_file:
            #print line
            #line = line.split()
            for number in line.split():
                #yield float(number)
                values.append(number)
            if int(values[8]) > 60 and int(values[8]) < 82:
                #print index
                hippVoxelObj = hippVoxel(index, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8])
                hippvoxelList.append(hippVoxelObj)
            values[:] = []
            index += 1
        input_file.close()    
    return

def get_ca3pvvoxels():
	
        
load_hippvoxels()
#print len(hippvoxelList)
#start_process(ca3axonalvoxelslistpath)
#print ca3caxonalvoxels
