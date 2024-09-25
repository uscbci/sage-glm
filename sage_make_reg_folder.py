#!/usr/bin/env python

import os,sys
from subprocess import call

outfolder = "/Volumes/BCI/SAGE/fsl-glm"
scriptdir = os.path.dirname(os.path.realpath(__file__))

subject = sys.argv[1]
print("Making reg folders for %s" % subject)

identity_matrix = "%s/ident.mat" % scriptdir
standard_image = "%s/mask.nii.gz" % scriptdir

for run in range(1,5):

	featfolder = "%s/%s/%s_run0%d.feat" % (outfolder,subject,subject,run)
	regfolder = "%s/reg" % (featfolder)
	if not os.path.exists(regfolder):
		os.mkdir(regfolder)

	command = "cp %s/example_func.nii.gz %s/reg/example_func.nii.gz " % (featfolder,featfolder)
	print(command)
	call(command,shell=True)

	command = "cp %s %s/reg/standard.nii.gz" % (standard_image,featfolder)
	print(command)
	call(command,shell=True)

	command = "cp %s %s/reg/example_func2standard.mat" % (identity_matrix,featfolder)
	print(command)
	call(command,shell=True)

	command = "cp %s %s/reg/standard2example_func.mat" % (identity_matrix,featfolder)
	print(command)
	call(command,shell=True)