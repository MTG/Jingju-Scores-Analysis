# Jingju Singing Analysis

The **Jingju Singing Analysis** code is a collection of tools for extracting statistical and quantitative information from machine readable jingju music scores, having the melodic line as basic analysis unit. It is tailored to be used with the [**Jingju Music Scores Collection** (**JMSC**)](https://doi.org/10.5281/zenodo.1285612), and for the research purposes of the PhD thesis *The musical dimension of
Chinese traditional theatre: An analysis from computer aided musicology* (Caro 2018, see below). The code computes the following information:
- pitch histograms per line,
- pitch histograms per line sections,
- non directed interval histograms,
- directed interval histograms,
- cadential notes,
- melodic density as notes, and
- melodic density as durations.

The results are returned in the form of plots and tables. Each of these information types can be computed for any combination of the jingju music elements covered by the **JMSC**. The instances of these elements that can be input as parameters to the functions included in the code are the following ones (as they should be written when calling a function):
- role type: `laosheng`, `dan`
- *shengqaing*: `erhuang`, `xipi`
- *banshi*: `manban`, `sanyan`, `zhongsanyan`, `kuaisanyan`, `yuanban`, `erliu`, `liushui`, `kuaiban`
- line type: `s` for opening line in *xipi*, `s1` for the long version of the opening line in *erhuang*, `s2` for the short version of the opening line in *erhuang*, `x` for closing line

## Description of the code
The **Jingju Singing Analysis** code is comprised by the following two scripts:
- `jingju_singing_analysis.py` contains a collection of main and auxiliary functions for analysing and browsing the **JMSC**. The five main functions are the ones used for extracting the seven types of information listed above:
 - `pitchHistogram` computes the pitch histograms per line,
 - `pitchHistogramLineJudou` computes the pitch histogrmas per line sections,
 - `intervalHistogram` computes the non directed interval histograms and the directed interval histograms,
 - `cadentialNotes` analyses the cadential notes, and
 - `melodicDensity` analyses the melodic density as notes and the melodic density as durations.


- `JMSC_plots.py` can be run from the terminal in order to reproduce all the plots and tables used in Caro (2018). It can also be used to compute a subset of information types listed above. All these plots and tables are also available in the **plots** folder of this repository.

## Using the code
The **Jingju Singing Analysis** code is written in Python 3.5.2, so for its use it is required a version of Python 3.

Before using the code, the dependencies listed in the requirements.txt file should be installed. This can be done from the terminal (using the package manager pip), by executing the following command from the directory where the requirements.txt file is stored:

    `pip install -r requirements.txt`

Since the code is created to be used with the **JMSC**, the lines_data.csv should be saved in the same folder as the MusicXML scores of the collection.

To use the `JMSC_plots.py` script from the terminal, the following command should be executed from the directory where this script is saved:

    `python JMSC_plots.py PATH\lines_data.csv`

where `PATH` should be the path to the lines_data.csv file.

The `JMSC_plots.py` script offer extra options, in order to select a subsect of information types or specifying a directory for saving the returned plots and tables. For a detailed description of how using the code, including these options, the following command can be executed from the directory where this script is saved:

    `python JMSC_plots.py -h`

For the use of the functions in the `jingju_singing_analysis.py`, a detailed description of each of them is available in their respective docstrings.

## Reference
The Jingju Scores Analysis code is openly available for free use. If you use this code for a published work, please cite the following publication:

- Caro Repetto, Rafael (2018) *The musical dimension of
Chinese traditional theatre: An analysis from computer aided musicology*. PhD thesis, Universitat Pompeu Fabra, Barcelona, Spain.

## Contact
For further questions of comments, please contact Rafael Caro Repetto (rafael.caro@upf.edu)

## License
 The Jingju Singing Analysis code is licensed under the terms of the GNU Affero General Public License (v3 or later).

## Acknowledgements
The creation of this code is funded by the European Research Council under the European Union’s Seventh Framework Program (FP7/2007-2013), as part of the CompMusic project (ERC grant agreement 267583).
