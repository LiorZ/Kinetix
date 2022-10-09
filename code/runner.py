#!/usr/bin/env python

from kinetix import parser
import argparse 
import sys 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run(exp,args):
    result = experiment.run(args.steps,dt=args.dt)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input', help='input yaml file with reaction definitions')
    argparser.add_argument('--csv_out', help='output csv file with reaction steps')
    argparser.add_argment('--plot_out', help='plot of the reaction kinetics')
    argparser.add_argument('--steps', help='number of steps to simulate (seconds)', type=int, default=1000)
    argparser.add_argument('--delta_t',help='size of each step (seconds)', type=float, default=0.01)
    args = argparser.parse_args()

    dt = args.delta_t
    steps = args.steps


    # Read the yaml file:
    yaml_parser = parser.KinetixParser(args.input)
    
    experiment = yaml_parser.parse_experiment()
    df = pd.DataFrame(result)

    ax = sns.lineplot(data=df.melt(id_vars='step'),y='value',x='step',hue='variable')

    plt.savefig('output.png')

