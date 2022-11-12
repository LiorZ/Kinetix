# Kinetix - A simple enzyme kinetics simulation framework

This is a simple framework for single / multiple reaction enzyme kinetics simulation and plotting.
It allows one to plot reaction kinetics that follows the reversible [Michaelis - Menten](https://en.wikipedia.org/wiki/Michaelis%E2%80%93Menten_kinetics) model.

## Usage
One can use the library to produce figures via a command line interface or programmatically (see below for examples)

### CLI
#### Single reaction

As an example, the reaction kinetics of Glucose Kinase (EC: [2.7.1.2](https://www.brenda-enzymes.org/enzyme.php?ecno=2.7.1.2) is displayed as an example)
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/8/8d/Glucokinase.png" />
</p>
First, create a definition file in YAML format, that defines the reaction parameters:

```yaml
name: "Glucose kinase simulation"
reactants: #Concentration of the reactants at the beginning of the reaction (mM)
  glucose: 0.2
  glucose_6_p: 0.0
enzymes: #Concentration of the enzyme(s) at the begining of the reaction (mM)
  gluk: 0.05 
reaction: #Kinetic parameters of each of the enzymes for the forward and backward steps of the (reversible) reaction. Note that non-reversible reactions can simple be modeled with high Km for on of the directions.
  gluk: 
    fwd: "glucose"
    back: "glucose_6_p"
    km_fwd: 0.24
    km_back: 21
    kcat_fwd: 61
    kcat_back: 15.9
```

Then, run the simulation with a simple command line and a few arguments:
```
python ./code/runner.py examples/glucose_kinase.yaml --plot_out gluc.png --csv_out gluc.csv
```
A figure showing the progression of the reaction as a function of time is generated:
<p align="center">
  <img src="examples/figures/gluc.svg" />
</p>

A csv file containing the data used to generate the figure can also optionally be generated and saved (using the `--csv_out` flag)

#### A pathway
Kinetix can also simulate a pathway composed of several enzymes. This example shows a pathway composed of 3 different enzymes used in the production of [allulose](https://en.wikipedia.org/wiki/Psicose) (D-psicose) a C3 epimer of fructose:

1. **Fructose kinase** (for the production of fructose-6-phosphate)
2. **D-psicose-3-epimerase** (converting fructose-6-phosphate to allulose-6-phosphate)
3. **Alkaline phosphatase** (converting allulose-6-phosphate to allulose)


The flow is similar to the one-enzyme case. First, define a yaml file with all the parameters:

```yaml
---
name: "Allulose synthesis from fructose"
reactants:
  fructose: 1.8
  fructose_6_p: 0.0
  allulose: 0.0
  allulose_6_p: 0.0
enzymes:
  fruk: 0.05
  alsE: 0.05
  phosphatase: 0.05
reaction:
  fruk:
    fwd: "fructose_6_p"
    back: "fructose"
    km_fwd: 0.24
    km_back: 21
    kcat_fwd: 61
    kcat_back: 15.9
  alsE:
    fwd: "allulose_6_p"
    back: "fructose_6_p"
    km_fwd: 1.6 
    km_back: 1.6 
    kcat_fwd: 46
    kcat_back: 46
  phosphatase:
    fwd: "allulose"
    back: "allulose_6_p"
    km_fwd: 1 
    km_back: 100
    kcat_fwd: 100
    kcat_back: 1
```

Then, invoke the application just as before:
```
./code/runner.py examples/allulose.yaml --plot_out examples/figures/alu.svg --csv_out examples/csvs/alu.csv
```

To produce the reaction figure, which displays the concentration of each of the reactants as a function of time:
<p align="center">
  <img src="examples/figures/alu.svg" />
</p>

### Programmatic Access
Kinetix also makes it really easy to simulate and plot a reaction more flexibly via a simple API.
Example:

https://github.com/LiorZ/Kinetix/blob/4d1107d3e85c45d8d3f222428936ef82c658f223/examples/programmatic.py#L8-L44
