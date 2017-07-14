# Jingju Singing Analysis

**Jingju Singing Analysis** is a collection of tools for extracting statistical information about singing lines in arias of the **Jingju Music Scores collection**. In order to research the building elements of jingju musical system, the extracted information can be restricted to any combination of the *hangdang* (role type), *shengqiang*, *banshi* and *ju* (line type) contained in the scores collection:
- **_hangdang_**: *laosheng*, *dan*
- **_shengqiang_**: *erhuang*, *xipi*
- **_banshi_**: *manban*, *sanyan*, *zhongsanyan*, *kuaisanyan*, *yuanban*, *erliu*, *liushui*, *kuaiban*
- **_ju_**: s (opening line in *xipi*), s1 (type 1 of opening line in *erhuang*), s2 (type 2 of opening line in *erhuang*), x (closing line)

The code is written in **Python 3.5.2** and using the [**music21** toolkit](http://web.mit.edu/music21/).

These tools are designed to work with the MusicXML scores from the **Jingju Music Scores collection v.x.x.x**. The lines_data.csv file, containing annotations for these scores, should be in the same folder as the MusicXML scores. This collection is available on demand for research purposes contacting the authors.

The **plots** folder contains a series of plots obtained as an exploratory analysis of the **Jingju Music Scores collection** using the Jingju Singing Analysis tools.

The code and some of results contained in the **plots** folder are presented and discussed in

- R. Caro Repetto and X. Serra (2017) "A collection of music scores for corpus based jingju singing research," *Proc. of the 18th International Society for Music Information Retrieval*, Suzhou, China

## Description of the scripts

- **jingju_singing_analysis.py**: collection of functions for extracting several features from the Jingju Music Scores collection. Please refer to the documentation inside the code for further details.

- **jSA_pitch_histogram.py**: creates a PNG file containing a pitch histogram for the given combination of jingju musical system elements. The script can be run from the command line. For more detailed information and further options, please refer to the help documentation in the code (`>python jSA_pitch_histogram.py -h`)

- **jSA_interval_histogram.py**: creates a PNG file containing an interval histogram for the given combination of jingju musical system elements. The script can be run from the command line. For more detailed information and further options, please refer to the help documentation in the code (`>python jSA_interval_histogram.py -h`)

- **jSA_cadential_notes.py**: creates a PNG file containing a bar chart with the percentage of cadential notes for each section of the opening and closing lines from the given combination of jingju musical system elements. The script can be run from the command line. For more detailed information and further options, please refer to the help documentation in the code (`>python jSA_cadential_notes.py -h`)

- **jSA_melodic_density.py**: creates a PNG file containing a boxplot for each score that matches the given combination of jingju musical system elements, plus one boxplot for the all these scores aggregated. The script can be run from the command line. For more detailed information and further options, please refer to the help documentation in the code (`>python jSA_melodic_density.py -h`)

## Contact
Rafael Caro Repetto (rafael.caro@upf.edu)

## License
 The Jingju Singing Analysis code is licensed under the terms of the GNU Affero General Public License (v3 or later).

## Acknowledgements
The creation of this code is funded by the European Research Council under the European Union’s Seventh Framework Program (FP7/2007-2013), as part of the CompMusic project (ERC grant agreement 267583).
