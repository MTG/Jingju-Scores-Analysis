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

import os
import jingju_singing_analysis as jSA
import argparse
import time

# General variables
ls = ['laosheng']
da = ['dan']
ld = ['laosheng', 'dan']
eh = ['erhuang']
xp = ['xipi']
ex = ['erhuang', 'xipi']
yb = ['yuanban', 'erliu']
mb = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan']
kb = ['kuaiban', 'liushui']
bs = ['yuanban', 'erliu', 'manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
      'kuaiban', 'liushui']
s = ['s']
s1 = ['s1']
s2 = ['s2']
x = ['x']
ju = ['s', 's1', 's2', 'x']

# Define lists
figs = ['ph', 'phlj', 'ihd', 'ihn', 'cn', 'mdn', 'mdd']

ph = [['ph-ls.png', ls, ex, bs, ju],
      ['ph-da.png', da, ex, bs, ju],
      ['ph-eh.png', ld, eh, bs, ju],
      ['ph-xp-png', ld, xp, bs, ju],
      ['ph-ls-eh.png', ls, eh, bs, ju],
      ['ph-ls-eh-mb.png', ls, eh, mb, ju],
      ['ph-ls-eh-mb-s1.png', ls, eh, mb, s1],
      ['ph-ls-eh-mb-s2.png', ls, eh, mb, s2],
      ['ph-ls-eh-mb-x.png', ls, eh, mb, x],
      ['ph-ls-eh-yb.png', ls, eh, yb, ju],
      ['ph-ls-eh-yb-s1.png', ls, eh, yb, s1],
      ['ph-ls-eh-yb-s2.png', ls, eh, yb, s2],
      ['ph-ls-eh-yb-x.png', ls, eh, yb, x],
      ['ph-ls-xp.png', ls, xp, bs, ju],
      ['ph-ls-xp-mb.png', ls, xp, mb, ju],
      ['ph-ls-xp-mb-s.png', ls, xp, mb, s],
      ['ph-ls-xp-mb-x.png', ls, xp, mb, x],
      ['ph-ls-xp-yb.png', ls, xp, yb, ju],
      ['ph-ls-xp-yb-s.png', ls, xp, yb, s],
      ['ph-ls-xp-yb-x.png', ls, xp, yb, x],
      ['ph-ls-xp-kb.png', ls, xp, kb, ju],
      ['ph-ls-xp-kb-s.png', ls, xp, kb, s],
      ['ph-ls-xp-kb-x.png', ls, xp, kb, x],
      ['ph-da-eh.png', da, eh, bs, ju],
      ['ph-da-eh-mb.png', da, eh, mb, ju],
      ['ph-da-eh-mb-s1.png', da, eh, mb, s1],
      ['ph-da-eh-mb-s2.png', da, eh, mb, s2],
      ['ph-da-eh-mb-x.png', da, eh, mb, x],
      ['ph-da-eh-yb.png', da, eh, yb, ju],
      ['ph-da-eh-yb-s1.png', da, eh, yb, s1],
      ['ph-da-eh-yb-s2.png', da, eh, yb, s2],
      ['ph-da-eh-yb-x.png', da, eh, yb, x],
      ['ph-da-xp.png', da, xp, bs, ju],
      ['ph-da-xp-mb.png', da, xp, mb, ju],
      ['ph-da-xp-mb-s.png', da, xp, mb, s],
      ['ph-da-xp-mb-x.png', da, xp, mb, x],
      ['ph-da-xp-yb.png', da, xp, yb, ju],
      ['ph-da-xp-yb-s.png', da, xp, yb, s],
      ['ph-da-xp-yb-x.png', da, xp, yb, x],
      ['ph-da-xp-kb.png', da, xp, kb, ju],
      ['ph-da-xp-kb-s.png', da, xp, kb, s],
      ['ph-da-xp-kb-x.png', da, xp, kb, x]]

phlj = [['phlj-ls.png', ls, ex, bs, ju],
        ['phlj-da.png', da, ex, bs, ju],
        ['phlj-eh.png', ld, eh, bs, ju],
        ['phlj-xp-png', ld, xp, bs, ju],
        ['phlj-ls-eh.png', ls, eh, bs, ju],
        ['phlj-ls-eh-mb.png', ls, eh, mb, ju],
        ['phlj-ls-eh-mb-s1.png', ls, eh, mb, s1],
        ['phlj-ls-eh-mb-s2.png', ls, eh, mb, s2],
        ['phlj-ls-eh-mb-x.png', ls, eh, mb, x],
        ['phlj-ls-eh-yb.png', ls, eh, yb, ju],
        ['phlj-ls-eh-yb-s1.png', ls, eh, yb, s1],
        ['phlj-ls-eh-yb-s2.png', ls, eh, yb, s2],
        ['phlj-ls-eh-yb-x.png', ls, eh, yb, x],
        ['phlj-ls-xp.png', ls, xp, bs, ju],
        ['phlj-ls-xp-mb.png', ls, xp, mb, ju],
        ['phlj-ls-xp-mb-s.png', ls, xp, mb, s],
        ['phlj-ls-xp-mb-x.png', ls, xp, mb, x],
        ['phlj-ls-xp-yb.png', ls, xp, yb, ju],
        ['phlj-ls-xp-yb-s.png', ls, xp, yb, s],
        ['phlj-ls-xp-yb-x.png', ls, xp, yb, x],
        ['phlj-ls-xp-kb.png', ls, xp, kb, ju],
        ['phlj-ls-xp-kb-s.png', ls, xp, kb, s],
        ['phlj-ls-xp-kb-x.png', ls, xp, kb, x],
        ['phlj-da-eh.png', da, eh, bs, ju],
        ['phlj-da-eh-mb.png', da, eh, mb, ju],
        ['phlj-da-eh-mb-s1.png', da, eh, mb, s1],
        ['phlj-da-eh-mb-s2.png', da, eh, mb, s2],
        ['phlj-da-eh-mb-x.png', da, eh, mb, x],
        ['phlj-da-eh-yb.png', da, eh, yb, ju],
        ['phlj-da-eh-yb-s1.png', da, eh, yb, s1],
        ['phlj-da-eh-yb-s2.png', da, eh, yb, s2],
        ['phlj-da-eh-yb-x.png', da, eh, yb, x],
        ['phlj-da-xp.png', da, xp, bs, ju],
        ['phlj-da-xp-mb.png', da, xp, mb, ju],
        ['phlj-da-xp-mb-s.png', da, xp, mb, s],
        ['phlj-da-xp-mb-x.png', da, xp, mb, x],
        ['phlj-da-xp-yb.png', da, xp, yb, ju],
        ['phlj-da-xp-yb-s.png', da, xp, yb, s],
        ['phlj-da-xp-yb-x.png', da, xp, yb, x],
        ['phlj-da-xp-kb.png', da, xp, kb, ju],
        ['phlj-da-xp-kb-s.png', da, xp, kb, s],
        ['phlj-da-xp-kb-x.png', da, xp, kb, x]]

ihd = [['ihd-ls.png', ls, ex, bs, ju],
       ['ihd-da.png', da, ex, bs, ju],
       ['ihd-eh.png', ld, eh, bs, ju],
       ['ihd-xp-png', ld, xp, bs, ju],
       ['ihd-ls-eh.png', ls, eh, bs, ju],
       ['ihd-ls-eh-mb.png', ls, eh, mb, ju],
       ['ihd-ls-eh-yb.png', ls, eh, yb, ju],
       ['ihd-ls-xp.png', ls, xp, bs, ju],
       ['ihd-ls-xp-mb.png', ls, xp, mb, ju],
       ['ihd-ls-xp-yb.png', ls, xp, yb, ju],
       ['ihd-ls-xp-kb.png', ls, xp, kb, ju],
       ['ihd-da-eh.png', da, eh, bs, ju],
       ['ihd-da-eh-mb.png', da, eh, mb, ju],
       ['ihd-da-eh-yb.png', da, eh, yb, ju],
       ['ihd-da-xp.png', da, xp, bs, ju],
       ['ihd-da-xp-mb.png', da, xp, mb, ju],
       ['ihd-da-xp-yb.png', da, xp, yb, ju],
       ['ihd-da-xp-kb.png', da, xp, kb, ju]]

ihn = [['ihn-ls.png', ls, ex, bs, ju],
       ['ihn-da.png', da, ex, bs, ju],
       ['ihn-eh.png', ld, eh, bs, ju],
       ['ihn-xp-png', ld, xp, bs, ju],
       ['ihn-ls-eh.png', ls, eh, bs, ju],
       ['ihn-ls-eh-mb.png', ls, eh, mb, ju],
       ['ihn-ls-eh-yb.png', ls, eh, yb, ju],
       ['ihn-ls-xp.png', ls, xp, bs, ju],
       ['ihn-ls-xp-mb.png', ls, xp, mb, ju],
       ['ihn-ls-xp-yb.png', ls, xp, yb, ju],
       ['ihn-ls-xp-kb.png', ls, xp, kb, ju],
       ['ihn-da-eh.png', da, eh, bs, ju],
       ['ihn-da-eh-mb.png', da, eh, mb, ju],
       ['ihn-da-eh-yb.png', da, eh, yb, ju],
       ['ihn-da-xp.png', da, xp, bs, ju],
       ['ihn-da-xp-mb.png', da, xp, mb, ju],
       ['ihn-da-xp-yb.png', da, xp, yb, ju],
       ['ihn-da-xp-kb.png', da, xp, kb, ju]]

cn = [['cn-ls-eh.png', ls, eh, bs],
      ['cn-ls-eh-mb.png', ls, eh, mb],
      ['cn-ls-eh-yb.png', ls, eh, yb],
      ['cn-ls-xp.png', ls, xp, bs],
      ['cn-ls-xp-mb.png', ls, xp, mb],
      ['cn-ls-xp-yb.png', ls, xp, yb],
      ['cn-ls-xp-kb.png', ls, xp, kb],
      ['cn-da-eh.png', da, eh, bs],
      ['cn-da-eh-mb.png', da, eh, mb],
      ['cn-da-eh-yb.png', da, eh, yb],
      ['cn-da-xp.png', da, xp, bs],
      ['cn-da-xp-mb.png', da, xp, mb],
      ['cn-da-xp-yb.png', da, xp, yb],
      ['cn-da-xp-kb.png', da, xp, kb]]

mdn = [['mdn-ls-eh-mb.png', ls, eh, mb, ju],
       ['mdn-ls-eh-mb-s1.png', ls, eh, mb, s1],
       ['mdn-ls-eh-mb-s2.png', ls, eh, mb, s2],
       ['mdn-ls-eh-mb-x.png', ls, eh, mb, x],
       ['mdn-ls-eh-yb.png', ls, eh, yb, ju],
       ['mdn-ls-eh-yb-s1.png', ls, eh, yb, s1],
       ['mdn-ls-eh-yb-s2.png', ls, eh, yb, s2],
       ['mdn-ls-eh-yb-x.png', ls, eh, yb, x],
       ['mdn-ls-xp-mb.png', ls, xp, mb, ju],
       ['mdn-ls-xp-mb-s.png', ls, xp, mb, s],
       ['mdn-ls-xp-mb-x.png', ls, xp, mb, x],
       ['mdn-ls-xp-yb.png', ls, xp, yb, ju],
       ['mdn-ls-xp-yb-s.png', ls, xp, yb, s],
       ['mdn-ls-xp-yb-x.png', ls, xp, yb, x],
       ['mdn-ls-xp-kb.png', ls, xp, kb, ju],
       ['mdn-ls-xp-kb-s.png', ls, xp, kb, s],
       ['mdn-ls-xp-kb-x.png', ls, xp, kb, x],
       ['mdn-da-eh-mb.png', da, eh, mb, ju],
       ['mdn-da-eh-mb-s1.png', da, eh, mb, s1],
       ['mdn-da-eh-mb-s2.png', da, eh, mb, s2],
       ['mdn-da-eh-mb-x.png', da, eh, mb, x],
       ['mdn-da-eh-yb.png', da, eh, yb, ju],
       ['mdn-da-eh-yb-s1.png', da, eh, yb, s1],
       ['mdn-da-eh-yb-s2.png', da, eh, yb, s2],
       ['mdn-da-eh-yb-x.png', da, eh, yb, x],
       ['mdn-da-xp-mb.png', da, xp, mb, ju],
       ['mdn-da-xp-mb-s.png', da, xp, mb, s],
       ['mdn-da-xp-mb-x.png', da, xp, mb, x],
       ['mdn-da-xp-yb.png', da, xp, yb, ju],
       ['mdn-da-xp-yb-s.png', da, xp, yb, s],
       ['mdn-da-xp-yb-x.png', da, xp, yb, x],
       ['mdn-da-xp-kb.png', da, xp, kb, ju],
       ['mdn-da-xp-kb-s.png', da, xp, kb, s],
       ['mdn-da-xp-kb-x.png', da, xp, kb, x]]

mdd = [['mdd-ls-eh-mb.png', ls, eh, mb, ju],
       ['mdd-ls-eh-mb-s1.png', ls, eh, mb, s1],
       ['mdd-ls-eh-mb-s2.png', ls, eh, mb, s2],
       ['mdd-ls-eh-mb-x.png', ls, eh, mb, x],
       ['mdd-ls-eh-yb.png', ls, eh, yb, ju],
       ['mdd-ls-eh-yb-s1.png', ls, eh, yb, s1],
       ['mdd-ls-eh-yb-s2.png', ls, eh, yb, s2],
       ['mdd-ls-eh-yb-x.png', ls, eh, yb, x],
       ['mdd-ls-xp-mb.png', ls, xp, mb, ju],
       ['mdd-ls-xp-mb-s.png', ls, xp, mb, s],
       ['mdd-ls-xp-mb-x.png', ls, xp, mb, x],
       ['mdd-ls-xp-yb.png', ls, xp, yb, ju],
       ['mdd-ls-xp-yb-s.png', ls, xp, yb, s],
       ['mdd-ls-xp-yb-x.png', ls, xp, yb, x],
       ['mdd-ls-xp-kb.png', ls, xp, kb, ju],
       ['mdd-ls-xp-kb-s.png', ls, xp, kb, s],
       ['mdd-ls-xp-kb-x.png', ls, xp, kb, x],
       ['mdd-da-eh-mb.png', da, eh, mb, ju],
       ['mdd-da-eh-mb-s1.png', da, eh, mb, s1],
       ['mdd-da-eh-mb-s2.png', da, eh, mb, s2],
       ['mdd-da-eh-mb-x.png', da, eh, mb, x],
       ['mdd-da-eh-yb.png', da, eh, yb, ju],
       ['mdd-da-eh-yb-s1.png', da, eh, yb, s1],
       ['mdd-da-eh-yb-s2.png', da, eh, yb, s2],
       ['mdd-da-eh-yb-x.png', da, eh, yb, x],
       ['mdd-da-xp-mb.png', da, xp, mb, ju],
       ['mdd-da-xp-mb-s.png', da, xp, mb, s],
       ['mdd-da-xp-mb-x.png', da, xp, mb, x],
       ['mdd-da-xp-yb.png', da, xp, yb, ju],
       ['mdd-da-xp-yb-s.png', da, xp, yb, s],
       ['mdd-da-xp-yb-x.png', da, xp, yb, x],
       ['mdd-da-xp-kb.png', da, xp, kb, ju],
       ['mdd-da-xp-kb-s.png', da, xp, kb, s],
       ['mdd-da-xp-kb-x.png', da, xp, kb, x]]

# Define plotting functions
def plot_ph(linesData, root_folder):
    print('\n\n##############################################################'\
          '#################')
    print('## Ploting pitch histograms                                       '\
          '           ##')
    print('##################################################################'\
          '#############')

    to_print = ''

    ph_folder = 'pitch_histograms'
    folder = root_folder + '/' + ph_folder
    if ph_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the pitch '\
              'histogram figures.')
        os.mkdir(folder)
    else:
        print('\nPitch histogram figures will be saved in the existing folder'\
              ' ' + folder + '.')

    for phi in ph:
        print('\nComputing figure "' + phi[0] + '"')
        fn = folder + '/' + phi[0]
        to_print += phi[0] + '\n'
        ph_results = jSA.pitchHistogram(linesData, hd=phi[1], sq=phi[2],
                                        bs=phi[3], ju=phi[4], filename=fn)
        for line in ph_results:
            to_print += line[0] + ',' + str(line[1]) + '\n'
        print('\n____________________________________________________________'\
          '___________________')

    with open(folder + '/ph_results.csv', 'w') as f:
        f.write(to_print[:-1])



def plot_phlj(linesData, root_folder):
    print('\n\n##############################################################'\
          '#################')
    print('## Ploting pitch histograms for sections in line                  '\
          '           ##')
    print('##################################################################'\
          '#############')

    to_print = ''

    phlj_folder = 'pitch_histograms_sections'
    folder = root_folder + '/' + phlj_folder
    if phlj_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the pitch '\
              'histogram figures.')
        os.mkdir(folder)
    else:
        print('\nPitch histogram figures will be saved in the existing folder'\
              ' ' + folder + '.')

    for phlji in phlj:
        print('\nComputing figure "' + phlji[0] + '"')
        fn = folder + '/' + phlji[0]
        to_print += phlji[0] + '\n'
        phlj_results = jSA.pitchHistogramLineJudou(linesData, hd=phlji[1],
                                                   sq=phlji[2], bs=phlji[3],
                                                   ju=phlji[4], filename=fn)
        for row in range(len(phlj_results[0])):
            to_print += phlj_results[0][row][0] + ',' +\
                        str(phlj_results[0][row][1]) + ',' +\
                        str(phlj_results[1][row][1]) + ',' +\
                        str(phlj_results[2][row][1]) + '\n'
        print('\n____________________________________________________________'\
          '___________________')

    with open(folder + '/phlj_results.csv', 'w') as f:
        f.write(to_print[:-1])



def plot_ihd(linesData, root_folder):
    print('\n\n##############################################################'\
          '#################')
    print('## Ploting histograms of directed intervals                       '\
          '           ##')
    print('##################################################################'\
          '#############')

    to_print = ''

    ihd_folder = 'directed_interval_histograms'
    folder = root_folder + '/' + ihd_folder
    if ihd_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the interval'\
              ' histogram figures.')
        os.mkdir(folder)
    else:
        print('\nInterval histogram figures will be saved in the existing '\
              'folder ' + folder + '.')

    for ihdi in ihd:
        print('\nComputing figure "' + ihdi[0] + '"')
        fn = folder + '/' + ihdi[0]
        to_print += ihdi[0] + '\n'
        ihd_results = jSA.intervalHistogram(linesData, hd=ihdi[1], sq=ihdi[2],
                                            bs=ihdi[3], ju=ihdi[4],
                                            filename=fn, directedInterval=True)
        for line in ihd_results:
            to_print += line[0] + ',' + str(line[1]) + '\n'
        print('\n____________________________________________________________'\
          '___________________')

    with open(folder + '/ihd_results.csv', 'w') as f:
        f.write(to_print[:-1])



def plot_ihn(linesData, root_folder):
    print('\n\n##############################################################'\
          '#################')
    print('## Ploting histograms of not directed intervals                   '\
          '           ##')
    print('##################################################################'\
          '#############')

    to_print = ''

    ihn_folder = 'not_directed_interval_histograms'
    folder = root_folder + '/' + ihn_folder
    if ihn_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the interval'\
              ' histogram figures.')
        os.mkdir(folder)
    else:
        print('\nInterval histogram figures will be saved in the existing '\
              'folder ' + folder + '.')

    for ihni in ihn:
        print('\nComputing figure "' + ihni[0] + '"')
        fn = folder + '/' + ihni[0]
        to_print += ihni[0] + '\n'
        ihn_results = jSA.intervalHistogram(linesData, hd=ihni[1], sq=ihni[2],
                                            bs=ihni[3], ju=ihni[4],
                                            filename=fn,
                                            directedInterval=False)
        for line in ihn_results:
            to_print += line[0] + ',' + str(line[1]) + '\n'
        print('\n____________________________________________________________'\
          '___________________')

    with open(folder + '/ihn_results.csv', 'w') as f:
        f.write(to_print[:-1])



def plot_cn(linesData, root_folder):
    print('\n\n##############################################################'\
          '#################')
    print('## Ploting cadential notes                                        '\
          '           ##')
    print('##################################################################'\
          '#############')

    to_print = ''

    cn_folder = 'cadential_notes'
    folder = root_folder + '/' + cn_folder
    if cn_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the '\
              'cadential notes figures.')
        os.mkdir(folder)
    else:
        print('\nCadential notes figures will be saved in the existing folder'\
              ' ' + folder + '.')

    for cni in cn:
        print('\nComputing figure "' + cni[0] + '"')
        fn = folder + '/' + cni[0]
        to_print += cni[0] + '\n'
        cn_results = jSA.cadentialNotes(linesData, hd=cni[1], sq=cni[2],
                                        bs=cni[3], filename=fn)
        if len(cn_results) == 2:
            to_print += ',Op. line,,,Cl. line,,\n,S1,S2,S3,S1,S2,S3\n'
            ol = cn_results['Op. line']
            cl = cn_results['Cl. line']
            for row in range(len(ol['S1'])):
                to_print += ol['S1'][row][0] + ',' +\
                            str(ol['S1'][row][1]) + ',' +\
                            str(ol['S2'][row][1]) + ',' +\
                            str(ol['S3'][row][1]) + ',' +\
                            str(cl['S1'][row][1]) + ',' +\
                            str(cl['S2'][row][1]) + ',' +\
                            str(cl['S3'][row][1]) + '\n'
        elif len(cn_results) == 3:
            to_print += ',Op. l. 1,,,Op. l. 2,,,Cl. line,,\n,S1,S2,S3,S1,S2,S3,S1,S2,S3\n'
            ol1 = cn_results['Op. l. 1']
            ol2 = cn_results['Op. l. 2']
            cl = cn_results['Cl. l.']
            for row in range(len(ol1['S1'])):
                to_print += ol1['S1'][row][0] + ',' +\
                str(ol1['S1'][row][1]) + ',' +\
                str(ol1['S2'][row][1]) + ',' +\
                str(ol1['S3'][row][1]) + ',' +\
                str(ol2['S1'][row][1]) + ',' +\
                str(ol2['S2'][row][1]) + ',' +\
                str(ol2['S3'][row][1]) + ',' +\
                str(cl['S1'][row][1]) + ',' +\
                str(cl['S2'][row][1]) + ',' +\
                str(cl['S3'][row][1]) + '\n'
        print('\n____________________________________________________________'\
          '___________________')

    with open(folder + '/cn_results.csv', 'w') as f:
        f.write(to_print[:-1])



def plot_mdn(linesData, root_folder):
    print('\n\n##############################################################'\
          '#################')
    print('## Ploting melodic density as notes                               '\
          '           ##')
    print('##################################################################'\
          '#############')

    keys = ['median', 'Q1', 'Q3', 'lower fence', 'upper fence']

    to_print = ''

    mdn_folder = 'melodic_density_notes'
    folder = root_folder + '/' + mdn_folder
    if mdn_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the melodic '\
              'density figures.')
        os.mkdir(folder)
    else:
        print('\nMelodic density figures will be saved in the existing folder'\
              ' ' + folder + '.')

    for mdni in mdn:
        print('\nComputing figure "' + mdni[0] + '"')
        fn = folder + '/' + mdni[0]
        to_print += mdni[0] + '\n'
        mdn_results = jSA.melodicDensity(linesData, hd=mdni[1], sq=mdni[2],
                                         bs=mdni[3], ju=mdni[4], filename=fn,
                                         notesOrDuration='notes')

        to_print += 'index,score,median,Q1,Q3,lower fence,upper fence,'\
                    'outliers\n'
        for i in range(1, len(mdn_results)):
            x = mdn_results[str(i)]
            to_print += str(i) + ',' + x['score'].split('/')[-1] + ','
            for k in keys:
                to_print += str(x[k]) + ','
            for o in x['outliers']:
                to_print += str(o) + ';'
            to_print = to_print[:-1] + '\n'

        to_print += 'Avg' + ',,'
        avg = mdn_results['Avg']
        for k in keys:
            to_print += str(avg[k]) + ','
        for o in avg['outliers']:
            to_print += str(o) + ';'
        to_print = to_print[:-1] + '\n'

        print('\n____________________________________________________________'\
          '___________________')

    with open(folder + '/mdn_results.csv', 'w') as f:
        f.write(to_print[:-1])



def plot_mdd(linesData, root_folder):
    print('\n\n##############################################################'\
          '#################')
    print('## Ploting melodic density as quarter length duration             '\
          '           ##')
    print('##################################################################'\
          '#############')

    keys = ['median', 'Q1', 'Q3', 'lower fence', 'upper fence']

    to_print = ''

    mdd_folder = 'melodic_density_duration'
    folder = root_folder + '/' + mdd_folder
    if mdd_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the melodic '\
              'density figures.')
        os.mkdir(folder)
    else:
        print('\nMelodic density figures will be saved in the existing folder'\
              ' ' + folder + '.')

    for mddi in mdd:
        print('\nComputing figure "' + mddi[0] + '"')
        fn = folder + '/' + mddi[0]
        to_print += mddi[0] + '\n'
        mdd_results = jSA.melodicDensity(linesData, hd=mddi[1], sq=mddi[2],
                                         bs=mddi[3], ju=mddi[4], filename=fn,
                                         notesOrDuration='duration')

        to_print += 'index,score,median,Q1,Q3,lower fence,upper fence,'\
                    'outliers\n'
        for i in range(1, len(mdd_results)):
            x = mdd_results[str(i)]
            to_print += str(i) + ',' + x['score'].split('/')[-1] + ','
            for k in keys:
                to_print += str(x[k]) + ','
            for o in x['outliers']:
                to_print += str(o) + ';'
            to_print = to_print[:-1] + '\n'

        to_print += 'Avg' + ',,'
        avg = mdd_results['Avg']
        for k in keys:
            to_print += str(avg[k]) + ','
        for o in avg['outliers']:
            to_print += str(o) + ';'
        to_print = to_print[:-1] + '\n'

        print('\n____________________________________________________________'\
          '___________________')

    with open(folder + '/mdd_results.csv', 'w') as f:
        f.write(to_print[:-1])



###############################################################################
## PLOTTING                                                                  ##
###############################################################################

if __name__ == '__main__':

    time0 = time.time()

    parser = argparse.ArgumentParser(description='Compute seven different '\
                                                 'types of statistical '\
                                                 'information from the Jingju'\
                                                 ' Music Scores Collections '\
                                                 'according to different line'\
                                                 ' categories. For each type,'\
                                                 ' return a csv file with '\
                                                 'numerical information and a'\
                                                 ' series of related plots.')
    parser.add_argument('linesData', help='Path to the lines_data.csv file, '\
                                          'which should be stored in the same'\
                                          ' folder as the MusicXML scores of '\
                                          'the Jingju Music Scores Collection')
    parser.add_argument('-f', '--figures', nargs='*',
                        choices=figs,
                        help='Select which information type to compute:  ph '\
                             '-- pitch histograms per line; phlj -- pitch '\
                             'histograms per line sections; ihn -- non '\
                             'directed interval histograms; ihd -- directed'\
                             ' interval histograms; cn -- cadential notes; '\
                             'mdn -- melodic density as notes; mdd -- melodic'\
                             ' density as duration. If no argument is passed,'\
                             ' information for all seven types is computed.')
    parser.add_argument('-p', '--path', help='Path to the location where the '\
                                             '"plots" folder containing all '\
                                             'the returned files will be '\
                                             'saved')

    args = parser.parse_args()

    # Create a folder for storing the plots
    if args.path == None:
        p = '.'
    else:
        if args.path[-1] == '/':
            p = args.path[:-1]
        else:
            p = args.path

    root_folder = p + '/plots'

    if 'plots' not in os.listdir(p):
        print('\nThe folder "' + root_folder + '" was created to save the '\
              'figures.')
        os.mkdir(root_folder)
    else:
        print('\nThe figures will be saved in the existing folder "' +\
              root_folder + '".')

    # Define the list of figures to plot
    if args.figures == None:
        to_plot = figs
    else:
        to_plot = args.figures

    # Plot figures
    if 'ph' in to_plot:
        plot_ph(args.linesData, root_folder)

    if 'phlj' in to_plot:
        plot_phlj(args.linesData, root_folder)

    if 'ihd' in to_plot:
        plot_ihd(args.linesData, root_folder)

    if 'ihn' in to_plot:
        plot_ihn(args.linesData, root_folder)

    if 'cn' in to_plot:
        plot_cn(args.linesData, root_folder)

    if 'mdn' in to_plot:
        plot_mdn(args.linesData, root_folder)

    if 'mdd' in to_plot:
        plot_mdd(args.linesData, root_folder)

    # Confirmation message
    print('\n================================================================'\
          '===============')
    print('--- FINISHED! ---')
    print('All the figures plotted and saved correctly.')
    print('(Required time: ' + time.strftime('%H:%M\'%S")',
                                             time.gmtime(time.time()-time0)))
    print('=================================================================='\
          '=============')
