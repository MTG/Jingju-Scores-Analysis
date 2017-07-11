# -*- coding: utf-8 -*-



# jSA_cadential_notes extracts statistical information about cadential notes
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



import jingju_singing_analysis as jSA

import argparse

if __name__=='__main__':
    # Default values
    default_hd=['laosheng', 'dan']
    default_bs = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan', 'yuanban',
                  'erliu', 'liushui', 'kuaiban']

    parser = argparse.ArgumentParser(description='Plot a bar chart with the percentage of cadential notes for each section of the opening and closing lines in the scores that match the given search criteria')
    parser.add_argument('path', help='Path to the directory file with the scores and the lines_data.csv file')
    parser.add_argument('shengqiang', help='Restrict the search to either erhuang or xipi')
    parser.add_argument('file', help='Path and name for file to be saved, including extension')
    parser.add_argument('-hd', '--hangdang', nargs='*', help='Restrict the search to the given role-type. Laosheng and dan given by default', default=default_hd)
    parser.add_argument('-bs', '--banshi', nargs='*', help='Restrict the search to the given shengqiang. All of them given by default.', default=default_bs)
    parser.add_argument('-gn', '--graceNotes', help='Set if grace notes should be counted. Take True or False. Set True by default', default='True')
    
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
    
if args.shengqiang == 'erhuang':
    material_s1 = jSA.collectJudouMaterial(linesData, args.hangdang,
                                           sq=['erhuang'], bs=args.banshi,
                                           ju=['s1'])
    material_s2 = jSA.collectJudouMaterial(linesData, args.hangdang,
                                           sq=['erhuang'], bs=args.banshi,
                                           ju=['s2'])
    material_x = jSA.collectJudouMaterial(linesData, args.hangdang,
                                          sq=['erhuang'], bs=args.banshi,
                                          ju=['x'])
    judouMaterialList = [material_s1, material_s2, material_x]
    
elif args.shengqiang == 'xipi':
    material_s = jSA.collectJudouMaterial(linesData, args.hangdang,
                                          sq=['xipi'], bs=args.banshi,
                                          ju=['s'])
    material_x = jSA.collectJudouMaterial(linesData,  args.hangdang,
                                          sq=['xipi'], bs=args.banshi,
                                          ju=['x'])
    judouMaterialList = [material_s, material_x]

jSA.cadentialNotes(judouMaterialList, filename=args.file,
                   includeGraceNotes=gn)