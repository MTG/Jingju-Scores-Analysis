# -*- coding: utf-8 -*-



# jTA_pairwise_relationship extracts statistical information about the pitch
# height relationship between two consecutive syllables in terms of their
# tonal categories from jingju music scores.
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



import jingju_tones_analysis as jTA

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_sq=['erhuang', 'xipi']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']
    default_ju = ['s', 's1', 's2', 'x']

    parser = argparse.ArgumentParser(description='Print a table with the analysis of the pairwise relationship of the syllables from all the dou that match the given search parameters. If none given, the whole collection is used')
    parser.add_argument('path', help='Path to the directory file with the scores and the lines_data.csv file')
    parser.add_argument('relationship', type=int, nargs=2, help='Notes from the melodic contour of each syllable to be compared: 0 for the first, 1 for the last. Two arguments required, one for the first syllable in the pair, and one for the second')
    parser.add_argument('-hd', '--hangdang', nargs='*', help='Restrict the search to the given role-type. Laosheng and dan given by default', default=default_hd)
    parser.add_argument('-sq', '--shengqiang', nargs='*', help='Restrict the search to the given shengqiang. Erhuang and xipi given by default', default=default_sq)
    parser.add_argument('-bs', '--banshi', nargs='*', help='Restrict the search to the given shengqiang. All of them given by default.', default=default_bs)
    parser.add_argument('-l', '--line', nargs='*', help='Restrict the search to the given shengqiang. S1, s2, s and x given by default', default=default_ju)
    parser.add_argument('-fn', '--filename', help='Path to the file to save the results')
    parser.add_argument('-q', '--query', nargs=2, help='Show the score of the dou that contains pairs that satisfy the two query criteria, pair, given as tone numbers separated by hyphen, and direction; for example: 1-4 A')

    args = parser.parse_args()
    
    path = args.path
    if path[-1] == '/':
        linesData = path + 'lines_data.csv'
    else:
        linesData = path + '/lines_data.csv'
        
    r1 = args.relationship[0]
    r2 = args.relationship[1]
    if r1 not in [0, 1] or r2 not in [0, 1]:
        raise Exception('The given values for the relationship argument are not valid')

    q = []
    if args.query != None:
        q = args.query
    
    material = jTA.toneMaterialPerJudou(linesData, hd=args.hangdang,
                                        sq=args.shengqiang, bs=args.banshi,
                                        ju=args.line)

    jTA.pairwiseRelationship(material, relationship=[r1, r2],
                             filename=args.filename, query=q)