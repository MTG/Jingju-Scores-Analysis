# Jingju Singing Analysis Plots

These plots present statistical information about singing lines in arias of the **Jingju Music Scores collection**. Each of the files in this folder contain plots for different combinations of *hangdang* (role type), *shengqiang*, *banshi* and *ju* (line type). The specific combination is specified in the title of each plot. If no specification for a particular element is given, it means that all instances have been considered. The list of all instances per element (with the abbreviations used in plots' titles in brackes) is:
- **_hangdang_**: *laosheng*, *dan*
- **_shengqiang_**: *erhuang*, *xipi*
- **_banshi_**: *manban* (mb), *sanyan* (sy), *zhongsanyan* (zsy), *kuaisanyan* (ksy), *yuanban* (yb), *erliu* (el), *liushui* (ls), *kuaiban* (kb)
- **_ju_**: opening line (ol, only in *xipi*), opening line type 1 (ol1, only in *erhuang*), opening line type 2 (ol2, only in *erhuang*), closing line (cl)

Each file contains plots computed as follows:

- **jSA_pitch_histograms.pdf**: contains plots computed using **jSA_pitch_histogram.py** for each of the combinations in the plots' titles. The optional arguments (count and gracenotes) are left to their default values.

- **jSA_interval_histograms_not_directed.pdf**: contains plots computed using **jSA_interval_histogram.py** for each of the combinations in the plots' titles. The optional arguments (count, directed, silence, and gracenotes) are left to their default values.

- **jSA_interval_histograms_directed.pdf**: contains plots computed using **jSA_interval_histogram.py** for each of the combinations in the plots' titles. The optional argument directed is set to 'True', and the rest (count, silence, and gracenotes) are left to their default values.

- **jSA_cadential_notes.pdf**: contains plots computed using **jSA_cadential_notes.py** for each of the combinations in the plots' titles. The optional argument gracenotes is left to its default value.

- **jSA_melodic_density_duration**: contains plots computed using **jSA_melodic_density.py** for each of the combinations in the plots' titles. The optional arguments (gracenotes and duration) are left to their default values.

- **jSA_melodic_density_notes.pdf**: contains plots computed using **jSA_melodic_density.py** for each of the combinations in the plots' titles. The optional argument duration is set to 'notes', and the other one (gracenotes) is left to its default value.

Selected plots from these files have been presented and discussed in

- R. Caro Repetto and X. Serra (2017) "A collection of music scores for corpus based jingju singing research," *Proc. of the 18th International Society for Music Information Retrieval*, Suzhou, China
