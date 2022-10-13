# Import modules
from flask_restplus import Namespace, Resource
from . import request_parser
from . import representations
from . import exceptions

# Import AutoPVS1 code
from pvs1 import PVS1
from utils import get_transcript, get_vcfrecord, vep_consequence_trans
from read_data import transcripts_hg19, transcripts_hg38

"""
Create a parser object locally
"""
parser = request_parser.parser

api = Namespace('AutoPVS1', description='AutoPVS1 API Endpoints')


@api.route("/autopvs1/<string:genome_build>/<string:genomic_coordinate>/<string:select_transcripts>/<string:hgvs_c>/<string:hgvs_p>/<string:consequence>")
@api.param("genome_build", "***Accepted:***\n"
                           ">   - hg19\n"
                           ">   - hg38")
@api.param("genomic_coordinate", "\n***Pseudo-VCF***\n"
                                 ">   - chr13-32912166-C-CA")
@api.param("select_transcripts", "\n***Single***\n"
                                 ">   NM_000093.4\n"
                                 ">   NM_000059.4")
@api.param("hgvs_c", "***HGVS-Nomenclature cDNA.c***\n"
                     ">   - c.3674_3675insA\n"
                     ">   - c.589G>T")
@api.param("hgvs_p", "***HGVS-Nomenclature protein - 3 Letter by VEP***\n"
                     ">   - p.Leu1227ThrfsTer6")
@api.param("consequence", "***Coding consequenc by VEP***\n"
                          ">   - frameshift_variant")
class AutoPVS1Class(Resource):
    # Add documentation about the parser
    @api.expect(parser, validate=True)
    def get(self, genome_build, genomic_coordinate, select_transcripts, hgvs_c, hgvs_p, consequence):

        # Predict pvs1 using the AutoPVS1 Python Library
        genomic_coordinate = get_vcfrecord(genomic_coordinate)
        consequence = vep_consequence_trans(consequence)
        if genome_build in ["GRCh37", "hg19"]:
            transcript = get_transcript(select_transcripts, transcripts_hg19)
        elif genome_build in ["GRCh38", "hg38"]:
            transcript = get_transcript(select_transcripts, transcripts_hg38)
        
        validate = PVS1(genomic_coordinate, consequence, hgvs_c, hgvs_p, transcript, genome_build)
        content = { "strength": validate.strength.name,
                    "description": validate.desc,
                    "init_path": validate.init_path,
                    "criterion": validate.criterion}

        # Collect Arguments
        args = parser.parse_args()

        # Overrides the default response route so that the standard HTML URL can return any specified format
        if args['content-type'] == 'application/json':
            # example: http://127.0.0.1:5000.....bob?content-type=application/json
            return representations.application_json(content, 200, None)
        # example: http://127.0.0.1:5000.....?content-type=application/xml
        elif args['content-type'] == 'application/xml':
            return representations.xml(content, 200, None)
        else:
            # Return the api default output
            return content