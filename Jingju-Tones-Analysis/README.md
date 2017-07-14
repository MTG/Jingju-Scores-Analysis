# Jingju Tones Analysis

**Jingju Tones Analysis** is a collection of tools for extracting statistical information about the relationship between linguistic tones and melody in arias of the **Jingju Music Scores collection**. In order to research the building elements of jingju musical system, the extracted information can be restricted to any combination of the *hangdang* (role type), *shengqiang*, *banshi* and *ju* (line type) contained in the scores collection:
- **_hangdang_**: *laosheng*, *dan*
- **_shengqiang_**: *erhuang*, *xipi*
- **_banshi_**: *manban*, *sanyan*, *zhongsanyan*, *kuaisanyan*, *yuanban*, *erliu*, *liushui*, *kuaiban*
- **_ju_**: s (opening line in *xipi*), s1 (type 1 of opening line in *erhuang*), s2 (type 2 of opening line in *erhuang*), x (closing line)

The code is written in **Python 3.5.2** and using the [**music21** toolkit](http://web.mit.edu/music21/).

These tools are designed to work with the MusicXML scores from the **Jingju Music Scores collection v.x.x.x**. The lines_data.csv file, containing annotations for these scores, should be in the same folder as the MusicXML scores. This collection is available on demand for research purposes contacting the authors.

The code and the obtained results are presented and discussed in

- R. Caro Repetto, S. Zhang, and X. Serra (2017) "Quantitative analysis of the relationship between linguistic tones and melody in jingju using music scores," *Proc. of the 4th International Digital Libraries for Musicology workshop*, Shanghai, China [submitted]

## Description of the scripts

- **jingju_tones_analysis.py**: collection of functions for extracting statistical information about syllabic contours and pairwise relationships from the **Jingju Music Scores collection**. Please refer to the documentation inside the code for further details.

- **jTA_syllabic_contour.py**: Prints a table with the count of the different syllabic contours per tone category, excluding tone 5. Results are given in absolute numbers, percentage, and percentage excluding the syllabic contour dL. The script can be run from the command line. For more detailed information and further options, please refer to the help documentation in the code (`>python jTA_syllabic_contour.py -h`)

- **jTA_pairwise_relationship.py**: Prints a table with the count of the different directions per pairwise relationship between two consecutive syllables. The results are given in absolute numbers and percentage. The script can be run from the command line. For more detailed information and further options, please refer to the help documentation in the code (`>python jTA_pairwise_relationship.py -h`)

## Contact
Rafael Caro Repetto (rafael.caro@upf.edu)

## License
 The Jingju Tones Analysis code is licensed under the terms of the GNU Affero General Public License (v3 or later).

## Acknowledgements
The creation of this code is funded by the European Research Council under the European Union’s Seventh Framework Program (FP7/2007-2013), as part of the CompMusic project (ERC grant agreement 267583).
