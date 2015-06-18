import logging

import pysistence as immutable

import handlers
import mail_renderer as mr
import data_sources as dss

class LongReads(handlers.EmailTemplate):
    recognized_versions = ['v1']

    data_sources = immutable.make_dict({
        'v1': {
            'long_reads': dss.long_reads.Reads(mr.client),
            'long_reads_audio': dss.long_reads.Audio(mr.client),
        }
    })

    priority_list = immutable.make_dict({
        'v1': [
            ('long_reads', 3),
            ('long_reads_audio', 2)
            ]
    })

    template_names = immutable.make_dict({
        'v1': 'long_reads/v1',
    })