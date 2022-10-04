#!/usr/bin/python3.9

import argparse
import json
# from pvs1 import PVS1
# from utils import get_transcript, get_vcfrecord, vep_consequence_trans
# from read_data import transcripts_hg19, transcripts_hg38

class run_autoPvs1():
       
    def setParameter(self):
        self._key = self._inputJson['key']
        self._vcfrecord = get_vcfrecord(self._key)

        self._hgvsC = self._inputJson['hgvs_c']
        self._hgvsP = self._inputJson['hgvs_p']
        self._consequence = vep_consequence_trans(self._inputJson['consequence'])

        self._genomeVersion = self._inputJson['genome_version']
        if self._genomeVersion in ['GRCh37', 'hg19']:
            self._transcript = get_transcript(self._inputJson['transcript'], transcripts_hg19)
        elif self._genomeVersion in ['GRCh38', 'hg38']:
            self._transcript = get_transcript(self._inputJson['transcript'], transcripts_hg38)

    
    def run(self, inputFile):

        with open(inputFile, 'r') as inputData:
            # inputData1= inputData.read()
            # inputData2 = json.load(inputData)
            # print(inputData2)
            for inputLine in inputData:
                self._vcfrecord = 'na'
                self._consequence = 'na'
                self._hgvsC = 'na'
                self._hgvsP = 'na'
                self._transcript = 'na'
                self._genomeVersion = 'na'

                print (inputLine)
                print (json.load(inputLine))
                self._inputJson = inputData[inputLine]
                print(self._inputJson)
                # self.setParameter()

                # self._output = PVS1(self._vcfrecord, self._consequence,
                #                     self._hgvsC, self._hgvsP,
                #                     self._transcript, self._genomeVersion)

                # print(self._output.strength_raw.name)

# key = 'chr13-32890593-TA-T'
# chrom = vcfrecord.chrom
# pos = vcfrecord.pos
# ref = vcfrecord.ref
# alt = vcfrecord.alt
# vcfrecord2 = VCFRecord(chrom, pos, ref, alt)


# hgvs_c = 'c.1delA'
# hgvs_p = 'p.Met1fs'
# genome_version = 'hg19'

# vep_trans = 'NM_000059.4'
# transcript = get_transcript(vep_trans, transcripts_hg19)

# vep_consequence = 'frameshift&start_lost&start_retained'
# consequence = vep_consequence_trans(vep_consequence)

# pvs1.strength_raw.name
# pvs1.transcript.full_name
# pvs1.strength.name


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='run AutoPVS1')
    parser.add_argument('--input', type=str, help='Input json file name', default='None')
    args = parser.parse_args()

    workflow = run_autoPvs1()
    workflow.run(args.input)
