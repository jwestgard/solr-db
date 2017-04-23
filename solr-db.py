#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import csv
import requests

HOST = 'localhost'
PORT = '8983'

#=== SUBCOMMAND =============================================================
#         NAME: load
#  DESCRIPTION: 
#============================================================================

'''
http://localhost:9600/solr/irroc/update/csv?commit=true&f.meta_description.split=true&f.meta_description.separator=,&f.stage_list.split=true&f.stage_list.separator=;&f.task_list.split=true&f.task_list.separator=;&f.stage_list_facet.split=true&f.stage_list_facet.separator=;&f.task_list_facet.split=true&f.task_list_facet.separator=;" --data-binary @$1 -H 'Content-type:text/csv; charset=utf-8'
'''


def load(args):
    '''load CSV data to Solr'''
    core = args.core
    url = 'http://{0}:{1}/solr/{2}/update/csv'.format(HOST, PORT, core)
    headers = {'Content-type': 'text/csv', 'charset': 'utf-8'}
    params = {'commit': True}

    with open(args.data, 'r') as datafile:
        header_row = next(csv.reader(datafile))
        print('Reading column info from data file: {0}'.format(args.data))
        for col in header_row:
            if col.startswith('['):
                fieldname = col.strip('[]')
                key1 = 'f.{0}.split'.format(fieldname)
                key2 = 'f.{0}.separator'.format(fieldname)
                params[key1] = 'true'
                params[key2] = ';'

    with open(args.data, 'rb') as datafile:
        data = datafile.read()
        response = requests.post(url, data=data, 
                                 params=params,
                                 headers=headers
                                 )
        print('Querying {0}'.format(response.url))
        print(response.text)


#=== SUBCOMMAND =============================================================
#         NAME: read
#  DESCRIPTION: 
#============================================================================

def read(args):
    '''read all data from existing core and summarize'''
    print('Read all data from Solr!')


#=== SUBCOMMAND =============================================================
#         NAME: delete
#  DESCRIPTION: 
#============================================================================

def delete(args):
    '''empty the existing core of all data'''
    print('Delete all data from Solr!')


#============================================================================
# MAIN LOOP
#============================================================================

def main():
    '''parse command line arguments and run subcommand'''
    parser = argparse.ArgumentParser(
                    description='Solr database management utility.'
                    )

    parser.add_argument('-v', '--version', 
                    action='version', 
                    help='print version number and exit',
                    version='%(prog)s 0.1'
                    )

    # common args for all subcommands
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-c', '--core',
                    help='core to act upon'
                    )

    # create the subcommand scaffolding
    subparsers = parser.add_subparsers(title='subcommands', 
                    description='valid subcommands', 
                    help='-h additional help', 
                    metavar='{load,read,delete}',
                    dest='cmd'
                    )
    subparsers.required = True

    # args specific to the load subcommand
    load_parser = subparsers.add_parser('load',
                    help='load csv data to solr',
                    description='load preprocessed data from CSV to Solr',
                    parents=[parent_parser]
                    )
    load_parser.add_argument('-d', '--data',
                    help='csv file to load'
                    )
    load_parser.set_defaults(func=load)

    # args specific to the read subcommand
    read_parser = subparsers.add_parser('read',
                    help='read data from solr core',
                    description='read and summarize data in existing core',
                    parents=[parent_parser]
                    )
    load_parser.set_defaults(func=load)

    # args specific to the delete subcommand
    delete_parser = subparsers.add_parser('delete', 
                    help='delete data from existing solr core',
                    description='clean out core by deleting all data',
                    parents=[parent_parser]
                    )
    delete_parser.set_defaults(func=delete)

    # parse args and execute the specified subcommand function
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
