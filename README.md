# ICC Profiles for SC-P800

This repository contains the patch sets, test charts, measurements and ICC profiles I created for my [Epson SureColor P800 (SC-P800)](docs/P800-brochure.pdf) printer using [X-Rite i1iSis XL](docs/i1iSis-brochure.pdf) automated chart reader using [X-Rite i1Profiler](https://www.xrite.com/categories/formulation-and-quality-assurance-software/i1profiler) and [Argyll CMS](https://www.argyllcms.com/).

The general information here about the printer profiling can be applied to any RGB printer. I do not have any experience with CMYK printers.

# Overview

ICC profile creation steps are:

- creating the patch set
- creating and printing the test chart
- measuring the test chart
- creating the ICC profile

*i1Profiler mentioned below is not a free software. However, creating the patch set and creating the test charts can be used in demo mode. Creating the ICC profile requires a license.*

## Creating the patch set

I create the patch sets using i1Profiler. I save the i1Profiler patch set as iProfiler CGATS .txt file. See [Patch Sets/README.md](Patch%20Sets/README.md) for more info.

## Creating and printing the test chart

I create the test charts (TIF files) using i1Profiler by loading the patch set's txt file. Since I am using X-Rite i1iSis XL Chart Reader, I can use A4, A3 or A3+ test charts. I check and prepare the TIF files using Adobe Photoshop, see [Test Charts/README.md](Test%20Charts/README.md) for more info.

I use ColorSync utility in macOS to print the test charts.

## Measuring the test chart

After the prints are dried, I measure the printed test charts using [X-Rite i1iSis XL Automated Chart Reader](https://xritephoto.com/documents/literature/en/L11-213_iSis_Brochure_en.pdf) in dual scan mode (M0 and M2), using i1Profiler. I save the measurements in i1Profiler CGATS Spectral format, and this creates two files, M0.txt and M2.txt. I usually measure the targets once after ~1h to be sure they can be read by i1iSis, and do the final measurement after 24h.

## Creating the ICC profile

I use [Argyll CMS colprof utility](https://www.argyllcms.com/) utility to create three profiles: one for M0 measurements without FWA compensation, one for M0 measurements with FWA compensation and one for M2 measurements without FWA compensation.

I also use i1Profiler to create the profiles.

# Design of Patch Sets

A patch set can be reused independent of the measuring instrument, the printer and the paper. Hence, there are standard patch sets (like TC9.18). The test chart can also be reused independent of the paper. All the profiling services I have seen also use a single test chart independent of the printer but I think this is not optimal as the test chart they provide may have patches in the reduced quality area of your printer.

The selection of patches to create a printer profile is a complicated topic. There are two main approaches to select the patches:

- using a regular/semi-regular sampling of a color space, and then augmenting this with extra patches (with neutral, near-neutral or particular colors). i1Profiler generates a patch set with this approach. All the standard test charts and test charts of remote ICC profiling services I have seen also uses this approach.

- using a non-regular/random/quasi-random sampling of a color space, and optionally augmenting this with extra patches. targen generates a patch set with this approach.

When using regular/semi-regular sampling, the size of the patch set can only reasonably take particular numbers. If not, some samples will be missing and it is against the idea of regular sampling. On the other hand, when using non-regular sampling, the number of patches can basically be any number. 

Independent of which sampling approach is used, the number of patches practically depend on the capability of the measuring instrument (and the time you have and the money you want to spend on the paper and the ink). If it is an automated reader (or if there is an embedded spectrometer in the printer), a lot of patches can be used. Finally, the actual number of patches then depends on the paper size, how many paper sheets to use and the printer's margin and reduced quality zone specification.

[For RGB Printer Profiling, X-Rite recommends](https://www.xrite.com/service-support/recommended_rgb_printer_profiling_with_i1profiler) using their patch set with 2033 or 1586 patches. Commercial printer profiling services also use something similar, between 1K and 3K patches. I have rarely seen any over 3K.

# File Naming

## Patch Sets

The patch sets starting with `i1_` is created with i1Profiler. The ones starting with `ac_` are created with targen (Argyll CMS). 

i1 patch sets are always scrambled (patch positions are randomized) and the only variable is the number of patches. Thus, the file names are always in the form `i1_XXXX.txt` whereas XXXX is a number (and probably always a 4 digit number).

ac patch sets are also always scrambled (but if requested targen adds the neutral patches to the beginning of the set, so they will be seen in order on the first page). targen has a number of parameters so they can be added to the name, but to keep it simple, I use the form: `ac_XXXX`, where XXXX is probably always a 4 digits number.

The patch sets are independent of the printer, paper or ink used. Hence, the name contains no such information.

## Test Charts

A test chart layout depends on the page size, printer and patch size. Thus, the test chart file name is an extension of the patch set, adding the page size, printer and patch size to that. For example, `i1_2033.txt` patch set might have a test chart base name `i1_2033_A4_P800_6x6` meaning an A4 page on SC-P800 and a patch size of 6x6mm. There is going to be a `.txf` file with this basename, and also one or more `.tif` files for each page of the color charts. When there are multiple pages, the basename also has a suffix `_X_Y` where X is the page number and Y is the total number of pages. For example, for the example before, `i1_2033_A4_P800_6x6_1_2.tif` would be the first page of this two pages color chart. The `.txf` file can be used to load this color chart back to i1Profiler before doing a measurement because the measurement needs to know both the patch set (txf file contains the patch set values) and the layout of color chart.

This repository only contains ICC profiles for SC-P800, but I decided to still keep the printer model in the base name to eliminate confusion.

## Measurements

The measurement is done with a specific paper and actually with a specific ink. However, I consider the ink as part of the printer, so what I mean by P800 is that it is using the original inks (Epson UltraChrome HD). Normally, the layout is not important for the measurement. However, because the same patch set with different layouts can be measured (particularly because of different patch sizes), I use the name of test chart and add the paper and the measurement condition to that. Thus, the measurement file name is `test_chart_basename_PAPER_M0orM2.txt`. For example, `i1_2033_A4_P800_6x6_Epson_Archival_Matte_M0.txt`. Since I always measure in dual scan mode, there are always an M0 and an M2 measurement file.

I do not plan to keep all of the temporary files (measurements after ~1h), but if I do, and also internally, I add the waiting time to the end of the file name, e.g. `i1_2033_P800_Epson_Archival_Matte_M0_2h.txt`. For the final versions, measurements after 24h, I do not add any waiting time suffix.

## Profiles

# Profile Generation

- The manufacturer (-A, Epson) and the model (-M, SC-P800) fields are set.
- The description tag is set to "Epson SC-P800 <MEASUREMENT_CONDITION_M0_or_M2> <FWA_IF_FWA_COMPENSATION_ENABLED> <PAPER>".
- The matte/glossy attribute is set and the default rendering intent is set to relative colorimetric.
- The quality is set to high and algorithm to Lab cLUT (default).
- For one profile generation using M0 measurements, FWA compensation is enabled with -f.
- The illuminant is set to D50 (default) and CIE observer is set to 1931_2 (default).
- For the generation of gamut mapping for the perceptual and saturation rendering intents, AdobeRGB1998 is used as source gamut.
- Monitor in typical work environment (-cmt) for input viewing conditions and Practical Reflection Print (ISO-3664 P2) (-dpp) for output viewing conditions are set.

# Issues To Be Aware Of

## Generating the Test Charts

iProfiler's test chart generation is a bit odd. It has a margin setup but no concept of reduced quality zone. Also, the top part of the test chart before the patches has a larger area than the bottom after the patches. However, the bottom reduced quality zone can be larger than the top for some printers (like SC-P800). So the test chart generated with iProfiler should not be used directly or you should be aware of these issues.

## Printing the Test Charts

Surprisingly printing a test chart (without an extra non-free software) is more difficult than it sounds. The difficulty is the test chart should be printed as it is without any color change/management applied. In the past, it was possible to do this with Adobe Photoshop, however Adobe removed this from Photoshop. A very common and traditional way is to use [Adobe Color Printer Utility](https://helpx.adobe.com/photoshop/kb/no-color-management-option-missing.html). However, ACPU has a scaling problem in Windows (it changes the scale of the test chart) and ACPU is not supported on macOS 10.15 and later. Unfortunately, this makes it not straight-forward to print a test chart on Windows. On macOS, there is a very simple solution. ColorSync utility supports printing test charts.
