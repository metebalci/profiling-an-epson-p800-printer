WORK-IN-PROGRESS

# Profiling an Epson P800 Printer

This repository contains the code and the data for my blog post: [Profiling an Epson P800 Printer](https://metebalci.com/blog/profiling-an-epson-p800-printer/).

This repository contains the patch sets, test charts, measurements and ICC profiles I created for [Epson SureColor P800 (SC-P800)](docs/P800-brochure.pdf) printer using [X-Rite i1iSis XL](docs/i1iSis-brochure.pdf) automated chart reader using [X-Rite i1Profiler](https://www.xrite.com/categories/formulation-and-quality-assurance-software/i1profiler) and [Argyll CMS](https://www.argyllcms.com/).

This repository also contains the script:

- [ti1totxt.py](scripts/ti1totxt.py): scales the RGB values (0-100) in targen's ti1 files to 0-255 which is expected by X-Rite's i1Profiler. If `-r` option is given, it also randomizes (scrambles) the patch locations (and save the original input with .bak extension)

# License

Profiling an Epson P800 Printer Blog Post and Repository © 2025 by Mete Balci is licensed under CC BY-NC-SA 4.0. To view a copy of this license, visit [https://creativecommons.org/licenses/by-nc-sa/4.0/](https://creativecommons.org/licenses/by-nc-sa/4.0/).
