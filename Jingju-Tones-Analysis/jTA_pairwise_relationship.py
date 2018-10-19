# -*- coding: utf-8 -*-



# jTA_pairwise_relationship.py is a script for reproducing with a single command
# line the results presented in Tables 13 and 14 in:
#   Caro Repetto, Rafael (2018) *The musical dimension of Chinese traditional
#   theatre: An analysis from computer aided musicology*, PhD thesis,
#   Universitat Pompeu Fabra, Barcelona, Spain
# regarding the pairwise relationship between linguistic tones and melody in the
# arias from the Jingju Music Scores Collection
# (http://doi.org/10.5281/zenodo.1464653).
#
# Copyright (C) 2018 Music Technology Group, Universitat Pompeu Fabra
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



import jingju_tones_analysis as jTA

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_sq=['erhuang', 'xipi']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']
    default_ju = ['s', 's1', 's2', 'x']

    parser = argparse.ArgumentParser(description='Analyse the pairwise '\
                                                 'relationship of the '\
                                                 'syllable pairs from the '\
                                                 'lines in the Jingju Music '\
                                                 'Scores Collection that '\
                                                 'match the given criteria. '\
                                                 'Print a table in the '\
                                                 'console with the results. '\
                                                 'If a path to a tsv file is '\
                                                 'given to the filename '\
                                                 'argument, the resuts are '\
                                                 'saved in that file.')
    parser.add_argument('path', help='Path to the directory containing the '\
                                     'lines_data.csv file and the MusicXML '\
                                     'scores of the Jingju Music Scores '\
                                     'Collection')
    parser.add_argument('relationship', type=int, nargs=2, help='Notes from '\
                                                                'the melodic '\
                                                                'contour of '\
                                                                'each '\
                                                                'syllable to '\
                                                                'be compared:'\
                                                                ' 0 for the '\
                                                                'first, 1 for'\
                                                                ' the last. '\
                                                                'Two '\
                                                                'arguments '\
                                                                'required, '\
                                                                'one for the '\
                                                                'first '\
                                                                'syllable in '\
                                                                'the pair, '\
                                                                'and one for '\
                                                                'the second')
    parser.add_argument('-hd', '--hangdang', nargs='*', help='Restrict the '\
                                                             'search to the '\
                                                             'given role-type'\
                                                             '. Laosheng and '\
                                                             'dan given by '
                                                             'default',
                        default=default_hd)
    parser.add_argument('-sq', '--shengqiang', nargs='*', help='Restrict the '\
                                                               'search to the'\
                                                               ' given '\
                                                               'shengqiang. '\
                                                               'Erhuang and '\
                                                               'xipi given by'\
                                                               ' default',
                        default=default_sq)
    parser.add_argument('-bs', '--banshi', nargs='*', help='Restrict the '\
                                                           'search to the '\
                                                           'given banshi. All'\
                                                           ' the banshi '\
                                                           'present in the '\
                                                           'Jingju Music '\
                                                           'Scores Collection'\
                                                           ' given by '\
                                                           'default',
                        default=default_bs)
    parser.add_argument('-l', '--line', nargs='*', help='Restrict the search '\
                                                        'to the given line '\
                                                        'types. S1, s2, s and'\
                                                        ' x given by default',
                        default=default_ju)
    parser.add_argument('-fn', '--filename', help='Path and name of the tsv '\
                                                  'file to save the results')
    parser.add_argument('-q', '--query', nargs=2, help='Open the score in the'\
                                                       ' display format '\
                                                       'defined by the user '\
                                                       'in music21 that '\
                                                       'contains lines with '\
                                                       'syllables that '\
                                                       'satisfy the two query'\
                                                       ' criteria, tone and '\
                                                       'contour; for example:'\
                                                       ' 1 A')

    args = parser.parse_args()

    path = args.path
    if path[-1] == '/':
        linesData = path + 'lines_data.csv'
    else:
        linesData = path + '/lines_data.csv'

    r1 = args.relationship[0]
    r2 = args.relationship[1]
    if r1 not in [0, 1] or r2 not in [0, 1]:
        raise Exception('The given values for the relationship argument are '\
                        'not valid')

    q = []
    if args.query != None:
        q = args.query

    material = jTA.toneMaterialPerJudou(linesData, hd=args.hangdang,
                                        sq=args.shengqiang, bs=args.banshi,
                                        ju=args.line)

    jTA.pairwiseRelationship(material, relationship=[r1, r2],
                             filename=args.filename, query=q)
