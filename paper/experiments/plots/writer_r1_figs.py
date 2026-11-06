"""Writer, round 1: regenerate fig13/fig14/fig15 for print legibility (fonts >= 7 pt, legends outside data,
encoder token sizes in fig13c) from the existing R1 CSVs, without rewriting r1_summary.txt.
python -m plots.writer_r1_figs --in ../results"""
import argparse
from plots import make_r1 as m

ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="inp", default="../results")
m.IN = ap.parse_args().inp
A = m.rd("r1_oprg_agg.csv")
_, fig, axs = m.deciles()
m.oprg_fig(A, fig, axs)
m.pmove()
m.b11(None)
