# ICC Profiles for SC-P800

This repository contains ICC profiles I created for Epson SureColor P800 (SC-P800) Printer.

# Overview

ICC profile creation steps are: creating the patch set, creating and printing the test chart, measuring the test chart and creating the ICC profile.

- I create the patchsets using [Argyll CMS targen utility](https://www.argyllcms.com/). This creates a patchset.ti1 file. 

- I use [my scaleti1rgb utility](scaleti1rgb.py) to scale the RGB values in ti1 file from 0-100 (what targen generates) to 0-255 (what i1Profiler expects). This creates a patchset.txt file. I guided ChatGPT to write this utility.

- I create the test charts (TIF files) using [X-Rite i1Profiler](https://www.xrite.com/categories/formulation-and-quality-assurance-software/i1profiler) by loading patchset.txt. i1Profiler is not a free software, but this feature can be freely used. Since I am using X-Rite i1iSis XL Chart Reader, I can use A3 or A3+ test charts, which is actually a very good thing since A3 can have more patches than 2x A4 and it can be read at one session but I am mostly using A4 papers.

- I use ColorSync utility in macOS to print the test charts.

- After the prints are dried, I measure the printed test charts using [X-Rite i1iSis XL Automated Chart Reader](https://xritephoto.com/documents/literature/en/L11-213_iSis_Brochure_en.pdf) in dual scan mode (M0 and M2), using i1Profiler (this feature can also be used freely). The measurements are saved as i1Profiler CGATS files, M0.txt and M2.txt. I usually measure the targets after ~1h to be sure they can be read by i1iSis, and do a final measurement after minimum 24h.

- I use [Argyll CMS colprof utility](https://www.argyllcms.com/) utility to create three profiles: one for M0 measurements, one for M0 measurements with FWA compensation and one for M2 measurements.

# Patchset and Test Chart Design

A patchset ideally includes enough number of important colors that samples the printer/ink/paper behavior to create an ICC profile. For example, the following points matter:

- how many white and black patches. Because white and black are extra important, the measurement error should be minimized.
- how many neutral (gray) patches. Because creating gray levels from color inks can be problematic.
- is near-neutral (gray) patches needed ? if so, how many. Because near-neutral colors are important in real photographs.
- how the remaining patches are selected/sampled, and how many.

At the moment all patchsets used for ICC profile creation include a different numbers of white, black and neutral patches. Some new patchsets also include extra near-neutral patches particularly if the other patches are regularly sampled. The main question is how the remaining patches are selected and how many of them are required.

The problem is also complicated by the fact that it is not possible to have a lot of patches since they have to be printed (consumes paper and ink) and measured (takes time). For a home user, or a proconsumer, this means A4 or A3 papers (A4 can contain ~1000 patches), and a simple spectrometer to measure the charts manually. For a professional or commercial business, this means larger papers, automated chart readers (~5K USD) and/or printers with embedded spectrometers (starts from ~5K USD).

Many ICC profiling services use 1K or 2K patches (and rarely 4-5K). I can see for example the profile of Hahnemuhle Matt Fibre has 936 measurements (TC9.18 standard color target with 18 extra white patches). It is usually recommended to use between 1-2K patches, or 2-3K patches when creating high quality ICC profiles.

For the remaining patches, there are two main methods. One is to regularly sample the RGB cube. This means to sample for example every 16th point in the cube, that is 16 points in each direction (RGB), thus 16x16x16=4096 points in total. The other method is to randomly sample the RGB cube but iteratively change the samples so the distance between them are similar. The first method is used by everything I saw until now, both the standard test charts and the ones created by a software like i1Profiler. The second method is used only by Argyll CMS.

The simple targets use small a small patchset, including regular sampling with only one or two white and black patches and maybe a few neutral patches. More advanced targets use a large patchset, including regular or random sampling, with more white and black and many more neutral patches. With regular sampling, for example iProfiler at the moment, also creates many near-netural patches.

As far as I can see, the standard test charts and iProfiler uses regular sampling whereas argyllcms (by default) uses random sampling. More information about random sampling can be found at [Adaptive color-printer modeling using regularized linear splines, Don Bone, 1993.](https://sci-hub.se/10.1117/12.149033) and [Improved output device characterisation test charts, Graeme W. Gill, 2004](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/12/1/art00036).

It says "the ... technique (MAMAS) is described and tested using simulations. With measurement noise level, delta, much less than the desired accuracy, alpha, the technique proves to have significant advantages over regular sampling approaches.".

Creating a test chart (e.g. TIF image) from a patchset is straight-forward but might not be very easy. printtarg utility in Argyll CMS.
 
I created a (Google) sheet to find maximum number of patches that can be laid on a single paper considering all variables including the printer parameters such as margins and reduced quality areas, the paper size and the i1iSis chart specifications. Using the minumums in chart specifications (which corresponds to tight margin setting in i1Profiler and 6x6mm patch size), 1020 patches fit to a single A4 page. This considers the reduced quality areas of the printer (patches are not laid out there)

## Patchsets of Standard Color Charts

- TC9.18: 1 white, 1 black,

# Printing the Test Chart

Surprisingly printing a test chart sounds simple but difficult to do in practice. The idea is that, because the profiling software needs to know the exact values of the colors in a test chart that is sent to the printer, the colors of the test chart (TIF, PS, PDF etc.) should not be modified at all, neither by the application software, nor by the operating system, nor by the printer driver. The last in the chain, the printer driver, is the easiest, you can just select no color management. However, the application software and the operating system interaction is not well documented, particularly in Windows. Many companies use and recommend [Adobe Color Printer Utility](https://helpx.adobe.com/photoshop/kb/no-color-management-option-missing.html) but this utility is not supported well enough. It has a scaling problem in Windows and macOS 10.15 is not supported. I think at the moment the only free option is to use ColorSync utility in macOS.

# Details

## targen

I generated a few different patchsets, for 1x, 2x and 3x A4 pages, 1x A3 page and 1x A3+ page. For 1x A4, I generated a few alternatives with different number of gray patches.

| name | # of white (-e) | # of black (-B) | # of gray (-g) | total # of patches (-f) | pages |
|---|---|---|---|---|
| patchset_wb4_g32_1020   |  4 |  4 |  32 | 1020 | 1x A4 |
| patchset_wb4_g64_1020   |  4 |  4 |  64 | 1020 | 1x A4 |
| patchset_wb8_g128_2040  |  8 |  8 | 128 | 2040 | 2x A4 |
| patchset_wb16_g256_3060 | 16 | 16 | 256 | 3060 | 3x A4 |
| patchset_wb16_g256_2420 | 16 | 16 | 256 | 2420 | 1x A3 |
| patchset_wb16_g256_3185 | 16 | 16 | 256 | 3185 | 1x A3+ |

## iProfiler

patchset2040 fits to two A4 pages, this is based on my calculation.

In i1Profiler (advanced, printer profiling workflow), I set the options to the parameters in my calculation (and select tight margins) and the test chart is generated as I expected.

## colprof

- The manufacturer (-A, Epson) and the model (-M, SC-P800) fields are set.
- The description tag is set to "Epson SC-P800 <MEASUREMENT_CONDITION_M0_or_M2> <FWA_IF_FWA_COMPENSATION_ENABLED> <PAPER>".
- The matte/glossy attribute is set and the default rendering intent is set to relative colorimetric.
- The quality is set to high and algorithm to Lab cLUT (default).
- For one profile generation using M0 measurements, FWA compensation is enabled with -f.
- The illuminant is set to D50 (default) and CIE observer is set to 1931_2 (default).
- For the generation of gamut mapping for the perceptual and saturation rendering intents, AdobeRGB1998 is used as source gamut.
- Monitor in typical work environment (-cmt) for input viewing conditions and Practical Reflection Print (ISO-3664 P2) (-dpp) for output viewing conditions are set.
