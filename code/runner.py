#!/usr/bin/env python

from kinetix import parser
import argparse 
import sys 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run(exp,args):
    result = exp.run(args.steps,dt=args.delta_t)

    df = pd.DataFrame(result)
    if args.plot_out is not None:
        ax = sns.lineplot(data=df.melt(id_vars='step'),y='value',x='step',hue='variable')
        ax.set_xlabel('Time (100 ms increments)')
        ax.set_ylabel('Concentration (mM)')
        plt.savefig(args.plot_out)
    if args.csv_out is not None:
        df.to_csv(args.csv_out,index=False)



if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input', help='input yaml file with reaction definitions')
    argparser.add_argument('--csv_out', help='output csv file with reaction steps',default=None)
    argparser.add_argument('--plot_out', help='plot of the reaction kinetics',default=None)
    argparser.add_argument('--steps', help='number of steps to simulate (seconds)', type=int, default=1000)
    argparser.add_argument('--delta_t',help='size of each step (seconds)', type=float, default=0.01)
    args = argparser.parse_args()

    # Read the yaml file:
    yaml_parser = parser.KinetixParser(args.input)
    
    experiment = yaml_parser.parse_experiment()
    run(experiment,args)
    
