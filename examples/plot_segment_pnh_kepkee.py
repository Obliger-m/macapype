"""
.. _plot_segment_pnh_kepkee:

============================================================
Plot the results of a segmentation with ANTS-based pipeline
============================================================
"""

# Authors: David Meunier <david_meunier_79@hotmail.fr>

# License: BSD (3-clause)
# sphinx_gallery_thumbnail_number = 2
import os
import os.path as op

import json
import pprint

from macapype.utils.utils_tests import load_test_data

##############################################################################
# Testing plot in local
##############################################################################

data_path = load_test_data("data_test_macapype")

wf_path = os.path.join(data_path, "test_NodeParams_KK")

graph = os.path.join(wf_path, "graph.png")

import matplotlib.pyplot as plt  # noqa
img = plt.imread(graph)
plt.figure(figsize=(36, 72))
plt.imshow(img)
plt.axis('off')
plt.show()

##############################################################################
# Data preparation
##############################################################################

###############################################################################
# results of cropping
#===========================

cropped_T1_file = op.join(wf_path, "data_preparation_pipe", "bet_crop", "sub-Apache_ses-01_T1w_cropped.nii.gz")

# displaying results
cropped_T1 = os.path.join(wf_path, "outfile_T1.png")
cmd = "fsleyes render --outfile {} --size 1800 600 {}".format(cropped_T1, cropped_T1_file)
os.system(cmd)

import matplotlib.pyplot as plt  # noqa
img = plt.imread(cropped_T1)
plt.figure(figsize=(36, 12))
plt.imshow(img)
plt.axis('off')
plt.show()

###############################################################################
# results of deoblique
#===========================

## after deoblique
deoblique_T1_file = os.path.join(
    wf_path, "data_preparation_pipe", "deoblique_T1",
    "sub-Apache_ses-01_T1w.nii")

outfile_deoblique = os.path.join(wf_path,"outfile_deoblique.png")
cmd = "fsleyes render --outfile {} --size 1800 600 {} -a 50 {} -a 50".format(outfile_deoblique, cropped_T1_file, deoblique_T1_file)
os.system(cmd)

import matplotlib.pyplot as plt  # noqa
img = plt.imread(outfile_deoblique)
plt.figure(figsize=(8, 8))
plt.imshow(img)
plt.axis('off')
plt.show()

##############################################################################
# First part of the pipeline: brain extraction
##############################################################################

###############################################################################
# Correct bias results
#==========================

debiased_T1_file = op.join(wf_path, "brain_extraction_pipe", "correct_bias_pipe", "restore_T1",
                           "sub-Apache_ses-01_T1w_cropped_noise_corrected_maths.nii.gz")

debiased_T1 = os.path.join(wf_path,"debiased_T1.png")

cmd = "fsleyes render --outfile {} --size 1800 600 {}".format(debiased_T1, debiased_T1_file)
os.system(cmd)

import matplotlib.pyplot as plt  # noqa
fig, axs = plt.subplots(2, 1, figsize=(36, 24))
axs[0].imshow(plt.imread(cropped_T1))
axs[0].axis('off')

axs[1].imshow(plt.imread(debiased_T1))
axs[1].axis('off')
plt.show()

###############################################################################
# Brain extraction results
#==========================

# At the end 1st part pipeline
mask_file = os.path.join(
    wf_path, "brain_extraction_pipe", "extract_pipe", "smooth_mask",
    "sub-Apache_ses-01_T1w_cropped_noise_corrected_maths_brain_bin_bin.nii.gz")

output_img_overlay = os.path.join(wf_path,"outfile_overlay.png")
#cmd = "fsleyes render --outfile {} --size 800 600 {} -ot mask -o -a 50 {}".format(output_img_overlay, mask_file, T1_file)
cmd = "fsleyes render --outfile {} --size 800 600 {} {} -a 50".format(output_img_overlay, cropped_T1_file, mask_file)
os.system(cmd)

import matplotlib.pyplot as plt  # noqa
img = plt.imread(output_img_overlay)
plt.figure(figsize=(36, 12))
plt.imshow(img)
plt.axis('off')
plt.show()

##############################################################################
# Second part of the pipeline: segmentation
##############################################################################

seg_pipe = op.join(wf_path, "brain_segment_from_mask_pipe")

###############################################################################
# debias T1xT2 and debias N4
#=============================

denoised_T1_file = os.path.join(wf_path, "data_preparation_pipe", "denoise_T1",
                           "sub-Apache_ses-01_T1w_cropped_noise_corrected.nii.gz")


denoised_T1 = os.path.join(wf_path,"denoised_T1.png")

cmd = "fsleyes render --outfile {} --size 1800 600 {} -cm Render3".format(denoised_T1, denoised_T1_file)
os.system(cmd)

debiased_mask_T1_file = os.path.join(seg_pipe, "masked_correct_bias_pipe", "restore_mask_T1",
                         "sub-Apache_ses-01_T1w_cropped_noise_corrected_maths_masked.nii.gz")

debiased_mask_T1 = os.path.join(wf_path,"debiased_mask_T1.png")

cmd = "fsleyes render --outfile {} --size 1800 600 {} -cm Render3".format(debiased_mask_T1, debiased_mask_T1_file)
os.system(cmd)


N4_debias_T1_file = os.path.join(seg_pipe, "register_NMT_pipe", "norm_intensity",
                         "sub-Apache_ses-01_T1w_cropped_noise_corrected_maths_masked_corrected.nii.gz")

N4_debias_T1 = os.path.join(wf_path,"N4_debias_T1.png")

cmd = "fsleyes render --outfile {} --size 1800 600 {} -cm Render3".format(N4_debias_T1, N4_debias_T1_file)
os.system(cmd)

import matplotlib.pyplot as plt  # noqa

fig, axs = plt.subplots(3, 1, figsize=(36, 24))
axs[0].imshow(plt.imread(denoised_T1))
axs[0].axis('off')

axs[1].imshow(plt.imread(debiased_mask_T1))
axs[1].axis('off')

axs[2].imshow(plt.imread(N4_debias_T1))
axs[2].axis('off')
plt.show()

###############################################################################
# register template to subject
#==============================

reg_template_mask_to_T1_file = os.path.join(
    seg_pipe, "register_NMT_pipe", "align_NMT",
    "NMT_allineate.nii.gz")

reg_template_mask_to_T1 = os.path.join(wf_path,"reg_template_mask_to_T1.png")


cmd = "fsleyes render --outfile {} --size 1800 600 {} {} -a 50".format(
    reg_template_mask_to_T1, reg_template_mask_to_T1_file, debiased_mask_T1_file)

os.system(cmd)

import matplotlib.pyplot as plt  # noqa
img = plt.imread(reg_template_mask_to_T1)
plt.figure(figsize=(36, 12))
plt.imshow(img)
plt.axis('off')
plt.show()

################################################################################
## segmentation results
##==========================

#tissue_file = os.path.join(seg_pipe, "segment_atropos_pipe", "seg_at", "segment_Segmentation.nii.gz")
#segmentation = os.path.join(wf_path,"segmentation.png")
#cmd = "fsleyes render --outfile {} --size 1800 600 {} {} -dr 0 4 -cm random -a 30".format(segmentation, debiased_mask_T1_file, tissue_file)
#os.system(cmd)

#import matplotlib.pyplot as plt  # noqa
#img = plt.imread(segmentation)
#plt.figure(figsize=(36, 12))
#plt.imshow(img)
#plt.axis('off')
#plt.show()

###############################################################################
# segmentation results by tissue
#================================

csf_file = os.path.join(seg_pipe, "segment_atropos_pipe", "threshold_csf", "segment_SegmentationPosteriors01_thresh.nii.gz")
gm_file = os.path.join(seg_pipe, "segment_atropos_pipe", "threshold_gm", "segment_SegmentationPosteriors02_thresh.nii.gz")
wm_file = os.path.join(seg_pipe, "segment_atropos_pipe", "threshold_wm", "segment_SegmentationPosteriors03_thresh.nii.gz")

segmentation_sep = os.path.join(wf_path,"segmentation_sep.png")
cmd = "fsleyes render --outfile {} --size 1800 600 {} {} -cm red -a 30 {} -cm blue -a 30 {} -cm green -a 30".format(segmentation_sep, debiased_mask_T1_file, gm_file, wm_file, csf_file)
os.system(cmd)

import matplotlib.pyplot as plt  # noqa
img = plt.imread(segmentation_sep)
plt.figure(figsize=(36, 12))
plt.imshow(img)
plt.axis('off')
plt.show()
