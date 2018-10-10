# -*- coding: utf-8 -*-



# Jingju Singing Analysis is a collection of tools for the statistical analysis
# of the singing melody in jingju music scores.
#
# Copyright (C) 2017 Music Technology Group, Universitat Pompeu Fabra
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



import numpy as np
import sys
import matplotlib.pyplot as plt
from music21 import *
import fractions



###############################################################################
## FUNCTIONS FOR GATHERING MATERIAL                                          ##
###############################################################################

def collectLineMaterial(linesData,
                        hangdang=['laosheng', 'dan'],
                        shengqiang=['erhuang', 'xipi'],
                        banshi=['manban', 'sanyan', 'zhongsanyan',
                                  'kuaisanyan', 'yuanban', 'erliu', 'liushui',
                                  'kuaiban'],
                        judou=['s', 's1', 's2', 'x']):
    '''
    Given the path to the lines_data.csv file, that should be stored in the
    same folder as the MusicXML scores of the Jingju Music Scores Collection,
    it returns information for accessing all the lines that meet the input
    criteria. If for any of the input instances no line is retrieved, a warning
    message indicates so.
    
    Paramenters:
    - linesData -- str, path to the lines_data.csv file
    - hangdang -- [str], list of role types
    - shengqiang -- [str], list of shengqiang
    - banshi -- [str], list of banshi
    - judou -- [str], list of line types
    
    It returns a list with the following elements:
    - a dictionary with the instances of each element for which a line is
          retrived. The keys are 'hd' for role type, 'sq' for shengqiang, 'bs'
          for banshi, and 'ju' for line type. Values are lists of strings
    - a series of lists for the scores from which lines are retrived. Each of
          these lists contains the following information
          - the path to the MusicXML file of the given score
          - a list for each of the vocal parts contained in the score. Each of
                these lists includes a list of two floats representing the
                starting and ending offset of a retrived line that part from
                that score
    
    For example:
    
    >>> collectLineMaterial('path-to-lines_data.csv', hangdang=['dan'], shengqi
        ang=['xipi'], banshi=['erliu'])

    Retrieving lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    [{'bs': ['erliu'], 'hd': ['dan'], 'ju': ['s', 'x'], 'sq': ['xipi']},
     ['../../Jingju-Music-Scores/MusicXML scores/daxp-ChunQiuTing-SuoLinNang.xm
      l',
      [[2.0, 14.75],
       [15.0, 25.25],
       [27.0, 36.75],
       [37.0, 47.25],
       [49.0, 58.75],
       [59.0, 72.75],
       [75.0, 84.25]]],
     ['../../Jingju-Music-Scores/MusicXML scores/daxp-QiaoLouShang-HuangShanLei
      .xml',
      [[559.0, 574.0],
       [577.0, 590.25],
       [591.0, 608.0],
       [609.0, 627.0],
       [639.0, 650.0]]]]
    '''
    
    # Check that the inputted info is correct input
    hd = checkInput(hangdang, 'hd')
    sq = checkInput(shengqiang, 'sq')
    bs = checkInput(banshi, 'bs')
    ju = checkInput(judou, 'ju')
    
    print('\nRetrieving lines that meet the given criteria...')

    # Get the path of the folder shared by the linesData file and the xml
    # scores
    path = linesData[:linesData.rfind('/')+1]
    if len(path) == 0:
        path = linesData[:linesData.rfind('\\')+1]
        path = path.replace('\\', '/')

    with open(linesData, 'r', encoding='utf-8') as f:
        data = f.readlines()

    material = []
    
    found_lines = 0

    # Search information
    searchInfo = {'hd':[], 'sq':[], 'bs':[], 'ju':[]}
    material.append(searchInfo)

    # Segments collection
    for line in data:
        strInfo = line.strip().split(',')
        score = strInfo[0]
        if score != '':
            material.append([path+score,[]])
            if 'Part 1' in line: continue

        if (score == '') and ('Part' in line):
            material[-1].append([])
            continue

        hd0 = strInfo[1]
        sq0 = strInfo[2]
        bs0 = strInfo[3]
        ju0 = strInfo[4]

        # Get the starting and ending points of the line as floats or fractions
        start = floatOrFraction(strInfo[6])
        end = floatOrFraction(strInfo[7])

        if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
            material[-1][-1].append([start, end])
            found_lines += 1
            if hd0 not in material[0]['hd']:
                material[0]['hd'].append(hd0)
            if sq0 not in material[0]['sq']:
                material[0]['sq'].append(sq0)
            if bs0 not in material[0]['bs']:
                material[0]['bs'].append(bs0)
            if ju0 not in material[0]['ju']:
                material[0]['ju'].append(ju0)

    printingFound(material[0], hangdang, shengqiang, banshi, judou,
                  found_lines)

    # Delete empty lists
    score2remove = []
    for i in range(1, len(material)):
        score = material[i]
        partsLength = 0
        for j in range(1, len(score)):
            part = score[j]
            partsLength += len(part)
        if partsLength == 0:
            score2remove.insert(0, i)
    if len(score2remove) != 0:
        for l in score2remove:
            material.pop(l)

    return material



def collectLineJudouMaterial(linesData,
                             hangdang=['laosheng', 'dan'],
                             shengqiang=['erhuang', 'xipi'],
                             banshi=['manban', 'sanyan', 'zhongsanyan',
                                     'kuaisanyan', 'yuanban', 'erliu',
                                     'liushui', 'kuaiban'],
                             judou=['s', 's1', 's2', 'x']):
    '''
    Given the path to the lines_data.csv file, that should be stored in the
    same folder as the MusicXML scores of the Jingju Music Scores Collection,
    it returns information for accessing all the line sections that meet the
    input criteria. If for any of the input instances no line is retrieved, a
    warning message indicates so.
    
    Paramenters:
    - linesData -- str, path to the lines_data.csv file
    - hangdang -- [str], list of role types
    - shengqiang -- [str], list of shengqiang
    - banshi -- [str], list of banshi
    - judou -- [str], list of line types
    
    It returns a list with the following elements:
    - a dictionary with the instances of each element for which a line is
          retrived. The keys are 'hd' for role type, 'sq' for shengqiang, 'bs'
          for banshi, and 'ju' for line type. Values are lists of strings
    - a series of lists for the scores from which lines are retrived. Each of
          these lists contains the following information
          - the path to the MusicXML file of the given score
          - a list for each of the vocal parts contained in the score. Each of
                these lists includes a list for each of the retrieved lines.
                And each of these lists contains three lists, one per line
                section, including two floats representing the starting and
                ending offset of a retrived line that part from that score. If
                a particular line misses one section, an empty list for that
                particular section is returned
    
    For example:
    
    >>> collectLineJudouMaterial('path-to-lines_data.csv', hangdang=['dan'], sh
        engqiang=['xipi'], banshi=['erliu'])

    Retrieving sections for lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    Out[10]: 
    [{'bs': ['erliu'], 'hd': ['dan'], 'ju': ['s', 'x'], 'sq': ['xipi']},
     ['../../Jingju-Music-Scores/MusicXML scores/daxp-ChunQiuTing-SuoLinNang.xm
      l',
      [[[2.0, 5.5], [7.0, 9.25], [10.0, 14.75]],
       [[15.0, 17.25], [18.0, 19.75], [20.0, 25.25]],
       [[27.0, 29.25], [30.0, 31.75], [32.0, 36.75]],
       [[37.0, 39.5], [40.0, 41.75], [42.0, 47.25]],
       [[49.0, 51.25], [52.0, 53.25], [54.0, 58.75]],
       [[59.0, 61.75], [62.0, 64.25], [66.0, 72.75]],
       [[75.0, 77.25], [78.0, 79.75], [80.0, 84.25]]]],
     ['../../Jingju-Music-Scores/MusicXML scores/daxp-QiaoLouShang-HuangShanLei
      .xml',
      [[[559.0, 563.25], [565.0, 567.75], [568.0, 574.0]],
       [[577.0, 580.75], [583.0, 585.75], [586.0, 590.25]],
       [[591.0, 595.25], [597.0, 599.5], [600.0, 608.0]],
       [[609.0, 611.25], [612.0, 618.0], [619.5, 627.0]],
       [[639.0, 641.5], [642.0, 644.5], [645.0, 650.0]]]]]
    '''
    
    # Check that the inputted info is correct input
    hd = checkInput(hangdang, 'hd')
    sq = checkInput(shengqiang, 'sq')
    bs = checkInput(banshi, 'bs')
    ju = checkInput(judou, 'ju')
    
    print('\nRetrieving sections for lines that meet the given criteria...')

    # Get the path of the folder shared by the linesData file and the xml
    # scores
    path = linesData[:linesData.rfind('/')+1]
    if len(path) == 0:
        path = linesData[:linesData.rfind('\\')+1]
        path = path.replace('\\', '/')

    with open(linesData, 'r', encoding='utf-8') as f:
        data = f.readlines()

    material = []
    
    found_lines = 0

    # Search information
    searchInfo = {'hd':[], 'sq':[], 'bs':[], 'ju':[]}
    material.append(searchInfo)

    # Segments collection
    for line in data:
        strInfo = line.strip().split(',')
        score = strInfo[0]
        if score != '':
            material.append([path+score,[]])
            if 'Part 1' in line: continue

        if (score == '') and ('Part' in line):
            material[-1].append([])
            continue

        hd0 = strInfo[1]
        sq0 = strInfo[2]
        bs0 = strInfo[3]
        ju0 = strInfo[4]

        if (hd0 in hd) and (sq0 in sq) and (bs0 in bs) and (ju0 in ju):
            material[-1][-1].append([])
            found_lines += 1
            if hd0 not in material[0]['hd']:
                material[0]['hd'].append(hd0)
            if sq0 not in material[0]['sq']:
                material[0]['sq'].append(sq0)
            if bs0 not in material[0]['bs']:
                material[0]['bs'].append(bs0)
            if ju0 not in material[0]['ju']:
                material[0]['ju'].append(ju0)

            if strInfo[10] != '':
                ju1_start = floatOrFraction(strInfo[10])
                ju1_end = floatOrFraction(strInfo[11])
                ju1 = [ju1_start, ju1_end]
            else:
                ju1 = []
            material[-1][-1][-1].append(ju1)

            if strInfo[13] != '':
                ju2_start = floatOrFraction(strInfo[13])
                ju2_end = floatOrFraction(strInfo[14])
                ju2 = [ju2_start, ju2_end]
            else:
                ju2 = []
            material[-1][-1][-1].append(ju2)

            if strInfo[16] != '':
                ju3_start = floatOrFraction(strInfo[16])
                ju3_end = floatOrFraction(strInfo[17])
                ju3 = [ju3_start, ju3_end]
            else:
                ju3 = []
            material[-1][-1][-1].append(ju3)

    printingFound(material[0], hangdang, shengqiang, banshi, judou,
                  found_lines)    

    # Delete empty lists
    score2remove = []
    for i in range(1, len(material)):
        score = material[i]
        partsLength = 0
        for j in range(1, len(score)):
            part = score[j]
            partsLength += len(part)
        if partsLength == 0:
            score2remove.insert(0, i)
    if len(score2remove) != 0:
        for l in score2remove:
            material.pop(l)

    return material



###############################################################################
## MAIN FUNCTIONS                                                            ##
###############################################################################

def pitchHistogram(linesData,
                   hd=['laosheng', 'dan'],
                   sq=['erhuang', 'xipi'],
                   bs = ['manban', 'sanyan', 'zhongsanyan','kuaisanyan',
                         'yuanban', 'erliu', 'liushui', 'kuaiban'],
                   ju = ['s', 's1', 's2', 'x'],
                   filename=None,
                   count='sum',
                   countGraceNotes=True,
                   scaleGuides=True,
                   title=None,
                   width=0.8,
                   title_fontsize=30,
                   xticks_fontsize=20,
                   yticks_fontsize=18,
                   xLabel_fontsize=26,
                   yLabel_fontsize=26):
    '''
    Given the path to the lines_data.csv file, that should be stored in the
    same folder as the MusicXML scores of the Jingju Music Scores Collection,
    it computes a pitch histogram for all the lines that meet the input
    criteria. If a path to an image file is given, a plot is returned. If for
    any of the input instances no line is retrieved, a warning message
    indicates so.
    
    Parameters:
    - linesData -- str, path to the lines_data.csv file
    - hangdang -- [str], list of role types
    - shengqiang -- [str], list of shengqiang
    - banshi -- [str], list of banshi
    - judou -- [str], list of line types
    - filename -- str, path for saving the returned plot as an image file. If
          None given, no plot is returned
    - count -- str, normalization method. It takes three values, 'sum' for
          normalizing the results to the summation of all the computed values,
          'max' for normalizing the results to the maximum computed value, and
          'abs' for no normalization
    - countGraceNotes -- bool, if True, grace notes are also computed. A
          quarterLength value is assigned to each grace note equivalent to the
          minimum quarterLength value present in the given score, but never
          higher than 0.25. If False, grace notes are ignored
    - scaleGuides -- bool, if True, vertical lines indicating first and five
          degrees are drawn in the returned plot. If False, no vertical lines
          are drawn
    - title -- str, title of the returned plot. If None, the plot is returned
          without a title
    - width -- float, width of the bars in the plot
    - title_fontsize -- int, size of the font for the plot's title
    - xticks_fontsize -- int, size of the font for the x axis' ticks
    - yticks_fontsize -- int, size of the font for the y axis' ticks
    - xLabel_fontsize -- int, size of the font for the x axis' label
    - yLabel_fontsize -- int, size of the font for the y axis' label
    
    It returns an ordered list containing a list for each of the pitches
    computed in the histogram, containing a string for the pitch name and a
    float for the (normalized) count of that pitch in the histogram. If a path
    to a file is input to the filename parameter, an image is also returned.
    
    For example:
    >>> pitchHistogram('path-to-lines_data.csv', hd=['dan'], sq=['xipi'], bs=['
        erliu'])

    Retrieving lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    
    Computing pitch histogram...
    Processing scores:
            Parsing daxp-ChunQiuTing-SuoLinNang.xml
            Parsing daxp-QiaoLouShang-HuangShanLei.xml
    Histogram computed.
    [['D#4', 0.0035794183445190158],
     ['E4', 0.008948545861297539],
     ['F#4', 0.098434004474272932],
     ['G#4', 0.25458612975391498],
     ['A4', 0.047874720357941832],
     ['B4', 0.25100671140939596],
     ['C#5', 0.17986577181208055],
     ['D#5', 0.038478747203579418],
     ['E5', 0.098434004474272932],
     ['F#5', 0.017897091722595078],
     ['G#5', 0.00089485458612975394]]
    '''
    
    material = collectLineMaterial(linesData, hangdang=hd, shengqiang=sq,
                                   banshi=bs, judou=ju)

    print('\nComputing pitch histogram...\nProcessing scores:')

    pitchCount = {}

    for score in material[1:]:
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print('\tParsing ' + scoreName)
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notes.stream()

            # Set the duration of grace notes if needed
            if countGraceNotes:
                minDur = 0.25
                for n in notes:
                    noteDur = n.quarterLength
                    if noteDur!=0 and noteDur<minDur:
                        minDur = noteDur

            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                # Count pitches in the current segment
                for n in segment:
                    noteName = n.nameWithOctave
                    noteDur = n.quarterLength
                    if noteDur == 0:
                        if not countGraceNotes: continue
                        noteDur = minDur
                    pitchCount[noteName] = pitchCount.get(noteName, 0)+noteDur

    print('Histogram computed.')

    # Sorting duration per pitch class frequency
    pitches = pitchCount.keys()
    toSort = {p:pitch.Pitch(p).midi for p in pitches}
    sortedPitches = sorted(toSort.items(), key=lambda x: x[1])
    xPositions = np.array([p[1] for p in sortedPitches])
    xLabels = [p[0] for p in sortedPitches]
    yValues = np.array([pitchCount[l] for l in xLabels])

    # Setting the parameters for plotting
    yValues, limX, yLabel, col, h = plottingParameters(material,count,yValues)

    if filename != None:
        # Start plotting
        print('\nPlotting...')

        # Setting y limits
        limY = None
        if count == 'sum':
            limY = [0, 0.35]

        plotting(filename, xPositions, xLabels, yValues, limX=limX,
                 xLabel='Pitch', limY=limY, yLabel=yLabel, col=col, h=h,
                 scaleGuides=scaleGuides, width=width,
                 title_fontsize=title_fontsize,
                 xticks_fontsize=xticks_fontsize,
                 yticks_fontsize=yticks_fontsize,
                 xLabel_fontsize=xLabel_fontsize,
                 yLabel_fontsize=yLabel_fontsize)

    # List to return
    results = []
    for i in range(len(xLabels)):
        results.append([xLabels[i], yValues[i]])

    return results



def pitchHistogramLineJudou(linesData,
                            hd=['laosheng', 'dan'],
                            sq=['erhuang', 'xipi'],
                            bs = ['manban', 'sanyan', 'zhongsanyan',
                                  'kuaisanyan', 'yuanban', 'erliu', 'liushui',
                                  'kuaiban'],
                            ju = ['s', 's1', 's2', 'x'],
                            filename=None, count='sum',
                            countGraceNotes=True,
                            scaleGuides=True,
                            title=None,
                            width=0.8,
                            title_fontsize=30,
                            xticks_fontsize=15,
                            yticks_fontsize=15,
                            xLabel_fontsize=26,
                            yLabel_fontsize=26):

    '''
    Given the path to the lines_data.csv file, that should be stored in the
    same folder as the MusicXML scores of the Jingju Music Scores Collection,
    it computes a pitch histogram for the three sections of all the lines that
    meet the input criteria. If a path to an image file is given, a plot is
    returned. If for any of the input instances no line is retrieved, a warning
    message indicates so.
    
    Parameters:
    - linesData -- str, path to the lines_data.csv file
    - hangdang -- [str], list of role types
    - shengqiang -- [str], list of shengqiang
    - banshi -- [str], list of banshi
    - judou -- [str], list of line types
    - filename -- str, path for saving the returned plot as an image file. If
          None given, no plot is returned
    - count -- str, normalization method. It takes three values, 'sum' for
          normalizing the results to the summation of all the computed values,
          'max' for normalizing the results to the maximum computed value, and
          'abs' for no normalization
    - countGraceNotes -- bool, if True, grace notes are also computed. A
          quarterLength value is assigned to each grace note equivalent to the
          minimum quarterLength value present in the given score, but never
          higher than 0.25. If False, grace notes are ignored
    - scaleGuides -- bool, if True, vertical lines indicating first and five
          degrees are drawn in the returned plot. If False, no vertical lines
          are drawn
    - title -- str, title of the returned plot. If None, the plot is returned
          without a title
    - width -- float, width of the bars in the plot
    - title_fontsize -- int, size of the font for the plot's title
    - xticks_fontsize -- int, size of the font for the x axis' ticks
    - yticks_fontsize -- int, size of the font for the y axis' ticks
    - xLabel_fontsize -- int, size of the font for the x axis' label
    - yLabel_fontsize -- int, size of the font for the y axis' label
    
    It returns a list containing an ordered list for each the three line
    sections. Each of these three lists contains a list for each of all the
    pitches computed. Each of these lists contains a string for the pitch name
    and a float for the (normalized) count of that pitch in the histogram. If a
    particular pitch is not present in a particular section, a list for that
    pitch is still included, containing the pitch name and '--' instead of a
    value. If a path to a file is input to the filename parameter, an image is
    also returned including a vertical histogram for each line section.
    
    For example:
    >>> pitchHistogramLineJudou('path-to-lines_data.csv', hd=['dan'], sq=['xipi
        '], bs=['erliu'])

    Retrieving sections for lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    
    Computing pitch histograms...
    Processing scores:
            Parsing daxp-ChunQiuTing-SuoLinNang.xml
            Parsing daxp-QiaoLouShang-HuangShanLei.xml
    Histograms computed.
    [[['D#4', '--'],
      ['E4', 0.013008130081300813],
      ['F#4', 0.078048780487804878],
      ['G#4', 0.35772357723577236],
      ['A4', 0.04878048780487805],
      ['B4', 0.1951219512195122],
      ['C#5', 0.10731707317073171],
      ['D#5', 0.019512195121951219],
      ['E5', 0.14959349593495935],
      ['F#5', 0.030894308943089432],
      ['G#5', '--']],
     [['D#4', '--'],
      ['E4', '--'],
      ['F#4', 0.072657743785850867],
      ['G#4', 0.21797323135755259],
      ['A4', 0.038240917782026769],
      ['B4', 0.29827915869980881],
      ['C#5', 0.24091778202676864],
      ['D#5', 0.017208413001912046],
      ['E5', 0.10707456978967496],
      ['F#5', 0.0076481835564053535],
      ['G#5', '--']],
     [['D#4', 0.0072926162260711028],
      ['E4', 0.010938924339106655],
      ['F#4', 0.12215132178669097],
      ['G#4', 0.21422060164083864],
      ['A4', 0.051959890610756607],
      ['B4', 0.25979945305378305],
      ['C#5', 0.19143117593436645],
      ['D#5', 0.059252506836827715],
      ['E5', 0.065633546034639931],
      ['F#5', 0.015496809480401094],
      ['G#5', 0.0018231540565177757]]]
    '''
    
    material = collectLineJudouMaterial(linesData, hangdang=hd, shengqiang=sq,
                                        banshi=bs, judou=ju)

    print('\nComputing pitch histograms...\nProcessing scores:')

    j1p = {}    # pitch count for judou 1
    j2p = {}    # pitch count for judou 2
    j3p = {}    # pitch count for judou 3

    for score in material[1:]:
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print('\tParsing ' + scoreName)
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notes.stream()

            # Set the duration of grace notes if needed
            if countGraceNotes:
                minDur = 0.25
                for n in notes:
                    noteDur = n.quarterLength
                    if noteDur!=0 and noteDur<minDur:
                        minDur = noteDur

            # Find segments to analyze in the current part
            for line in score[partIndex]:
                for judou in range(len(line)):
                    if len(line[judou]) == 0: continue
                    start = line[judou][0]
                    end = line[judou][1]
                    segment = notes.getElementsByOffset(start, end)
                    # Count pitches in the current segment
                    for n in segment:
                        noteName = n.nameWithOctave
                        noteDur = n.quarterLength
                        if noteDur == 0:
                            if not countGraceNotes: continue
                            noteDur = minDur
                        if judou == 0:
                            j1p[noteName] = j1p.get(noteName, 0) + noteDur
                        elif judou == 1:
                            j2p[noteName] = j2p.get(noteName, 0) + noteDur
                        elif judou == 2:
                            j3p[noteName] = j3p.get(noteName, 0) + noteDur
                        else:
                            print('There is a problem with the number of '\
                                  'judou in this line')
                            break

    print('Histograms computed.')

    jps = [j1p, j2p, j3p]
    
    jps_plotting = []
    pre_yLab_general = []

    for jp in jps:
        # Sorting duration per pitch class frequency
        pitches = jp.keys()
        toSort = {p:pitch.Pitch(p).midi for p in pitches}
        for pk in toSort.keys():
            if pk not in pre_yLab_general:
                pre_yLab_general.append(pk)
        sortedPitches = sorted(toSort.items(), key=lambda x: x[1])
        yPositions = np.array([p[1] for p in sortedPitches])
        yLabels = [p[0] for p in sortedPitches]
        xValues = np.array([jp[l] for l in yLabels])
    
        # Setting the parameters for plotting for first judou
        xValues, limY, xLabel, col, h = plottingParameters(material, count,
                                                            xValues)
        
        jps_plotting.append({'xValues': xValues, 'xLabel': xLabel,
                            'yPositions': yPositions, 'yLabels': yLabels,
                            'limY': limY, 'col': col,
                            'h': h})

    # Y axis labels for the three histograms
    toSort = {p:pitch.Pitch(p).midi for p in pre_yLab_general}
    sortedPitches = sorted(toSort.items(), key=lambda x: x[1])
    yPos_general = np.array([p[1] for p in sortedPitches])
    yLab_general = [p[0] for p in sortedPitches]

    if filename != None:
        # Start plotting
        print('\nPlotting...')

        # Setting y limits
        if count == 'sum':
            limX = [0, 0.5]
        elif count == 'max':
            limX = [0, 1]
        elif count == 'abs':
            limX = [0, 0]
            for j in jps_plotting:
                max_val = max(j['xValues'])
                if max_val > limX[1]:
                    limX[1] = max_val
            
        ticksX = np.round(np.arange(limX[0], limX[1], limX[1]/5), 1)
            
        width = 0.8
        
        plt.figure()
        
        for i in range(len(jps_plotting)):
            jp = jps_plotting[i]
            plt.subplot(131+i)
            plt.barh(jp['yPositions'], jp['xValues'], width, linewidth=0,
                     zorder=1, color = jp['col'], hatch = jp['h'])
            plt.axhline(y=64+width/2, color='red', zorder=0) # Tonic line
            plt.axhline(y=76+width/2, color='red', ls='--', zorder=0) # 8ve
            plt.axhline(y=59+width/2, color='gray', ls=':', zorder=0) # Fifth
            plt.axhline(y=71+width/2, color='gray', ls=':', zorder=0) # Fifth
            plt.axhline(y=83+width/2, color='gray', ls=':', zorder=0) # Fifth
            for xValue in jp['xValues']:
                plt.axvline(x=xValue, color='gray', ls=':', zorder=0)
            if i == 0:
                plt.yticks(yPos_general + width/2, yLab_general,
                           fontsize=yticks_fontsize)
                plt.ylabel('Pitch', fontsize=yLabel_fontsize)
            else:
                plt.yticks([])
            if i == 1:
                plt.xlabel(xLabel, fontsize=xLabel_fontsize)
            plt.ylim(jp['limY'][0], jp['limY'][1])
            plt.xticks(ticksX, ticksX, rotation=90, fontsize=xticks_fontsize)
            plt.xlim(limX[0], limX[1])
    
        plt.tight_layout()
        if title != None:
            plt.suptitle(title, fontsize=title_fontsize)
            plt.subplots_adjust(top=1-title_fontsize/300)
        plt.savefig(filename)    
#        plt.show()
        print('"' + filename + '" plotted and saved.')

    # List to return
    results = []
    for dou in jps_plotting:
        d = []
        for label in yLab_general:
            if label in dou['yLabels']:
                d.append([label, dou['xValues'][dou['yLabels'].index(label)]])
            else:
                d.append([label, '--'])
        results.append(d)
        
    if not len(results[0]) == len(results[1]) == len(results[2]):
        print('ERROR: There was a problem saving the results. The program '\
              'will exit')
        exit()

    return results



def intervalHistogram(linesData,
                      hd=['laosheng', 'dan'],
                      sq=['erhuang', 'xipi'],
                      bs = ['manban', 'sanyan', 'zhongsanyan','kuaisanyan',
                            'yuanban', 'erliu', 'liushui', 'kuaiban'],
                      ju = ['s', 's1', 's2', 'x'],
                      filename=None,
                      count='sum',
                      directedInterval=False,
                      silence2ignore=0.25,
                      ignoreGraceNotes=False,
                      title=None,
                      width=0.8,
                      title_fontsize=30,
                      xticks_fontsize=20,
                      yticks_fontsize=18,
                      xLabel_fontsize=26,
                      yLabel_fontsize=26):

    '''
    Given the path to the lines_data.csv file, that should be stored in the
    same folder as the MusicXML scores of the Jingju Music Scores Collection,
    it computes an interval histogram for all the lines that meet the input
    criteria. If a path to an image file is given, a plot is returned. If for
    any of the input instances no line is retrieved, a warning message
    indicates so.
    
    Parameters:
    - linesData -- str, path to the lines_data.csv file
    - hd -- [str], list of role types
    - sq -- [str], list of shengqiang
    - bs -- [str], list of banshi
    - jd -- [str], list of line types
    - filename -- str, path for saving the returned plot as an image file. If
          None given, no plot is returned
    - count -- str, normalization method. It takes three values, 'sum' for
          normalizing the results to the summation of all the computed values,
          'max' for normalizing the results to the maximum computed value, and
          'abs' for no normalization
    - directedInterval -- bool, if False the direction of the interval
          (ascending or descending) is not considered. If True, the direction
          of the interval is considered
    - silence2ignore -- float, establishes the quarterLength duration of a rest
          between two notes to be ignored for the computation of the interval
          that those two notes form
    - ignoreGraceNotes -- bool, if True, grace notes are ignored. If False,
          grace notes are considered for the computation of intervals
    - title -- str, title of the returned plot. If None, the plot is returned
          without a title
    - width -- float, width of the bars in the plot
    - title_fontsize -- int, size of the font for the plot's title
    - xticks_fontsize -- int, size of the font for the x axis' ticks
    - yticks_fontsize -- int, size of the font for the y axis' ticks
    - xLabel_fontsize -- int, size of the font for the x axis' label
    - yLabel_fontsize -- int, size of the font for the y axis' label
    
    It returns an ordered list containing a list for each of the invervals
    computed in the histogram, containing a string for the interval name and a
    float for the (normalized) count of that interval in the histogram. If a
    path to a file is input to the filename parameter, an image is also
    returned. The name of the interval is formed by the initial of the interval
    quality and an integer for the interval number. The initials stand for the
    following qualities: P -- Perfect, m -- minor, M -- Major, A -- Augmented,
    d -- diminished. If the direction of the interval is considered, descending
    intervals are identified with a minus sign "-" between the quality and the
    number, so that "m-3" indicates a descending minor third. In this case, the
    absence of this minus sign indicates an ascending interval.
    
    For example:
    >>> intervalHistogram(ln, hd=['dan'], sq=['xipi'], bs=['erliu'])

    Retrieving lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    
    Computing interval histogram...
    Processing scores:
            Parsing daxp-ChunQiuTing-SuoLinNang.xml
            Parsing daxp-QiaoLouShang-HuangShanLei.xml
    Histogram computed.    
    [['P1', 0.098321342925659472],
     ['m2', 0.088729016786570747],
     ['M2', 0.46762589928057552],
     ['m3', 0.21103117505995203],
     ['M3', 0.043165467625899283],
     ['P4', 0.064748201438848921],
     ['P5', 0.0047961630695443642],
     ['m6', 0.016786570743405275],
     ['m7', 0.0047961630695443642]]
    '''
    
    material = collectLineMaterial(linesData, hangdang=hd, shengqiang=sq,
                                   banshi=bs, judou=ju)

    print('\nComputing interval histogram...\nProcessing scores:')

    intervalCount = {}

    for score in material[1:]:
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print('\tParsing ' + scoreName)
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notesAndRests.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                # Count intervals in the current segment
                # Find the last note that is not a grace note
                i = 1
                lastn = segment[-i]
                while lastn.quarterLength == 0:
                    i += 1
                    lastn = segment[-i]

                for j in range(len(segment)-i):
                    n1 = segment[j]
                    if n1.isRest: continue
                    if ignoreGraceNotes:
                        if n1.quarterLength == 0: continue
                    k = 1
                    while True:
                        n2 = segment[j+k]
                        if n2.isRest:
                            if n2.quarterLength <= silence2ignore:
                                k += 1
                            else:
                                n2 = None
                                break
                        elif (n2.quarterLength==0)and(ignoreGraceNotes==True):
                            j += 1
                        else:
                            break
                    if n2==None: continue
                    intvl = interval.Interval(n1, n2)
                    if directedInterval:
                        intvlName = intvl.directedName
                    else:
                        intvlName = intvl.name
                    intervalCount[intvlName] = (intervalCount.get(intvlName, 0)
                                                + 1)

    print('Histogram computed.')

    # Sorting intervals per size
    intvlNames = intervalCount.keys()
    toSort = {i:interval.Interval(i).semitones for i in intvlNames}
    sortedIntvl = sorted(toSort.items(), key=lambda x: x[1])
    xPositions = np.array([i[1] for i in sortedIntvl])
    # Check if there repeated positions
    for i in range(1, len(xPositions)):
        if xPositions[i] != xPositions[i-1]: continue
        for j in range(i):
            xPositions[j] += -1
    xLabels = [i[0] for i in sortedIntvl]
    yValues = np.array([intervalCount[l] for l in xLabels])

    ## Setting the parameters for plotting
    yValues, limX, yLabel, col, h = plottingParameters(material,count,yValues)

    if filename != None:
        # Start plotting
        print('\nPlotting...')

        # Setting x limits
        limX = None

        # Setting y limits
        limY = None
        if count == 'sum':
            if directedInterval:
                limY = [0, 0.27]
            else:
                limY = [0, 0.5]

        plotting(filename, xPositions, xLabels, yValues, title=title,
                 limX=limX, xLabel='Interval',limY=limY, yLabel=yLabel,
                 col=col, h=h, width=width, title_fontsize=title_fontsize,
                 xticks_fontsize=xticks_fontsize,
                 yticks_fontsize=yticks_fontsize,
                 xLabel_fontsize=xLabel_fontsize,
                 yLabel_fontsize=yLabel_fontsize)

    # List to return
    results = []
    for i in range(len(xLabels)):
        results.append([xLabels[i], yValues[i]])

    return results



def cadentialNotes(linesData,
                   hd=['laosheng', 'dan'],
                   sq=None,
                   bs = ['manban', 'sanyan', 'zhongsanyan','kuaisanyan',
                         'yuanban', 'erliu', 'liushui','kuaiban'],
                   filename=None,
                   includeGraceNotes=True,
                   width=0.5,
                   title_fontsize=30,
                   xticks_fontsize=20,
                   yticks_fontsize=18,
                   legend_fontsize=20,
                   adjust_right_margin=0.77):
    '''
    Given the path to the lines_data.csv file, that should be stored in the
    same folder as the MusicXML scores of the Jingju Music Scores Collection,
    it computes the proportion of pitches used as cadential notes for each
    section of all the line types used in the given shengqiang and banshi.
    Consequently, it only takes one shengqiang, that should be input as a list,
    and it doesn't take any line type instance. If an invalid input is given,
    an error message indicates so and asks the user for a correction. If a path
    to an image file is given, a plot is returned. If for any of the input
    instances no line is retrieved, a warning message indicates so.
    
    Parameters:
    - linesData -- str, path to the lines_data.csv file
    - hd -- [str], list of role types
    - sq -- [str], list of shengqiang
    - bs -- [str], list of banshi
    - filename -- str, path for saving the returned plot as an image file. If
          None given, no plot is returned
    - includeGraceNotes -- bool, if True, grace notes are also computed. If
          False, grace notes are ignored
    - width -- float, width of the bars in the plot
    - title_fontsize -- int, size of the font for the plot's title
    - xticks_fontsize -- int, size of the font for the x axis' ticks
    - yticks_fontsize -- int, size of the font for the y axis' ticks
    - legend_fontsize -- int, size of the font for the labels in the legend
    - adjust_right_margin -- float, distance to the right margin of each line
          type's box, in percentage normalize to one.
    
    It returns a dictionary with the following structure:
    - keys: str, line type, including 'Op. line' for opening line and 'Cl.
          line' for closing line (xipi), 'Op. l. 1' for opening line 1, 'Op. l.
          2' for opening line 2, and 'Cl. l.' for closing line (erhuang)
    - values: a dictionary with the following structure>
          - keys: str, line section, including 'S1' for the first section, 'S2'
                for the second sectioin, and 'S3' for the third section
          - values: an ordered list containing a list for each of all the
                pitches found across line types and sections. Each of these
                lists contains a string for the pitch name, and a float for the
                (normalized) count of that pitch in the given line section.
    If a path to a file is input to the filename parameter, an image is also
    returned.
    
    For example:
    >>> cadentialNotes(ln, hd=['dan'], sq=['xipi'], bs=['erliu'])
    
    Counting cadential notes for opening lines...
    
    Retrieving sections for lines that meet the given criteria...
    
    6 lines were retrieved for the combination of dan, xipi, erliu and s.
    
    Processing scores:
            Parsing daxp-ChunQiuTing-SuoLinNang.xml
            Parsing daxp-QiaoLouShang-HuangShanLei.xml
    Notes for opening lines counted.
    
    Counting cadential notes for closing lines...
    
    Retrieving sections for lines that meet the given criteria...
    
    6 lines were retrieved for the combination of dan, xipi, erliu and x.
    
    Processing scores:
            Parsing daxp-ChunQiuTing-SuoLinNang.xml
            Parsing daxp-QiaoLouShang-HuangShanLei.xml
    Notes for closing lines counted.
    {'Cl. line': {'S1': [['D#4', 0.0],
       ['E4', 33.333333333333336],
       ['F#4', 0.0],
       ['G#4', 16.666666666666668],
       ['A4', 0.0],
       ['B4', 50.0],
       ['C#5', 0.0]],
      'S2': [['D#4', 0.0],
       ['E4', 0.0],
       ['F#4', 0.0],
       ['G#4', 66.666666666666671],
       ['A4', 0.0],
       ['B4', 33.333333333333336],
       ['C#5', 0.0]],
      'S3': [['D#4', 33.333333333333336],
       ['E4', 0.0],
       ['F#4', 0.0],
       ['G#4', 0.0],
       ['A4', 16.666666666666668],
       ['B4', 50.0],
       ['C#5', 0.0]]},
     'Op. line': {'S1': [['D#4', 0.0],
       ['E4', 0.0],
       ['F#4', 0.0],
       ['G#4', 33.333333333333336],
       ['A4', 0.0],
       ['B4', 66.666666666666671],
       ['C#5', 0.0]],
      'S2': [['D#4', 0.0],
       ['E4', 0.0],
       ['F#4', 33.333333333333336],
       ['G#4', 16.666666666666668],
       ['A4', 0.0],
       ['B4', 33.333333333333336],
       ['C#5', 16.666666666666668]],
      'S3': [['D#4', 0.0],
       ['E4', 0.0],
       ['F#4', 0.0],
       ['G#4', 0.0],
       ['A4', 0.0],
       ['B4', 83.333333333333343],
       ['C#5', 16.666666666666668]]}}
    '''

    xLabels = ['S1', 'S2', 'S3']
    pos = np.arange(len(xLabels))

    colors = {'G#3':['#F4D03F','x'],'B3':['#76D7C4','x'],'C#4':['#2E86C1','x'],
              'C##4':['#5B2C6F','x'],'D#4':['#BB8FCE','x'],'E4':['#E74C3C',''],
              'F#4':['#F39C12',''], 'G#4':['#F4D03F',''], 'A4':['#2ECC71',''],
              'A#4':['#117864',''], 'B4':['#76D7C4',''], 'C#5':['#2E86C1',''],
              'D#5':['#BB8FCE',''],'E5':['#E74C3C','O'],'F#5':['#F39C12','O']}

    legendCode = {}

    pre_result = {}
    result = {}
    
    hd, sq, bs = checkInput_cn(hd, sq, bs)

    if sq == ['xipi']:
        titles = ['Op. line', 'Cl. line']
        judous = ['s', 'x']
        nice_names = ['opening lines', 'closing lines']
    elif sq == ['erhuang']:
        titles = ['Op. l. 1', 'Op. l. 2', 'Cl. l.']
        judous = ['s1', 's2', 'x']
        nice_names = ['opening lines (type 1)', 'opening lines (type 2)',
                      'closing lines']

    y = True
    plt.figure()
    for i in range(len(judous)):
        print('\nCounting cadential notes for ' + nice_names[i] + '...')
        lt = titles[i] # lt: line type
        pre_result[lt] = {}
        result[lt] = {}
        sortedNoteNames, sortedValues = findCadentialNotes(linesData, hd, sq,
                                                           bs, [judous[i]],
                                                           includeGraceNotes=\
                                                           includeGraceNotes)
        print('Notes for ' + nice_names[i] + ' counted.')

        for j in range(len(xLabels)):
            sec = xLabels[j]
            pre_result[lt][sec] = {} # sec: section
            result[lt][sec] = []
            for k in range(len(sortedNoteNames)):
                nn = sortedNoteNames[k] # note name
                pre_result[lt][sec][nn] = sortedValues[k][j]

        bot = np.array([0, 0, 0])
        plotNumber = '1' + str(len(judous)) + str(i+1)
        plt.subplot(int(plotNumber))
        for l in range(len(sortedValues)):
            val = sortedValues[l]
            colHatch = colors[sortedNoteNames[l]]
            p = plt.bar(pos, val, width, color=colHatch[0],
                        hatch = colHatch[1], bottom=bot, align='center')
            bot = bot + val
            # Prepare the legend
            noteName = sortedNoteNames[l]
            mid = pitch.Pitch(noteName).midi
            legendCode[mid] = [p[0], noteName]
        if not y:
            plt.yticks(np.array([]), ())
        y = False
        plt.ylim(0, 100)
        plt.title(lt, fontsize=title_fontsize)
        plt.yticks(fontsize=yticks_fontsize)
        plt.xticks(pos, xLabels, fontsize=xticks_fontsize)

    legendColors = []
    legendNotes = []
    for k in sorted(legendCode.keys(), reverse=True):
        lcode = legendCode[k]
        legendColors.append(lcode[0])
        legendNotes.append(lcode[1])
    plt.legend(legendColors, legendNotes, bbox_to_anchor=(1, 1), loc=2,
               fontsize=legend_fontsize)
    plt.tight_layout(rect=(0, 0, adjust_right_margin, 1))

    if filename != None:
        print('\nPlotting...')
        plt.savefig(filename)
#        plt.show()
        print('"' + filename + '" plotted and saved.')
    
    # Final results:
    for line in pre_result:
        for s in pre_result[line]:
            for n in reversed(legendNotes):
                try:
                    result[line][s].append([n, pre_result[line][s][n]])
                except:
                    result[line][s].append([n, 0.0])

    return result



def melodicDensity(linesData,
                   hd=['laosheng', 'dan'],
                   sq=['erhuang', 'xipi'],
                   bs = ['manban', 'sanyan', 'zhongsanyan','kuaisanyan',
                         'yuanban', 'erliu', 'liushui', 'kuaiban'],
                   ju = ['s', 's1', 's2', 'x'],
                   filename=None,
                   includeGraceNotes=True,
                   notesOrDuration='notes',
                   yticks_fontsize=18,
                   xticks_fontsize=20,
                   xlabel_fontsize=26,
                   ylabel_fontsize=26):
    '''
    Given the path to the lines_data.csv file, that should be stored in the
    same folder as the MusicXML scores of the Jingju Music Scores Collection,
    it computes the melodic length for singing one syllable, measured either as
    number of notes or as aggregated quarterLength duration of those notes. If
    a path to an image file is given, a plot is returned. If for any of the
    input instances no line is retrieved, a warning message indicates so.
    
    Parameters:
    - linesData -- str, path to the lines_data.csv file
    - hd -- [str], list of role types
    - sq -- [str], list of shengqiang
    - bs -- [str], list of banshi
    - ju -- [str], list of line types
    - filename -- str, path for saving the returned plot as an image file. If
          None given, no plot is returned
    - includeGraceNotes -- bool, if True, grace notes are computed. If False,
          grace notes are ignored
    - notesOrDuration -- str, it takes two values. If 'notes' is input, it
          computes the melodic density in terms of number of notes per,
          syllable, if 'duration' is input, it computes the melodic density in
          terms of aggregated quarterLength duration of the notes per syllable.
    - xticks_fontsize -- int, size of the font for the x axis' ticks
    - yticks_fontsize -- int, size of the font for the y axis' ticks
    - xLabel_fontsize -- int, size of the font for the x axis' label
    - yLabel_fontsize -- int, size of the font for the y axis' label
    
    It returns data for each of the scores from which a line is retrieved, as
    well as for the average of all scores. These data are returned in a
    dictionary with the following structure:
    - keys: str, the numerical index of the score in the plot, and 'Avg' for
          the average of all scores
    - values: a dictionary with the following key/value pairs:
          - 'score': str -- path to the corresponding score (this pair is
                absent in the results for 'Avg')
          - 'median': float -- median of the melodic density
          - 'Q1': float -- first quartile
          - 'Q3': float -- third quartile
          - 'lower fence': float
          - 'upper fence': float
          - 'outliers': [float]
    If a path to a file is input to the filename parameter, an image of a
    boxplot is also returned.
    
    For example:
    >>> melodicDensity(ln, hd=['dan'], sq=['xipi'], bs=['erliu'])
    
    Retrieving lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    
    Computing melodic density...
    Processing scores:
            Parsing daxp-ChunQiuTing-SuoLinNang.xml
            Parsing daxp-QiaoLouShang-HuangShanLei.xml
    Melodic density computed.
    {'1': {'Q1': 3.0,
      'Q3': 6.0,
      'lower fence': 1.0,
      'median': 4.0,
      'outliers': [17, 15, 15],
      'score': '../../Jingju-Music-Scores/MusicXML scores/daxp-ChunQiuTing-SuoL
    inNang.xml',
      'upper fence': 10.0},
     '2': {'Q1': 2.0,
      'Q3': 5.0,
      'lower fence': 1.0,
      'median': 3.0,
      'outliers': [19, 12, 14],
      'score': '../../Jingju-Music-Scores/MusicXML scores/daxp-QiaoLouShang-Hua
    ngShanLei.xml',
      'upper fence': 8.0},
     'Avg': {'Q1': 2.0,
      'Q3': 5.5,
      'lower fence': 1.0,
      'median': 4.0,
      'outliers': [17, 15, 15, 19, 12, 14],
      'score': 'average',
      'upper fence': 10.0}}
    '''
    
    material = collectLineMaterial(linesData, hangdang=hd, shengqiang=sq,
                                   banshi=bs, judou=ju)

    while notesOrDuration not in ['notes', 'Notes', 'duration', 'Duration']:
        message = '\nERROR: The value given for the notesOrDuration parameter'\
                  ' is invalid. Please enter either "notes" or "duration" (to'\
                  ' quit the program, please type "stop"): '
        ans = input(message)
        if ans == 'stop':
            exit()
        else:
            notesOrDuration = ans

    syllables = []
    totalCount = []
    accumulatedCount = []
    scores = []
    results = {}

    print('\nComputing melodic density...\nProcessing scores:')

    for score in material[1:]:
        # Loading the score to get the parts list
        scorePath = score[0]
        scores.append(scorePath)
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print('\tParsing ' + scoreName)
        localCount = []
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notesAndRests.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                openParenthesis = False
                graceNote = False
                for i in range(len(segment)):
                    n = segment[i]
                    if notesOrDuration == 'notes':
                        value = 1
                    else:
                        value = n.quarterLength
                    if n.isRest: continue
                    if n.quarterLength==0:
                        if not includeGraceNotes: continue
                        j = 1
                        while (i+j<len(segment) and
                               segment[i+j].quarterLength==0):
                            j += 1
                        if i+j == len(segment): continue
                        n2 = segment[i+j]
                        if n2.hasLyrics():
                            if (('（' in n2.lyric) or ('）' in n2.lyric) or
                                openParenthesis):
                                localCount[-1] += value
                                accumulatedCount[-1] += value
                            else:
                                if graceNote:
                                    localCount[-1] += value
                                    accumulatedCount[-1] += value
                                else:
                                    localCount.append(value)
                                    accumulatedCount.append(value)
                                    syllables.append(n2.lyric)
                                    graceNote = True
                        else:
                            localCount[-1] += value
                            accumulatedCount[-1] += value
                    else:
                        if n.hasLyrics():
                            # Check if the lyric is a padding syllable
                            if ('（' in n.lyric) and ('）' in n.lyric):
                                localCount[-1] += value
                                accumulatedCount[-1] += value
                            elif ('（' in n.lyric) and ('）' not in n.lyric):
                                localCount[-1] += value
                                accumulatedCount[-1] += value
                                openParenthesis = True
                            elif ('（' not in n.lyric) and ('）' in n.lyric):
                                localCount[-1] += value
                                accumulatedCount[-1] += value
                                openParenthesis = False
                            else:
                                if openParenthesis:
                                    localCount[-1] += value
                                    accumulatedCount[-1] += value
                                elif graceNote:
                                    localCount[-1] += value
                                    accumulatedCount[-1] += value
                                    graceNote = False
                                else:
                                    localCount.append(value)
                                    accumulatedCount.append(value)
                                    syllables.append(n.lyric)
                        else:
                            localCount[-1] += value
                            accumulatedCount[-1] += value
        totalCount.append(localCount)
    print('Melodic density computed.')

    totalCount.append(accumulatedCount)
    scores.append('average')

    xLabels = [str(i) for i in range(1, len(totalCount))]
    xLabels.append('Avg')

    for i in range(len(xLabels)):
        results[xLabels[i]] = {}
        results[xLabels[i]]['score'] = scores[i]

    plt.figure()    
    data = plt.boxplot(totalCount)

    # Collect all statistical information in the results dictionary
    limits = []
    for i in range(len(data['medians'])):
        limits.append(np.mean(data['medians'][i].get_xdata()))
        bp = results[xLabels[i]] # bp: boxplot
        bp['median'] = data['medians'][i].get_ydata()[0]
        bp['Q1'] = data['boxes'][i].get_ydata()[1]
        bp['Q3'] = data['boxes'][i].get_ydata()[2]
        bp['lower fence'] = data['caps'][i*2].get_ydata()[1]
        bp['upper fence'] = data['caps'][i*2+1].get_ydata()[1]
        bp['outliers'] = data['fliers'][i].get_ydata().tolist()

    plt.xticks(range(1, len(totalCount)+1), xLabels, fontsize=xticks_fontsize)
    plt.yticks(fontsize=yticks_fontsize)
    plt.axvline(x=len(totalCount)-0.5, ls='--', color='red')
    if notesOrDuration == 'duration':
        plt.ylim(0, 27)
        plt.ylabel('Quarter length duration', fontsize=ylabel_fontsize)
    elif notesOrDuration == 'notes':
        plt.ylim(0, 70)
        plt.ylabel('Number of notes', fontsize=ylabel_fontsize)
    plt.xlabel('Sample scores', fontsize=xlabel_fontsize)
    plt.tight_layout()

    if filename != None:
        print('\nPlotting...')
        plt.savefig(filename)
#        plt.show()
        print('"' + filename + '" plotted and saved.')

    return results



###############################################################################
## AUXILIARY FUNCTIONS                                                       ##
###############################################################################

def checkInput(value, element):
    '''
    It takes a list of instances of a given element of the jingju musical
    system and evaluates if the input instances are correct for being used in
    the pitchHistogram, pitchHistogramLineJudou, intervalHistogram, and
    melodicDensity functions. If a given instance is incorrect, it asks the
    user for a valid input.
    
    Parameters:
    - value -- a list with the instances for a given element of the jingju
          musical system
    - element -- the corresponding element of the jingju musical system, with
          the following abbreviations: 'hd' for role type, 'sq' for shengqiang,
          'bs' for banshi, and 'ju' for line type
    
    It returns a list with valid instances of the given element to be used in
    the aforementioned functions.
    
    For example:
    >>> checkInput(['erhuan', 'xipi'], 'sq')
    
    ACTION REQUIRED: "erhuan" is not a valid shengqiang. Valid inputs are erhua
    ng and xipi. Please enter a new input, "skip" to ignore this input, or "sto
    p" to quit the program: erhuang
    ['erhuang', 'xipi']
    '''
    corrects = {'hd': ('hangdang', ['laosheng', 'dan']),
                'sq': ('shengqiang', ['erhuang', 'xipi']),
                'bs': ('banshi', ['manban', 'sanyan', 'zhongsanyan',
                                  'kuaisanyan', 'yuanban', 'erliu', 'liushui',
                                  'kuaiban']),
                'ju': ('judou', ['s', 's1', 's2', 'x'])}

    to_skip = []

    for i in range(len(value)):
        inputs = ''
        correct = corrects[element][1] 
        for j in range(len(correct)-1):
            inputs += correct[j] + ', '
        inputs = inputs[:-2] + ' and ' + correct[-1]
        while value[i] not in correct:
            error = True
            message = '\nACTION REQUIRED: "' + value[i] + '" is not a valid '+\
                      corrects[element][0] + '. Valid inputs are ' + inputs +\
                      '. Please enter a new input, "skip" to ignore '\
                      'this input, or "stop" to quit the program: '
            ans = input(message)
            if ans == 'stop' or ans == 'Stop':
                exit()
            elif ans == 'skip' or ans == 'Skip':
                to_skip.insert(0, i)
                break
            else:
                value[i] = ans
                
    if len(to_skip) == len(value):
        message = '\nERROR: after skipping incorrect values no input for ' +\
                  corrects[element][0] + ' is left. The program will exit.'
        print(message)
        exit()

    if len(to_skip) > 0:
        for k in to_skip:
            value.pop(k)
    
    return value



def checkInput_cn(hangdang, shengqiang, banshi):
    '''
    It takes a list of instances for role type, shengqiang and banshi, and
    evaluates if they are valid to be used in the cadentialNotes function. If a
    given instance is incorrect, it asks the user for a valid input.
    
    Parameters:
    - hangdang -- a list of role type instances
    - shengqiang -- a list of shengqiang instances
    - banshi -- a list of banshi instances
    
    It returns three lists with valid instances for respectively role type,
    shengqiang and banshi to be used in the cadentialNotes function.
    
    For example:
    >>> checkInput_cn(['dan'], ['erhuang, xipi'], ['yuanban', 'erliu'])
    
    ERROR: Invalid shengqiang. This function only takes either "xipi" or "erhua
    ng". Which shengqiang do you want to analyse? (To quit the program, please 
    type "stop"): xipi
    (['dan'], ['xipi'], ['yuanban', 'erliu'])
    '''
    
    # Check that the inputted parameters are correct
    ## Check hangdang is only one
    if len(hangdang) > 1:
        n = str(len(hangdang))
        message = '\nWARNING: you inputted ' + n + ' hangdang. This function '\
                  'might return not musically meaningful results for more '\
                  'than one hangdang. If you want to continue with ' + n +\
                  ' hangdang please type "continue". Otherwise, please type '\
                  'which hangdang you want to analyse. (To quit the program,'\
                  ' please type "stop"): '
        ans = input(message)
        if ans == 'stop':
            exit()
        elif ans == 'continue' or ans == 'Continue':
            hangdang = checkInput(hangdang, 'hd')
        else:
            hangdang = checkInput([ans], 'hd')

    ## Check shengqiang is correct
    
    while shengqiang not in [['xipi'], ['erhuang']]:
        message = '\nERROR: Invalid shengqiang. This function only takes '\
                  'either "xipi" or "erhuang". Which shengqiang do you want '\
                  'to analyse? (To quit the program, please type "stop"): '
        ans = input(message)
        if ans == 'stop' or ans == 'Stop':
            exit()
        else:
            shengqiang = [ans]

    ##
    banshi = checkInput(banshi, 'bs')
    
    return hangdang, shengqiang, banshi



def findVoiceParts(score):
    '''
    It takes a score and searches which of the parts is the one containing
    lyrics, and therefore, the one containing singing voice.
    
    Parameter:
    - score -- a music21.strem.Score object
    
    It returns a list with all the parts that contain lyrics
    
    For example:
    >>> import music21
    >>> s = music21.converter.parse('sdxp-WoHeNi-SiLangTanMu.xml')
    >>> findVoiceParts(s)
    [<music21.stream.Part Piano>, <music21.stream.Part Piano>]
    '''

    voiceParts = []

    for p in score.parts:
        if len(p.flat.notes) == 0: continue
        i = 0
        n = p.flat.notes[i]
        while n.quarterLength == 0:
            i += 1
            n = p.flat.notes.stream()[i]
        if n.hasLyrics():
                if p.hasElementOfClass('Instrument'):
                    p.remove(p.getInstrument())
                voiceParts.append(p)
    return voiceParts



def floatOrFraction(strValue):
    '''
    It takes a string with a numerical value and analyses if it is a float or
    a fractions.Fraction object.
    
    Parameter:
    - strValue -- str, a numercial value
    
    It returns a flot or a fractions.Fraction object. If the input is an empty
    string, it returns None
    
    For example:
    >>> floatOrFraction('1277/6')
    Fraction(1277, 6)
    >>> floatOrFraction('164')
    164.0
    >>> floatOrFraction('')
    >>> 
    '''
    if '/' in strValue:
        numerator = int(strValue.split('/')[0])
        denominator = int(strValue.split('/')[1])
        value = fractions.Fraction(numerator, denominator)
    elif len(strValue) == 0:
        value = None
    else:
        value = float(strValue)

    return value



def plottingParameters(material, count, yValues):
    '''
    It takes the dictionary returned by either the collectLineMaterial or
    collectLineJudouMaterial functions, a normalization method a list with non
    normalized values and it normalizes these values according to the given
    method, as well as it establishes some stylistic elements for plotting.
    
    Parameters:
    - material -- the dictionary returned by either the collectLineMaterial or
          the collectLineJudouMaterial functions
    - count -- str, either 'sum' for normalizing the results to the summation
          of all the computed values, 'max' for normalizing the results to the
          maximum computed value, and 'abs' for no normalization
    - yValues -- numpy.ndarray, a numpy array with the non normalized values
    
    It returns the following outputs:
    - a numpy.ndarray with the normalized values
    - a tuple of integers with the limits for the x axis of a matplotlib.pyplot
          plot
    - a string with a label for the y axis of a matplotlib.pyplot plot
    - a string with a hex color code for the color of the bars of a
          matplotlib.pyplot bar plot
    - a string with the code for the hatch of the bars of a matplotlib.pyplot
          bar plot
          
    For example:
    >>> import numpy
    >>> material = collectLineMaterial(ln, hangdang=['dan'], shengqiang=['xipi'
    ], banshi=['erliu'])
    
    Retrieving lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    >>> yValues = numpy.array([41,37,195,88,18,27,2,7,2])
    >>> plottingParameters(material, 'sum', yValues)
    (array([ 0.09832134,  0.08872902,  0.4676259 ,  0.21103118,  0.04316547,
             0.0647482 ,  0.00479616,  0.01678657,  0.00479616]),
     (59, 85),
     'Normalized Count',
     '#FF9966',
     '\\')
    '''

    # Determing the handang and shengqiang present
    searchInfo = material[0]
    hdInfo = searchInfo['hd']
    sqInfo = searchInfo['sq']
    # Hangdang information
    if len(hdInfo) == 2:
        hd = 'sd'
    else:
        if hdInfo[0] == 'laosheng':
            hd = 'ls'
        elif hdInfo[0] == 'dan':
            hd = 'da'
    # Shengqiang information
    if len(sqInfo) == 2:
        sq = 'ex'
    else:
        if sqInfo[0] == 'erhuang':
            sq = 'eh'
        elif sqInfo[0] == 'xipi':
            sq = 'xp'

    # Color, hatch and limits codes
    colors = {'ls':'#66CCFF', 'da':'#FF9966', 'sd':'#B2B2B2'}
    hatches = {'eh':'/', 'xp':'\\', 'ex':'x'} # hatch for the bars
    xLimits = {'ls':(54, 76), 'da':(59, 85), 'sd':(54,85)}

    # Setting x limits
    limX = xLimits[hd]

    # Setting y limits and y label
    limY = None

    # Normalising, if requested
    if count == 'sum':
        yValues = yValues / float(sum(yValues))
        yLabel = 'Normalized Count'
    elif count == 'max':
        yValues = yValues / float(max(yValues))
        yLabel = 'Normalized Count'
    else:
        yLabel = 'Count'

    # Setting bar color
    col = colors[hd]

    # Setting bar hatch
    h = hatches[sq]

    return yValues, limX, yLabel, col, h



def plotting(filename, xPositions, xLabels, yValues, title=None, limX=None,
             xLabel=None, limY=None, yLabel=None, col=None, h=None,
             scaleGuides=False, width=0.8, title_fontsize=26,
             xticks_fontsize=20, yticks_fontsize=18, xLabel_fontsize=26,
             yLabel_fontsize=26):
    '''
    It takes all the parameters needed to plot a matplotlib.pyplot bar plot.
    This function is used in the pitchHistogram, pitchHistogramLineJudou, and
    intervalHistogram functions.
    
    Parameters:
    - filename -- str, path to the file to save the plot
    - xPositions -- numpy.ndarray, integers with the x axis values
    - xLabels -- [str], labels for the x axis ticks
    - yValues -- numpy.ndarray, floats with the y axis values
    - title -- str, title for the plot
    - limX -- (int), limits for the x axis
    - xLabel -- str, label for the x axis
    - limY -- [float], limits for the y axis
    - yLabel -- str, label for the y axis
    - col -- str, hex color code for the bars
    - h -- str, hatch code for the bars
    - scaleGuides -- bool, True for displaying vertical lines for first and
          fifth degrees
    - width -- float, width of the bars
    - title_fontsize -- int, size of the font for the plot's title
    - xticks_fontsize -- int, size of the font for the x axis' ticks
    - yticks_fontsize -- int, size of the font for the y axis' ticks
    - xLabel_fontsize -- int, size of the font for the x axis' label
    - yLabel_fontsize -- int, size of the font for the y axis' label
    
    It returns an image file saved in the path input in the filename parameter.
    '''

    plt.figure()
    plt.bar(xPositions, yValues, width, linewidth=0, zorder=1,
            color = col,
            hatch = h)
    if scaleGuides:
        plt.axvline(x=64+width/2, color='red', zorder=0) # Tonic line
        plt.axvline(x=76+width/2, color='red', ls='--', zorder=0) # 8ve tonic
        plt.axvline(x=59+width/2, color='gray', ls=':', zorder=0) # Fifth
        plt.axvline(x=71+width/2, color='gray', ls=':', zorder=0) # Fifth
        plt.axvline(x=83+width/2, color='gray', ls=':', zorder=0) # Fifth
    for yValue in yValues:
        plt.axhline(y=yValue, color='gray', ls=':', zorder=0)
    plt.xticks(xPositions + width/2, xLabels, rotation=90,
               fontsize=xticks_fontsize)
    plt.yticks(fontsize=yticks_fontsize)
    if limX != None:
        plt.xlim(limX[0]-(1-width), limX[1]+1)
    else:
        plt.xlim(xPositions[0]-(1-width), xPositions[-1]+1)
    if limY != None:
        plt.ylim(limY[0], limY[1])
    if xLabel != None:
        plt.xlabel(xLabel, fontsize=xLabel_fontsize)
    if yLabel != None:
        plt.ylabel(yLabel, fontsize=yLabel_fontsize)
    if title != None:
        plt.title(title, fontsize=title_fontsize)
    plt.tight_layout()
    plt.savefig(filename)
#    plt.show()

    print('"' + filename + '" plotted and saved.')



def printingFound(rubric, hd, sq, bs, ju, found_lines):
    '''
    It checks if the collectLineMaterial and collectLineJudouMaterial functions
    retrieve lines for all the combinations of the input data, and it prints a
    message related to the found lines.
    
    Parameters:
    - rubric -- dict, first element of the list returned by the
          collectLineMaterial and the collectLineJudouMaterial functions
    - hd -- [str], list of role types
    - sq -- [str], list of shengqiang
    - bs -- [str], list of banshi
    - ju -- [str], list of line types
    - found_lines -- int, number of lines retrieved by the collectLineMaterial
          and the collectLineJudouMaterial functions
          
    It prints a message to the console with the number of lines retrieved, and,
    in case, a warning message for the instances for which no lines are
    retrieved.
    '''
    
    if found_lines == 0:
        message = '\nALERT: no lines found for any combination of the '\
                  'elements inputted. The program will exit.'
        print(message)
        exit()

    to_check = [(hd, 'hd'), (sq, 'sq'), (bs, 'bs'), (ju, 'ju')]
    found = []
    not_found = '\nWARNING: no results found for'
    nothing = 0
    for element in to_check:
        retrieved = rubric[element[1]]
        for given in element[0]:
            if given not in retrieved:
                not_found += '\n\t' + given
            else:
                found.append(given)

    if len(found) == 4:
        to_print = '\n' + str(found_lines) + ' lines were retrieved for the '\
                   'combination of '
    else:
        to_print = '\n' + str(found_lines) + ' lines were retrieved for '\
                   'combinations of '
    for item in range(len(found)-1):
        to_print += found[item] + ', '
    to_print = to_print[:-2] + ' and ' + found[-1] + '.'
    print(to_print)

    if len(not_found) > 30:
        print(not_found)



def findCadentialNotes(linesData, hd, sq, bs, ju, includeGraceNotes=True):
    '''
    Given the path to the lines_data.csv file, that should be stored in the
    same folder as the MusicXML scores of the Jingju Music Scores Collection,
    it retrieves all the pitches that appear as cadential notes for the three
    sections of the lines that meet the input criteria.
    
    Parameters:
    - linesData -- str, path to the lines_data.csv file
    - hd -- [str], list of role types
    - sq -- [str], list of shengqiang
    - bs -- [str], list of banshi
    - ju -- [str], list of line types
    - includeGraceNotes -- bool, if True, grace notes are also computed. If
          False, grace notes are ignored
    
    It returns two lists:
    - [str], a list with the name of all the pitches that appear as cadential
          notes for the three sections of the retrieved lines
    - [array([float])], a list with a numpy array for each of the pitches of
          the previous list and in the same order. They contain three floats,
          accounting for the percentage that the corresponding pitch appears as
          cadential note in the three line sections
    
    For example:
    >>> findCadentialNotes(ln, ['dan'], ['xipi'], ['erliu'], ['s'])
    
    Retrieving sections for lines that meet the given criteria...
    
    6 lines were retrieved for the combination of dan, xipi, erliu and s.
    
    Processing scores:
            Parsing daxp-ChunQiuTing-SuoLinNang.xml
            Parsing daxp-QiaoLouShang-HuangShanLei.xml
    (['F#4', 'G#4', 'B4', 'C#5'],
     [array([  0.        ,  33.33333333,   0.        ]),
      array([ 33.33333333,  16.66666667,   0.        ]),
      array([ 66.66666667,  33.33333333,  83.33333333]),
      array([  0.        ,  16.66666667,  16.66666667])])
    '''
    
    # Collect material
    material = collectLineJudouMaterial(linesData, hangdang=hd, shengqiang=sq,
                                        banshi=bs, judou=ju)
    
    # Find cadential notes
    cadNotCount = [{}, {}, {}]
    
    print('\nProcessing scores:')

    for score in material[1:]:
        scorePath = score[0]
        loadedScore = converter.parse(scorePath)
        scoreName = scorePath.split('/')[-1]
        print('\tParsing ' + scoreName)
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notesAndRests.stream()
            # Find segments to analyze in the current part
            for line in score[partIndex]:
                for judou in range(len(line)):
                    if len(line[judou]) == 0: continue
                    start = line[judou][0]
                    end = line[judou][1]
                    segment = notes.getElementsByOffset(start, end)
                    i = -1
                    lastNote = segment[i]
                    while lastNote.isRest:
                        i += -1
                        lastNote = segment[i]
                    if includeGraceNotes:
                        cadenceNote = lastNote.nameWithOctave
                    else:
                        while lastNote.quarterLength == 0:
                            print('\t(Grace note omitted in ' + scoreName +\
                                  ', ' + str(partIndex) + ')')
                            i += -1
                            lastNote = segment[i]
                        cadenceNote = lastNote.nameWithOctave
                    sec = cadNotCount[judou]
                    sec[cadenceNote] = sec.get(cadenceNote, 0) + 1

    noteNames = {}

    for secCount in cadNotCount:
        for noteName in secCount.keys():
            noteNames[pitch.Pitch(noteName).midi] = noteName

    sortedNoteNames = [noteNames[j] for j in sorted(noteNames.keys())]

    for secCount in cadNotCount:
        counts = np.array([k for k in secCount.values()])
        toPerCent = 100 / sum(counts)
        for noteName in secCount:
            secCount[noteName] = secCount[noteName] * toPerCent

    sortedValues = []

    for noteName in sortedNoteNames:
        row = []
        for secCount in cadNotCount:
            row.append(secCount.get(noteName, 0))
        sortedValues.append(np.array(row))

    return sortedNoteNames, sortedValues
    


def getAmbitus(material):
    '''
    Given the list returned by the collectLineMaterial function it computes the
    overall ambitus for all the retrieved lines.
    
    It returns a music21.interval.Interval corresponding to the ambitus.
    
    For example:
    >>> material = collectLineMaterial(ln, hangdang=['dan'], shengqiang=['xipi'
    ], banshi=['erliu'])
    
    Retrieving lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    >>> getAmbitus(material)
    daxp-ChunQiuTing-SuoLinNang.xml parsed
    daxp-QiaoLouShang-HuangShanLei.xml parsed
    Ambitus: Perfect Eleventh, from D#4 to G#5
    <music21.interval.Interval P11>
    '''

    ambitusStart = None
    ambitusEnd = None

    for score in material[1:]:
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notes.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                segmentAmbitus = segment.analyze('ambitus')
                if ambitusStart==None and ambitusEnd==None:
                    ambitusStart = segmentAmbitus.noteStart
                    ambitusEnd = segmentAmbitus.noteEnd
                else:
                    if segmentAmbitus.noteStart.midi < ambitusStart.midi:
                        ambitusStart = segmentAmbitus.noteStart
                    if segmentAmbitus.noteEnd.midi > ambitusEnd.midi:
                        ambitusEnd = segmentAmbitus.noteEnd

    ambitusInterval = interval.Interval(ambitusStart, ambitusEnd)

    print('Ambitus:', ambitusInterval.niceName + ', from',
          ambitusStart.nameWithOctave, 'to', ambitusEnd.nameWithOctave)

    return ambitusInterval



def findScoreByPitchThreshold(material, thresholdPitch, lowHigh):
    '''
    Given the list returned by the collectLineMaterial function and a threshold
    pitch, it looks for the scores contained in the input list in which the
    lines retrieved by the collectLineMaterial function contain pitches higher
    or lower than the given pitch threshold.
    
    Parameters:
    - material -- list, the list returned by the collectLineMaterial function
    - thresholdPitch -- int, midi value of the threshold pitch
    - lowHigh -- str, it takes two values, either 'low' or 'high'. If 'low', it
          searches for pitches lower than the threshold, if 'high', it searches
          for pitches higher than the threshold
    
    It returns a list with the file names of the scores in which pitches that
    go beyond the given threshold are found.
    
    For example:
    >>> material = collectLineMaterial(ln, hangdang=['dan'], shengqiang=['xipi'
    ], banshi=['erliu'])
    
    Retrieving lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    >>> findScoreByPitchThreshold(material, 79, 'high')
    daxp-ChunQiuTing-SuoLinNang.xml parsed
    daxp-QiaoLouShang-HuangShanLei.xml parsed
    Done!
    ['daxp-QiaoLouShang-HuangShanLei.xml']
    '''

    scores = []

    for score in material[1:]:
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notes.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                segmentAmbitus = segment.analyze('ambitus')
                ambitusStart = segmentAmbitus.noteStart.midi
                ambitusEnd = segmentAmbitus.noteEnd.midi
                if lowHigh == 'low':
                    if ambitusStart < pitch.Pitch(thresholdPitch).midi:
                        if scoreName not in scores:
                            scores.append(scoreName)
                if lowHigh == 'high':
                    if ambitusEnd > pitch.Pitch(thresholdPitch).midi:
                        if scoreName not in scores:
                            scores.append(scoreName)

    print('Done!')

    return scores



def findScoreByPitch(material, pitchList):
    '''
    Given the list returned by the collectLineMaterial function and a list of
    pitches, it searches for the scores in which lines retrieved by the
    collectLineMaterial contain any of the input pitches. If a match is found,
    the corresponding score is open in the display format defined by the user
    in music21 with the matching pitches in red.
    
    Parameters:
    - material -- list, the list returned by the collectLineMaterial function
    - pitchList -- [str], a list of pitches in the format returned by the
          nameWithOctave method of music21.note.Note objects
    
    It returns a list with the paths of the scores for which a match is found.
    
    For example:
    >>> material = collectLineMaterial(ln, hangdang=['dan'], shengqiang=['xipi'
    ], banshi=['erliu'])
    
    Retrieving lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    >>> findScoreByPitch(material, ['G#5', 'F#5'])
    daxp-ChunQiuTing-SuoLinNang.xml parsed
            6 samples of F#5 found in this score
            Showing daxp-ChunQiuTing-SuoLinNang.xml
    daxp-QiaoLouShang-HuangShanLei.xml parsed
            1 samples of G#5 found in this score
            7 samples of F#5 found in this score
            Showing daxp-QiaoLouShang-HuangShanLei.xml
    ['../../Jingju-Music-Scores/MusicXML scores/daxp-ChunQiuTing-SuoLinNang.xml
    ', '../../Jingju-Music-Scores/MusicXML scores/daxp-QiaoLouShang-HuangShanLe
    i.xml']
    '''

    scores = []

    for score in material[1:]:
        showScore = False
        pitchesFound = {}
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notes.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                for n in segment:
                    noteName = n.nameWithOctave
                    if noteName in pitchList:
                        n.color = 'red'
                        pitchesFound[noteName] = pitchesFound.get(noteName,0)+1
                        showScore = True
                        if scorePath not in scores:
                            scores.append(scorePath)
        if showScore:
            for p in pitchesFound:
                print('\t' + str(pitchesFound[p]), 'samples of', p,
                  'found in this score')
            print('\tShowing', scoreName)
            loadedScore.show()

    return scores



def findScoreByInterval(material, intvlList, directedInterval=False,
                 silence2ignore=0.25, ignoreGraceNotes=False):
    '''
    Given the list returned by the collectLineMaterial function and a list of
    intervals, it searches for the scores in which lines retrieved by the
    collectLineMaterial contain any of the input intervals. If a match is
    found, the corresponding score is open in the display format defined by the
    user in music21 with the matching intervals in red.
    
    Parameter:
    - material -- list, the list returned by the collectLineMaterial function
    - intvlList -- [str], a list of intervals in the format returned by the
          name (if directedInterval = False) or directedName (if
          directedInterval = True) methods of music21.interval.Interval objects
    - directedInterval -- bool, if False, the direction of the interval
          (ascending or descending) is not considered. If True, the direction
          of the interval is considered
    - silence2ignore -- float, establishes the quarterLength duration of a rest
          between two notes to be ignored for the computation of the interval
          that those two notes form
    - ignoreGraceNotes -- bool, if True, grace notes are ignored. If False,
          grace notes are considered for the computation of intervals
    
    It returns a list with the paths of the scores for which a match is found.
    
    For example:
    >>> material = collectLineMaterial(ln, hangdang=['dan'], shengqiang=['xipi'
    ], banshi=['erliu'])
    
    Retrieving lines that meet the given criteria...
    
    12 lines were retrieved for combinations of dan, xipi, erliu, s and x.
    
    WARNING: no results found for
            s1
            s2
    >>> findScoreByInterval(material, ['m3'])
    daxp-ChunQiuTing-SuoLinNang.xml parsed
            43 samples of m3 found in this score
            Showing daxp-ChunQiuTing-SuoLinNang.xml
    daxp-QiaoLouShang-HuangShanLei.xml parsed
            45 samples of m3 found in this score
            Showing daxp-QiaoLouShang-HuangShanLei.xml
    ['daxp-ChunQiuTing-SuoLinNang.xml', 'daxp-QiaoLouShang-HuangShanLei.xml']
    '''

    scores = []

    for score in material[1:]:
        showScore = False
        intvlsFound = {}
        # Loading the score to get the parts list
        scorePath = score[0]
        scoreName = scorePath.split('/')[-1]
        loadedScore = converter.parse(scorePath)
        print(scoreName, 'parsed')
        parts = findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0: continue # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notesAndRests.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                segment = notes.getElementsByOffset(start, end)
                # Count intervals in the current segment
                # Find the last note that is not a grace note
                i = 1
                lastn = segment[-i]
                while lastn.quarterLength == 0:
                    i += 1
                    lastn = segment[-i]

                for j in range(len(segment)-i):
                    n1 = segment[j]
                    if n1.isRest: continue
                    if ignoreGraceNotes:
                        if n1.quarterLength == 0: continue
                    k = 1
                    while True:
                        n2 = segment[j+k]
                        if n2.isRest:
                            if n2.quarterLength <= silence2ignore:
                                k += 1
                            else:
                                n2 = None
                                break
                        elif (n2.quarterLength==0)and(ignoreGraceNotes==True):
                            j += 1
                        else:
                            break
                    if n2==None: continue
                    currentIntvl = interval.Interval(n1, n2)
                    if directedInterval:
                        intvlName = currentIntvl.directedName
                    else:
                        intvlName = currentIntvl.name
                    if intvlName in intvlList:
                        n1.color = 'red'
                        n2.color = 'red'
                        intvlsFound[intvlName] = intvlsFound.get(intvlName,0)+1
                        showScore = True
                        if scorePath not in scores:
                            scores.append(scorePath)
        if showScore:
            for k in intvlsFound:
                print('\t' + str(intvlsFound[k]), 'samples of', k,
                  'found in this score')
            print('\tShowing', scoreName)
            loadedScore.show()

    return scores
