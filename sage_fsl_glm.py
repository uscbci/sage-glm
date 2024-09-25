#!/usr/bin/env python
from subprocess import call
import os, socket
import re

# We are using different parameters on different host computers due to processing power differences etc. 
host = socket.gethostname()
print("Running on host %s" % host)

scriptdir = os.path.dirname(os.path.realpath(__file__))

outfolder = "/Volumes/BCI/SAGE/fsl-glm"
datafolder = "/Volumes/BCI/SAGE/BIDS_data"

donefolders = [fol for fol in os.listdir(outfolder) if ".feat" in fol]
datafolders = [fol for fol in os.listdir(datafolder) if "sub-" in fol]

to_do = []
for subject in datafolders:
    if subject not in donefolders:
        to_do.append(subject)

print("Subjects to do:")
print(to_do)
to_do.sort()

to_do = ["sub-12582"]

template = "sage_glm_template.fsf"
reference =  "%s/standard.nii.gz" % scriptdir
reference = reference.replace("/","\/")


for subject in to_do:
    subject = subject[4:9]
    for run in range(1,5):
        print("Working on run %d" % run)

        #If there's no junk EV we need to set that EV to blank
        junkfile = "/Volumes/BCI/SAGE/fslstimfiles/%s/%s_run%d_junk_all.txt" % (subject,subject,run)
        print ("Checking for junk ev file %s" % junkfile )
        if os.path.exists(junkfile):
            junkevtype = 3
        else:
            junkevtype = 10
        print("Junk EV type is %d" % junkevtype)

        #Create design file for this subject/run
        outfile = "%s/designs/%s-run0%d.fsf" % (outfolder,subject,run)
        print ("Will create %s" % outfile)
        command = "sed -e \'s/DEFINESUBJECT/%s/g\' -e \'s/DEFINERUN/%s/g\' -e \'s/DEFINEREFERENCE/%s/g\' -e \'s/DEFINEJUNKEV/%d/\' %s > %s" % (subject,run,reference,junkevtype,template,outfile)
        print(command)
        call(command, shell=True)
    
        #run feat
        command = "feat %s" % outfile
        print(command)
        call(command, shell=True)
    
    command = "%s/sage_make_reg_folder.py %s" % (scriptdir,subject)

    #Higher level
    template = "sage_glm_template_higherlevel.fsf"
    outfile = "%s/designs/%s.fsf" % (outfolder,subject)
    print ("Will create %s" % outfile)
    command = "sed -e \'s/DEFINESUBJECT/%s/g\' -e \'s/DEFINEREFERENCE/%s/g\' %s > %s" % (subject,reference,template,outfile)
    print(command)
    call(command, shell=True)

    #run feat
    command = "feat %s" % outfile
    print(command)
    call(command, shell=True)