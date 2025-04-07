# ICC Profiles for SC-P800

This repository contains ICC profiles I created for Epson SureColor P800 (SC-P800) Printer.

# Overview

ICC profile creation steps are: creating the patch set, creating and printing the test chart, measuring the test chart and creating the ICC profile.

- I create the patch sets using [Argyll CMS targen utility](https://www.argyllcms.com/). I typically use a number of patches to fully cover 2x A4 pages. This creates a patchset.ti1 file. Since I am using X-Rite i1iSis XL Chart Reader, I can use A3 or A3+ test charts, which is actually a very good thing since A3 can have more patches than 2x A4 and it can be read at one session but I am mostly using A4 papers.

- I use [my scaleti1rgb utility](scaleti1rgb.py) to scale the RGB values in ti1 file from 0-100 (what targen generates) to 0-255 (what i1Profiler expects). This creates a patchset.txt file. I guided ChatGPT to write this utility.

- I create the test charts (TIF files) using [X-Rite i1Profiler](https://www.xrite.com/categories/formulation-and-quality-assurance-software/i1profiler) by loading patchset.txt. i1Profiler is not a free software, but this feature can be freely used.

- I use ColorSync utility in macOS to print the test charts.

- After the prints are dried, I measure the printed test charts using [X-Rite i1iSis XL Automated Chart Reader](https://xritephoto.com/documents/literature/en/L11-213_iSis_Brochure_en.pdf) in dual scan mode (M0 and M2), using i1Profiler (this feature can also be used freely). The measurements are saved as i1Profiler CGATS files, M0.txt and M2.txt. I usually measure the targets after ~1h to be sure they can be read by i1iSis, and do a final measurement after minimum 24h.

- I use [Argyll CMS colprof utility](https://www.argyllcms.com/) utility to create three profiles: one for M0 measurements, one for M0 measurements with FWA compensation and one for M2 measurements.

# Patchset and Test Chart Design

There are different patch sets, standard or generated on the fly. Main parameters are:

- does it regularly sample the RGB cube (e.g. take a value every X step), or does it randomly sample (e.g. OFPS in argyllcms)
- how many white and black patches
- how many neutral (gray) patches
- how many near-neutral (gray) patches

The simple targets use small a small patchset, including regular sampling with only one or two white and black patches and maybe a few neutral patches. More advanced targets use a large patchset, including regular or random sampling, with more white and black and many more neutral patches. With regular sampling, for example iProfiler at the moment, also creates many near-netural patches.

As far as I can see, the standard test charts and iProfiler uses regular sampling whereas argyllcms (by default) uses random sampling. More information about random sampling can be found at [Adaptive color-printer modeling using regularized linear splines, Don Bone, 1993.](https://sci-hub.se/10.1117/12.149033) and [Improved output device characterisation test charts, Graeme W. Gill, 2004](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/12/1/art00036).

It says "the ... technique (MAMAS) is described and tested using simulations. With measurement noise level, delta, much less than the desired accuracy, alpha, the technique proves to have significant advantages over regular sampling approaches.".

Creating a test chart (e.g. TIF image) from a patchset is straight-forward but might not be very easy. printtarg utility in Argyll CMS.
 
I created a (Google) sheet to find maximum number of patches that can be laid on a single paper considering all variables including the printer parameters such as margins and reduced quality areas, the paper size and the i1iSis chart specifications. Using the minumums in chart specifications (which corresponds to tight margin setting in i1Profiler and 6x6mm patch size), 1020 patches fit to a single A4 page. This considers the reduced quality areas of the printer (patches are not laid out there)

# Printing the Test Chart

Surprisingly printing a test chart sounds simple but difficult to do in practice. The idea is that, because the profiling software needs to know the exact values of the colors in a test chart that is sent to the printer, the colors of the test chart (TIF, PS, PDF etc.) should not be modified at all, neither by the application software, nor by the operating system, nor by the printer driver. The last in the chain, the printer driver, is the easiest, you can just select no color management. However, the application software and the operating system interaction is not well documented, particularly in Windows. Many companies use and recommend [Adobe Color Printer Utility](https://helpx.adobe.com/photoshop/kb/no-color-management-option-missing.html) but this utility is not supported well enough. It has a scaling problem in Windows and macOS 10.15 is not supported. I think at the moment the only free option is to use ColorSync utility in macOS.

# Details

## targen

I use 2040 patches to fill two A4 pages, including:

- 8 white patches (-e)
- 8 black patches (-B)
- 256 gray patches (-g)
- 2040 total OFPS (full spread) patches (-f)

```
targen -v -d2 -G -e8 -B8 -g256 -f2040 patchset2040
```

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
