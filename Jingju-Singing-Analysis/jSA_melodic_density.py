# -*- coding: utf-8 -*-



# jSA_melodic_density extracts statistical information about melodic density of
# the singing melody in jingju music scores.
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



import jingju_singing_analysis as jSA

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_sq=['erhuang', 'xipi']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']
    default_ju = ['s', 's1', 's2', 'x']

    parser = argparse.ArgumentParser(description='Plot melodic denstity boxplots for the scores that match the given search criteria. If none given, the whole collection is used')
    parser.add_argument('path', help='Path to the directory file with the scores and the lines_data.csv file')
    parser.add_argument('file', help='Path and name for file to be saved, including extension')
    parser.add_argument('-hd', '--hangdang', nargs='*', help='Restrict the search to the given role-type. Laosheng and dan given by default', default=default_hd)
    parser.add_argument('-sq', '--shengqiang', nargs='*', help='Restrict the search to the given shengqiang. Erhuang and xipi given by default', default=default_sq)
    parser.add_argument('-bs', '--banshi', nargs='*', help='Restrict the search to the given shengqiang. All of them given by default.', default=default_bs)
    parser.add_argument('-l', '--line', nargs='*', help='Restrict the search to the given shengqiang. S1, s2, s and x given by default', default=default_ju)
    parser.add_argument('-gn', '--graceNotes', help='Set if grace notes should be counted. Take True or False. Set True by default', default='True')
    parser.add_argument('-d', '--duration', help='Set the duration output: notes for number of notes, duration for agregated length in quarter notes. Duration given as default', default='duration')
    
    args = parser.parse_args()
    
    path = args.path
    if path[-1] == '/':
        linesData = path + 'lines_data.csv'
    else:
        linesData = path + '/lines_data.csv'
    
    gn = args.graceNotes
    if gn == 'True':
        gn = True
    elif gn == 'False':
        gn = False
    
    material = jSA.collectLineMaterial(linesData, hd=args.hangdang,
                                       sq=args.shengqiang, bs=args.banshi,
                                       ju=args.line)
    jSA.melodicDensity(material, filename=args.file,
                       includeGraceNotes=gn,
                       notesOrDuration=args.duration)

