# Jingju Tones Analysis

**Jingju Tones Analysis** is a collection of tools for extracting statistical information about the relationship between linguistic tones and melody from machine readable jingju music scores, having the melodic line as basic analysis unit. It is tailored to be used with the [**Jingju Music Scores Collection**](https://doi.org/10.5281/zenodo.1285612) (**JMSC**), and for the research purposes of the PhD thesis *The musical dimension of
Chinese traditional theatre: An analysis from computer aided musicology* (Caro 2018). The code computes information for two relationship types:
- syllabic contour, and
- pairwise relationship, both considering the first note of two consecutive syllables (first-first pairwise relationship), or the last note and the first note of two consecutive syllables (last-first pairwise relationship).

The results are returned in the form of tables. Each of these relationship types can be computed for any combination of the jingju music system elements covered by the **JMSC**. The instances of these elements that can be input as parameters to the functions included in the code are the following ones (as they should be written when calling a function):
- role type: `laosheng`, `dan`
- *shengqaing*: `erhuang`, `xipi`
- *banshi*: `manban`, `sanyan`, `zhongsanyan`, `kuaisanyan`, `yuanban`, `erliu`, `liushui`, `kuaiban`
- line type: `s` for opening line in *xipi*, `s1` for the long version of the opening line in *erhuang*, `s2` for the short version of the opening line in *erhuang*, `x` for closing line

## Description of the code
The **Jingju Tones Analysis** code is comprised by the following three scripts:
- `jingju_tones_analysis.py` contains a collection of main and auxiliary functions for analysing the **JMSC**. The two main functions are the ones used for extracting information about the relationship types listed above:
    - `syllabicContour` computes information about the syllabic contour, and
    - `pairwiseRelationship` computes information for either the first-first pairwise relationship or the last-first pairwise relationship.


- `jTA_syllabic_contour.py` can be run with a single command line from the terminal in order to reproduce the results shown in Table 12 in Caro (2018). It can also be used to call the `syllabicContour` function with customized inputs.
- `jTA_pairwise_relationship.py` can be run with a single command line from the terminal in order to reproduce the results shown in either Table 13 or Table 14 in Caro (2018). It can also be used to call the `pairwiseRelationship` function with customized inputs.

The **results** folder contains the results returned by `jTA_syllabic_contour.py` and `jTA_pairwise_relationship.py` as applied to the whole **JMSC** and presented in Tables 12, 13, and 14 in Caro (2018).

## Using the code
The **Jingju Tones Analysis** code is written in Python 3.5.2, so for its use it is required a version of Python 3.

Before using the code, the dependencies listed in the requirements.txt file should be installed. This can be done from the terminal (using the package manager pip), by executing the following command from the directory where the requirements.txt file is stored:

    pip install -r requirements.txt

Since the code is created to be used with the **JMSC**, the lines_data.csv should be stored in the same folder as the MusicXML scores of the collection.

To use the `jTA_syllabic_contour.py` script from the terminal, the following command should be executed from the directory where this script is saved:

    python jTA_syllabic_contour.py PATH

where `PATH` is the path to the directory where the MusicXML scores and the lines_data.csv file are stored.

The `jTA_syllabic_contour.py` script offers extra options. For a detailed description of how using the code, including these options, the following command can be executed from the directory where this script is saved:

    python jTA_syllabic_contour.py -h

The `jTA_pairwise_relationship.py` script can be used for computing either first-first or last-first pairwise relationships from the terminal. In order to compute the first-first pairwise relationship, the following command should be executed from the directory where this script is saved:

    python jTA_pairwise_relationship.py PATH 0 0

In order to compute the last-first pairwise relationship, the following command should be executed from the directory where this script is saved:

    python jTA_pairwise_relationship.py PATH 1 0

In both cases, `PATH` is the path to directory where the MusicXML scores and the lines_data.csv file are stored.

The `jTA_pairwise_relationship.py` script also offers extra options. For a detailed description of how using the code, including these options, the following command can be executed from the directory where this script is saved:

    python jTA_pairwise_relationship.py -h

For the use of the functions in the `jingju_tones_analysis.py`, a detailed description of each of them is available in their respective docstrings.

## Reference
The **Jingju Tones Analysis** code is openly available for free use. If you use this code for a published work, please cite the following publication:

- Caro Repetto, Rafael (2018) *The musical dimension of
Chinese traditional theatre: An analysis from computer aided musicology*. PhD thesis, Universitat Pompeu Fabra, Barcelona, Spain.

## Contact
For further questions of comments, please contact Rafael Caro Repetto (rafael.caro@upf.edu)

## License
 The **Jingju Tones Analysis** code is licensed under the terms of the GNU Affero General Public License (v3 or later).

## Acknowledgements
The creation of this code is funded by the European Research Council under the European Union’s Seventh Framework Program (FP7/2007-2013), as part of the CompMusic project (ERC grant agreement 267583).
