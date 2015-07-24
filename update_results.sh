
# Update the noisy tournaments
echo "-- Regenerating noisy tournament figures"
# Run the noisy tournament
./run_axelrod --noise 0.05 --xc -p 0
# Copy these figures over, renaming as appropriate
cp strategies_payoff.png assets/strategies_payoff_noise_5.png
cp strategies_boxplot.png assets/strategies_boxplot_noise_5.png

# Running noiseless tournament
echo "-- Running Axelrod, regenerating cache, results, and figures"
# Also Copy the results and figures over to assets
./run_axelrod --rc -p 0 -o assets

echo "Be sure to git commit changes to update the docs!"