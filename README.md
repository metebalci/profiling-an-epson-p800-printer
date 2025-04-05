# ICC Profiles for SC-P800

This repository contains ICC profiles I created for Epson SureColor P800 (SC-P800) Printer.

I follow the following procedure:

- I create the color targets using [Argyll CMS targen utility](https://www.argyllcms.com/). I typically use enough patches to cover 4x A4 pages.

- I use [my scaleti1rgb utility](scaleti1rgb.py) to scale the RGB values in ti1 file from 0-100 to 0-255. This creates a patchset.txt file. This utility is written by ChatGPT.

- I create the TIF targets using [X-Rite iProfiler](https://www.xrite.com/categories/formulation-and-quality-assurance-software/i1profiler) by loading patchset.txt. I set the margin to printer's minimum margin values for top and sides (3mm) and use minimum patch size of 9mm width (50% larger than minimum 6mm for i1iSis) and 6.6mm height (10% larger than minimum 6mm for i1iSis). Because the bottom reduced quality area is slightly (33mm vs. 38mm) larger than the top, I increase the bottom margin value to 6mm. The header length is the default value of 32mm. Depending on how the actual patches are layout on the pages, I increase the size of the patch while still fitting them to the same number of pages.

- I print the TIF targets using [Adobe Photoshop](https://en.wikipedia.org/wiki/Adobe_Photoshop) by setting Printer manages color, disabling color management in the printer driver and setting top-left offset to 0.

- After the prints are dried, I measure them using [X-Rite i1iSis XL](https://xritephoto.com/documents/literature/en/L11-213_iSis_Brochure_en.pdf) in dual mode, with both M0 and M2 illuminants. The measurements are saved as iProfiler CGATS files, M0.txt and M2.txt. I usually measure the targets after ~1h to be sure they can be read by i1iSis, and do a final measurement after minimum 24h.

- I use [Argyll CMS colprof utility](https://www.argyllcms.com/) utility to create three profiles: one for M0 measurements, one for M0 measurements with FWA compensation and one for M2 measurements.

# Details

## targen

For A4, I use:

- 2508 OPFS patches (-f)
- 16 white patches (-e)
- 16 black patches (-B)
- 256 gray patches (-g)

```
targen -v -d2 -G -e16 -B16 -g256 -f2508 -w -W patchset2508
```

## iProfiler

For patchset2508 layout on 4x A4 pages, I use 9.2mm x 6.6mm patches.

## colprof

- The manufacturer (-A, Epson) and the model (-M, SC-P800) fields are set.
- The description tag is set to "Epson SC-P800 <MEASUREMENT_CONDITION_M0_or_M2> <FWA_IF_FWA_COMPENSATION_ENABLED> <PAPER>".
- The matte/glossy attribute is set and the default rendering intent is set to relative colorimetric.
- The quality is set to high and algorithm to Lab cLUT (default).
- For one profile generation using M0 measurements, FWA compensation is enabled with -f.
- The illuminant is set to D50 (default) and CIE observer is set to 1931_2 (default).
- For the generation of gamut mapping for the perceptual and saturation rendering intents, AdobeRGB1998 is used as source gamut.
- Monitor in typical work environment (-cmt) for input viewing conditions and Practical Reflection Print (ISO-3664 P2) (-dpp) for output viewing conditions are set.
