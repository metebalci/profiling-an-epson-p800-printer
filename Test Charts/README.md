# Test Charts

The test charts are created in iProfiler by setting up:

- i1iSis XL as device and enabling tight margins
- A4, A3 or A3+ as page size, portrait page orientation and test chart margins as the minimum margins of the printer (3mm on all sides for SC-P800)
- patch width and height as required, header length always 32mm

After creating a test chart, I open the TIF files in Adobe Photoshop and change the canvas height (keeping the current canvas on top center) to the height of the page minus top and bottom margin (e.g. 291 mm for A4 and 414 mm for A3). Then, I check if the patches are outside of the reduced quality area of the printer (for P800 it is 33mm on top and 38mm on bottom). This is a must to do because ColorSync centers the image when printing and i1Profiler has no such features to automatically do all these, so it has to be done unfortunately manually.

i1Profiler by default adds the base name of the test chart to the test chart (header). It is a double check. It is also possible to add layout information a barcode that can be automatically read by i1iSis but I am not using this feature.
