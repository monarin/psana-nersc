dark_runs=(6 18 29 36 54 59 75)
light_runs=(7 19 30 37 55 60 76) 
let "n_runs=${#dark_runs[@]}-1"
for i in `seq 0 $n_runs`; do
    python get_pedestals.py cxic0515 DsdCsPad ${light_runs[$i]} ${dark_runs[$i]}
done
