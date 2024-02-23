#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitary functions to manage, check and preprocess large sampling data assiciated with passive acoustic monitoring

"""
import os
import argparse
import matplotlib.pyplot as plt
from maad import sound, util
from pamflow.preprocess.utils import (
    load_config, 
    metadata_summary, 
    add_file_prefix, 
    select_metadata,
    audio_timelapse,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Perform preprocessing operations on audio data.")
    parser.add_argument(
        "operation", 
        choices=["get_audio_metadata", 
                 "metadata_summary",
                 "select_metadata",
                 "audio_timelapse",
                 "add_file_prefix"], 
        help="Preprocessing operation")
    
    parser.add_argument("--input", "-i", 
                        type=str, help="Path to directory to search")
    parser.add_argument("--output", "-o", 
                        type=str, help="Path and filename to save results")
    parser.add_argument("--config", "-c", type=str, default='config.yaml',
                        help="Path to configuration file. ")
    parser.add_argument("--recursive", "-r", 
                        action="store_true", help="Enable recursive mode")
    parser.add_argument("--quiet", "-q", 
                        action="store_true", help="Enable quiet mode")
    args = parser.parse_args()

    verbose = 0 if args.quiet else 1

    if args.operation == "get_audio_metadata":
        df = util.get_metadata_dir(args.input, verbose)
        df.dropna(inplace=True)  # remove problematic files
        df.to_csv(args.output, index=False)
    
    elif args.operation == "add_file_prefix":
        _ = add_file_prefix(args.input, args.recursive, verbose)
    
    elif args.operation == "audio_timelapse":
        config = load_config(args.config)
        date_range = config['preprocessing']['date_range']
        sample_length = config['preprocessing']['sample_length']
        audio_timelapse(
            args.input, sample_length, sample_period='30T', date_range=date_range, path_save=args.output, save_audio=True, verbose=True)
    
    elif args.operation == "metadata_summary":
        df = metadata_summary(args.input)
        df.to_csv(args.output)
    
    elif args.operation == "select_metadata":
        df = select_metadata(args.input)
        df.to_csv(args.output)