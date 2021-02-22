#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# import datetime
# import numpy as np
import json

from nomad.datamodel import EntryArchive
from nomad.parsing import FairdiParser
from nomad.units import ureg as units
from nomad.datamodel.metainfo.public import section_run as Run
from nomad.datamodel.metainfo.public import section_system as System
from nomad.datamodel.metainfo.public import section_single_configuration_calculation as SCC

from . import metainfo  # pylint: disable=unused-import
# from .metainfo import Measurement, Sample, Metadata, Instrument
from .metainfo import *
'''
This is a hello world style example for an example parser/converter.
'''


class ExampleParser(FairdiParser):
    def __init__(self):
        super().__init__(
            name='parsers/example', code_name='EXAMPLE', code_homepage='https://www.example.eu/',
            mainfile_mime_re=r'(application/json)'
        )

    def run(self, mainfile: str, archive: EntryArchive, logger):
        # Log a hello world, just to get us started. TODO remove from an actual parser.
        logger.info('Testing the World')

        # Read the JSON file into a dictionary
        with open(mainfile, 'rt') as f:
            file_data = json.load(f)

        for measurement_data in file_data:
            # Reading a measurement
            measurement = archive.m_create(Measurement)

            # Create the hierarchical structure
            metadata = measurement.m_create(Metadata)
            data = measurement.m_create(Data)

            # Create the hierarchical structure inside metadata
            sample = metadata.m_create(Sample)
            experiment = metadata.m_create(Experiment)
            instrument = metadata.m_create(Instrument)
            author_generated = metadata.m_create(AuthorGenerated)

            # Load entries into each above hierarchical structure
            # Sample
            sample.spectrum_region = measurement_data['metadata']['spectrum_region']

            # Experiment
            experiment.method_type = measurement_data['metadata']['method_type']

            # Instrument
            instrument.n_scans = measurement_data['metadata']['n_scans']
            instrument.dwell_time = measurement_data['metadata']['dwell_time']
            instrument.excitation_energy = measurement_data['metadata']['excitation_energy']

            if measurement_data['metadata']['source_label']:
                instrument.source_label = measurement_data['metadata']['source_label']

            author_generated.author_name = measurement_data['metadata']['author']
            author_generated.group_name = measurement_data['metadata']['group_name']
            author_generated.sample_id = measurement_data['metadata']['sample']
            author_generated.experiment_id = measurement_data['metadata']['experiment_id']
            author_generated.timestamp = measurement_data['metadata']['timestamp']

            # Data Header
            for label_data in measurement_data['metadata']['data_labels']:
                data_header = metadata.m_create(DataHeader)
                data_header.channel_id = str(label_data['channel_id'])
                data_header.label = label_data['label']
                data_header.unit = label_data['unit']

            # Reading columns
            numerical_values = data.m_create(NumericalValues)
            numerical_values.data_values = measurement_data['data']
