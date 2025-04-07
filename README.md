# ICC Profiles for SC-P800

This repository contains ICC profiles I created for Epson SureColor P800 (SC-P800) Printer.

# Overview

ICC profile creation steps are: creating the patch set, creating and printing the test chart, measuring the test chart and creating the ICC profile.

*i1Profiler is not a free software, but the features I am using below can be used freely in demo mode.*

- I create the patchsets either using [Argyll CMS](https://www.argyllcms.com/) [targen](https://www.argyllcms.com/doc/targen.html) utility or [X-Rite i1Profiler](https://www.xrite.com/categories/formulation-and-quality-assurance-software/i1profiler). targen creates a patchset.ti1 file and I save the i1Profiler's patchset to a patchset.txt file. If I use targen, then I also use my [scaleti1rgb utility](scaleti1rgb.py) to scale the RGB values in ti1 file from 0-100 (what targen generates) to 0-255 (what i1Profiler expects). This converts the ti1 file to a txt file, patchset.txt. I guided ChatGPT to write this utility.

- I create the test charts (TIF files) using i1Profiler by loading patchset.txt. Since I am using X-Rite i1iSis XL Chart Reader, I can use A4, A3 or A3+ test charts. After creating the test chart, I check the TIF files in Adobe Photoshop to be sure it fits to a corresponding page (within margins) and also the patches are outside of reduced quality area of the printer. i1Profiler has no feature to specify this, so it has to be done manually.

- I use ColorSync utility in macOS to print the test charts.

- After the prints are dried, I measure the printed test charts using [X-Rite i1iSis XL Automated Chart Reader](https://xritephoto.com/documents/literature/en/L11-213_iSis_Brochure_en.pdf) in dual scan mode (M0 and M2), using i1Profiler. I save the measurements in i1Profiler CGATS Spectral format, and this creates two files, M0.txt and M2.txt. I usually measure the targets once after ~1h to be sure they can be read by i1iSis, and do the final measurement after 24h.

- I use [Argyll CMS colprof utility](https://www.argyllcms.com/) utility to create three profiles: one for M0 measurements without FWA compensation, one for M0 measurements with FWA compensation and one for M2 measurements without FWA compensation.

# File Naming

There is going to be a lot of similar files in this repository, so the file naming rules are important. I list them here.

## Patch Sets

The patch sets (ti1 and/or txt) starting with `i1_` is created with i1Profiler, whereas the ones starting with `ac_` are created with targen (Argyll CMS). 

i1 patch sets are always scrambled (patch positions are randomized) and the only variable is the number of patches. Thus, the file names are always in the form `i1_XXXX.txt` whereas XXXX is a number (and probably always a 4 digit number).

ac patch sets are also always scrambled but targen adds the gray patches to the beginning of the set, so they will be seen in order on the first page. The variables are the number of white, black, gray and the total number of patches. I always keep the number of white patches equal to black patches. Thus, the file names are always in the form `ac_wbXX_gYYY_ZZZZ`. XX, YYY and ZZZZ are numbers, whereas XX can be one or two digits, YYY can be two or three digits and ZZZZ is probably always 4 digits.

The patch sets are independent of the printer, paper or ink used. Hence, the name contains no such information.

I generated a few patch sets to reuse. 

- The default patch set in the current i1Profiler (3.8.4) (when Advanced > Printer > Profiling is opened) has 2033 patches. The scrambled (randomized) set is [i1_2033.txt](). Its patches are semi-regularly sampled including neutral and near-neutral patches.

[i3_2033 image]

- With Argyll CMS, I created a few different patch sets.

, for 1x, 2x and 3x A4 pages, 1x A3 page and 1x A3+ page. For 1x A4, I generated a few alternatives with different number of gray patches.

| name | # of white (-e) | # of black (-B) | # of gray (-g) | total # of patches (-f) | pages |
| ---- | --------------- | --------------- | -------------- | ----------------------- | ----- |
| ac_wb4_g32_1020   |  4 |  4 |  32 | 1020 | 1x A4 |
| ac_wb4_g64_1020   |  4 |  4 |  64 | 1020 | 1x A4 |
| ac_wb8_g128_2040  |  8 |  8 | 128 | 2040 | 2x A4 |
| ac_wb16_g256_3060 | 16 | 16 | 256 | 3060 | 3x A4 |
| ac_wb16_g256_2420 | 16 | 16 | 256 | 2420 | 1x A3 |
| ac_wb16_g256_3185 | 16 | 16 | 256 | 3185 | 1x A3+ |


| name | # of white (-e) | # of black (-B) | # of gray (-g) | total # of patches (-f) | pages |
|---|---|---|---|---|
| ac_wb4_g32_1020   |  4 |  4 |  32 | 1020 | 1x A4 |
| ac_wb4_g64_1020   |  4 |  4 |  64 | 1020 | 1x A4 |
| ac_wb8_g128_2040  |  8 |  8 | 128 | 2040 | 2x A4 |
| ac_wb16_g256_3060 | 16 | 16 | 256 | 3060 | 3x A4 |
| ac_wb16_g256_2420 | 16 | 16 | 256 | 2420 | 1x A3 |
| ac_wb16_g256_3185 | 16 | 16 | 256 | 3185 | 1x A3+ |

## Test Charts

The test chart is created in iProfiler by setting up:

- i1iSis XL as device and enabling tight margins
- A4, A3 or A3+ as page size, portrait page orientation and test chart margins as the minimum margins of the printer (3mm on all sides for SC-P800)
- patch width and height as required, header length always 32mm

Thus, a test chart layout depends on the page size, printer and patch size. The test chart file name is an extension of the patch set, adding the page size, printer and patch size to that. For example, `i1_2033.txt` patch set might have a test chart base name `i1_2033_A4_P800_6x6` meaning an A4 page on SC-P800 and a patch size of 6x6mm. There is going to be a `.txf` file with this basename, and also one or more `.tif` files for each page of the color charts. When there are multiple pages, the basename also has a suffix `_X_Y` where X is the page number and Y is the total number of pages. For example, for the example before, `i1_2033_A4_P800_6x6_1_2.tif` would be the first page of this two pages color chart. The `.txf` file can be used to load this color chart back to i1Profiler before doing a measurement because the measurement needs to know both the patch set (txf file contains the patch set values) and the layout of color chart.

i1Profiler by default adds the base name of the test chart to the test chart itself. It is double check. It is also possible to add layout information a barcode that can be automatically read by i1iSis but I am not using this feature.

This repository only contains ICC profiles for SC-P800, but I decided to still keep the printer model in the base name to eliminate confusion.

## Measurements

The measurement is done with a specific paper and actually with a specific ink. However, I consider the ink as part of the printer, so what I mean by P800 is that it is using the original inks (Epson UltraChrome HD). Also, the layout is not important for the measurement. It already contains information about the patch set but to easily understand the connection I extend the patch set name. Thus, the measurement file name is `patch_set_basename_PRINTER_PAPER_M0orM2.txt`. For example, `i1_2033_P800_Epson_Archival_Matte_M0.txt`. Since I always measure in dual scan mode, there are always an M0 and an M2 measurement file.

I do not plan to keep all of the temporary files (measurements after ~1h), but if I do, and also internally, I add this to the end of the file name, e.g. `i1_2033_P800_Epson_Archival_Matte_M0_2h.txt` for a measurement after I did after 2h. For the final versions, measurements after 24h, I do not add any suffix.

## Profiles

# Details

## targen



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
