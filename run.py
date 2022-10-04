#!/usr/bin/python

import sys
import argparse
import vcf
import json
import logging
from autopvs1 import AutoPVS1

class auto_PVS1 (object):

    def __init__(self, input_name, output_name):

        self._input_name = input_name
        self._output_name = output_name

        self._logger = logging.getLogger("Predict PVS1")
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_hander = logging.StreamHandler()
        stream_hander.setFormatter(formatter)
        self._logger.addHandler(stream_hander)

    def run(self):
        #Read VCF File
        input_file = open(self._input_name,'r')
        vcf_reader = vcf.Reader(input_file)

        #Write VCF File
        output_file = open(self._output_name, 'w')
        vcf_write = vcf.Writer(output_file, vcf_reader) #vcf_reader-> vcf header 가 위치함


        #PARSING & AutoPVS1 command
        for record in vcf_reader:
            CHROM = str(record.CHROM).replace("[","").replace("]","").replace(" ","").replace("chr","").strip()
            POS = str(record.POS).replace("[","").replace("]","").replace(" ","").strip()
            REF = str(record.REF).replace("[","").replace("]","").replace(" ","").strip()
            ALT = str(record.ALT).replace("[","").replace("]","").replace(" ","").strip()
            
            key = CHROM + "-" +  POS + "-" +  REF + "-" + ALT
            
            # demo = AutoPVS1( key, 'hg19')
            # if demo.islof: 
            #     print(demo.hgvs_c, demo.hgvs_p, demo.consequence, demo.pvs1.criterion,
            #     demo.pvs1.strength_raw, demo.pvs1.strength)
            #     pvs1_strength = "PVS1" + "_" + str(demo.pvs1.strength_raw).replace("Strength.","").strip()
            #     print(pvs1_strength)
            #     record.INFO['AutoPVS1'] = pvs1_strength
            try:
                output_list = []
                result = AutoPVS1(key, 'hg19')
                if result.islof:
                    for tmp_transcript in result.total:
                        result_dict = result.total[tmp_transcript]
                        output_list.append('{0}|{1}|{2}|{3}|{4}'.format(tmp_transcript,
                                                                        result_dict['hgvs.c'], result_dict['hgvs.p'],
                                                                        result_dict['consequence'],
                                                                        result_dict['strength_raw'].split('.')[1]))
                    if not output_list == []:
                        record.INFO['AutoPVS1'] = ','.join(output_list)
                        self._logger.info('Complete to predict PVS1 ({0})'.format(key))
                else:
                    self._logger.info('Skip as not PVS1 ({0})'.format(key))
            except:
                self._logger.error('Error to predict PVS1 ({0})'.format(key))
                sys.exit(1)

            vcf_write.write_record(record)

        #VCF File Close
        input_file.close()
        output_file.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='VCF Format Filtering')
    parser.add_argument('--input', type=str, help='VCF input file name', default='None')
    parser.add_argument('--output', type=str, help='VCF output file name', default='None')
    args = parser.parse_args()

    workflow = auto_PVS1(args.input, args.output)
    workflow.run()
