import logging

import pysistence as immutable

import mail_renderer as mr
import data_sources as dss

class LongReads(mr.EmailTemplate):
    recognized_versions = ['v1']
    cache_bust=True

    data_sources = immutable.make_dict({
        'v1': {
            'long_reads': dss.long_reads.Reads(mr.client),
            'long_reads_audio': dss.long_reads.Audio(mr.client),
        }
    })

    priority_list = immutable.make_dict({
        'v1': [
            ('long_reads', 3),
            ('long_reads_audio', 3)
            ]
    })

    template_names = immutable.make_dict({
        'v1': 'long_reads/v1',
    })