# ICC Profiles for SC-P800

This repository contains ICC profiles I created for Epson SureColor P800 (SC-P800) Printer.

# Overview

- I create the patch sets using [Argyll CMS targen utility](https://www.argyllcms.com/). I typically use enough patches to cover 2x A4 pages. This creates a patchset.ti1 file. Since I am using X-Rite i1iSis XL Chart Reader, I can use A3 or A3+ test charts, but I am mostly using A4 papers.

- I use [my scaleti1rgb utility](scaleti1rgb.py) to scale the RGB values in ti1 file from 0-100 (what targen generates) to 0-255 (what i1Profiler expects). This creates a patchset.txt file. I guided ChatGPT to write this utility.

- I create the test charts (TIF files) using [X-Rite i1Profiler](https://www.xrite.com/categories/formulation-and-quality-assurance-software/i1profiler) by loading patchset.txt. i1Profiler is not a free software, but this feature can be freely used.

- I print the TIF test charts using Color Sync Utility on macOS.

- After the prints are dried, I measure the printed test charts using [X-Rite i1iSis XL Automated Chart Reader](https://xritephoto.com/documents/literature/en/L11-213_iSis_Brochure_en.pdf) in dual scan mode (M0 and M2), using i1Profiler (this feature can also be used freely). The measurements are saved as i1Profiler CGATS files, M0.txt and M2.txt. I usually measure the targets after ~1h to be sure they can be read by i1iSis, and do a final measurement after minimum 24h.

- I use [Argyll CMS colprof utility](https://www.argyllcms.com/) utility to create three profiles: one for M0 measurements, one for M0 measurements with FWA compensation and one for M2 measurements.

# Patchset and Test Chart Design

There are different patch sets, standard or generated on the fly. Main parameters are:

- does it regularly sample the RGB cube (e.g. take a value every X step), or does it randomly sample (e.g. OFPS in argyllcms)
- how many white and black patches
- how many neutral (gray) patches
- how many near-neutral (gray) patches

The simple targets use small a small patchset, including regular sampling with only one or two white and black patches and maybe a few neutral patches. More advanced targets use a large patchset, including regular or random sampling, with more white and black and many more neutral patches. With regular sampling, for example iProfiler at the moment, also creates many near-netural patches.

As far as I can see, argyllcms is the only software using random sampling and the idea comes from [Adaptive color-printer modeling using regularized linear splines, Don Bone, 1993.](https://sci-hub.se/10.1117/12.149033). It says "the ... technique (MAMAS) is described and tested using simulations. With measurement noise level, delta, much less than the desired accuracy, alpha, the technique proves to have significant advantages over regular sampling approaches.". 
 
I created a (Google) sheet to find maximum number of patches that can be laid on a single paper considering all variables including the printer parameters such as margins and reduced quality areas, the paper size and the i1iSis chart specifications. Using the minumums in chart specifications (which corresponds to tight margin setting in i1Profiler and 6x6mm patch size), 1020 patches fit to a single A4 page. This considers the reduced quality areas of the printer (patches are not laid out there)

# Printing the Test Chart

# Details

## targen

For A4, I use:

- 8 white patches (-e)
- 8 black patches (-B)
- 256 gray patches (-g)
- 2040 total OFPS (full spread) patches (-f)

```
targen -v -d2 -G -e8 -B8 -g256 -f2040 patchset2040
```

## iProfiler

For patchset2852 layout on 4x A4 pages, I use 7.5mm x 6.6mm patches. 

In iProfiler (advanced, printer profiling workflow), I set the test chart margins to printer's minimum margin values for top and sides (3mm) and try to find a slightly larger (>10%) than minimum patch size (6mm x 6mm for i1iSis). Because the bottom reduced quality area is slightly (33mm vs. 38mm) larger than the top (and the footer area of the test chart is smaller than the header), I set the bottom margin value to 12mm. The header length is the default value of 32mm. Depending on how the actual patches are layout on the pages, I try to find reasonable numbers, this is a manual, trial-and-error process.

## colprof

- The manufacturer (-A, Epson) and the model (-M, SC-P800) fields are set.
- The description tag is set to "Epson SC-P800 <MEASUREMENT_CONDITION_M0_or_M2> <FWA_IF_FWA_COMPENSATION_ENABLED> <PAPER>".
- The matte/glossy attribute is set and the default rendering intent is set to relative colorimetric.
- The quality is set to high and algorithm to Lab cLUT (default).
- For one profile generation using M0 measurements, FWA compensation is enabled with -f.
- The illuminant is set to D50 (default) and CIE observer is set to 1931_2 (default).
- For the generation of gamut mapping for the perceptual and saturation rendering intents, AdobeRGB1998 is used as source gamut.
- Monitor in typical work environment (-cmt) for input viewing conditions and Practical Reflection Print (ISO-3664 P2) (-dpp) for output viewing conditions are set.
